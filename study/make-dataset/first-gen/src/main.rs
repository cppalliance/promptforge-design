// First-gen extractor.
//
// Finds the true first-generation version of every tool file across four
// separate git repos. Files were renamed, moved between directories, and
// moved across repo boundaries, so git --follow alone cannot trace them.
// The robust key is the basename: search every repo's full history for the
// creation of any file with that basename, take the globally earliest, and
// that is the first generation.

use std::collections::BTreeMap;
use std::path::{Path, PathBuf};
use std::process::Command;

use anyhow::{anyhow, Context, Result};
use clap::Parser;
use serde::Serialize;

/// Repos to search, in no particular order; ages are discovered from git.
const REPOS: &[&str] = &["tools-public", "staff-private", "umbra", "profiles-coalition"];

/// Directories whose current .md files are the tools to resolve. Each entry
/// is (repo, path-relative-to-repo).
const SOURCE_DIRS: &[(&str, &str)] = &[
    ("tools-public", "tools"),
    ("tools-public", "tools-wg21"),
    ("tools-public", "how-to"),
    ("staff-private", "tools"),
    ("umbra", "tools"),
    ("profiles-coalition", "campaign/tools"),
];

/// A commit that created a file with some basename, in some repo, at some path.
#[derive(Clone)]
struct Birth {
    repo: String,
    commit: String,
    unix: i64,
    iso: String,
    path: String, // path relative to repo root
}

#[derive(Serialize)]
struct ManifestRow {
    basename: String,
    current_repo: String,
    current_path: String,
    origin_repo: String,
    origin_path: String,
    birth_commit: String,
    birth_date: String,
    repos_seen: Vec<String>,
    cross_repo: bool,
    flags: Vec<String>,
}

#[derive(Parser, Debug)]
#[command(about = "Extract the first-generation version of every tool across repos")]
struct Args {
    /// Workspace root containing the repos
    #[arg(long, default_value = ".")]
    workspace: PathBuf,

    /// Output directory for extracted v1 files
    #[arg(long, default_value = "first-gen")]
    out: PathBuf,

    /// Manifest JSONL path
    #[arg(long, default_value = "manifest.jsonl")]
    manifest: PathBuf,

    /// Commits touching more than this many files count as bulk imports
    #[arg(long, default_value_t = 20)]
    bulk_threshold: usize,
}

/// Run a git command in a repo and return stdout, or an error with stderr.
fn git(repo: &Path, args: &[&str]) -> Result<String> {
    let out = Command::new("git")
        .arg("-C")
        .arg(repo)
        .args(args)
        .output()
        .with_context(|| format!("spawn git {args:?}"))?;
    if !out.status.success() {
        return Err(anyhow!(
            "git {args:?} in {}: {}",
            repo.display(),
            String::from_utf8_lossy(&out.stderr).trim()
        ));
    }
    Ok(String::from_utf8_lossy(&out.stdout).into_owned())
}

fn basename(path: &str) -> String {
    path.rsplit(['/', '\\']).next().unwrap_or(path).to_string()
}

/// Build the birth index for one repo: basename -> every creation event.
/// Uses --diff-filter=A so only original creations are recorded; later
/// renames appear as R and are skipped, which is what we want because the
/// A entry is the true birth at the original name.
fn build_birth_index(repo_path: &Path, repo: &str) -> Result<BTreeMap<String, Vec<Birth>>> {
    // Sentinel-delimited commit header, then A-filtered name-status lines.
    let log = git(
        repo_path,
        &[
            "log",
            "--all",
            "--diff-filter=A",
            "--name-status",
            "--pretty=format:C|%H|%at|%aI",
        ],
    )?;

    let mut index: BTreeMap<String, Vec<Birth>> = BTreeMap::new();
    let mut cur: Option<(String, i64, String)> = None;
    for line in log.lines() {
        if let Some(rest) = line.strip_prefix("C|") {
            let mut it = rest.splitn(3, '|');
            let commit = it.next().unwrap_or_default().to_string();
            let unix = it.next().unwrap_or("0").parse::<i64>().unwrap_or(0);
            let iso = it.next().unwrap_or_default().to_string();
            cur = Some((commit, unix, iso));
        } else if let Some((commit, unix, iso)) = cur.as_ref() {
            // Name-status line for an addition: "A\t<path>"
            if let Some(path) = line.strip_prefix("A\t") {
                let path = path.trim();
                if !path.is_empty() {
                    index.entry(basename(path)).or_default().push(Birth {
                        repo: repo.to_string(),
                        commit: commit.clone(),
                        unix: *unix,
                        iso: iso.clone(),
                        path: path.to_string(),
                    });
                }
            }
        }
    }
    Ok(index)
}

/// Every historical basename a file had within its current repo, via --follow.
fn historical_names(repo_path: &Path, rel_path: &str) -> Vec<String> {
    let out = match git(
        repo_path,
        &["log", "--follow", "--name-only", "--pretty=format:", "--", rel_path],
    ) {
        Ok(s) => s,
        Err(_) => return vec![],
    };
    let mut names: Vec<String> = out
        .lines()
        .map(str::trim)
        .filter(|l| !l.is_empty())
        .map(basename)
        .collect();
    names.sort();
    names.dedup();
    names
}

/// Number of files a commit touched, for the bulk-import heuristic.
fn commit_file_count(repo_path: &Path, commit: &str) -> usize {
    git(
        repo_path,
        &["diff-tree", "--no-commit-id", "--name-only", "-r", commit],
    )
    .map(|s| s.lines().filter(|l| !l.trim().is_empty()).count())
    .unwrap_or(0)
}

fn main() -> Result<()> {
    let args = Args::parse();
    let ws = &args.workspace;

    // 1. Enumerate current tools.
    let mut current: Vec<(String, String, String)> = Vec::new(); // (repo, rel_path, basename)
    for (repo, dir) in SOURCE_DIRS {
        let full = ws.join(repo).join(dir);
        let entries = std::fs::read_dir(&full)
            .with_context(|| format!("read dir {}", full.display()))?;
        for e in entries {
            let e = e?;
            let p = e.path();
            if p.extension().and_then(|s| s.to_str()) == Some("md") {
                let name = p.file_name().unwrap().to_string_lossy().to_string();
                let rel = format!("{dir}/{name}");
                current.push((repo.to_string(), rel, name));
            }
        }
    }
    current.sort();
    println!("Enumerated {} current tool files.", current.len());

    // 2. Build birth index per repo.
    let mut births: BTreeMap<String, Vec<Birth>> = BTreeMap::new();
    for repo in REPOS {
        let repo_path = ws.join(repo);
        let idx = build_birth_index(&repo_path, repo)
            .with_context(|| format!("birth index for {repo}"))?;
        let n: usize = idx.values().map(|v| v.len()).sum();
        println!("  {repo}: {} creation events across {} basenames", n, idx.len());
        for (k, mut v) in idx {
            births.entry(k).or_default().append(&mut v);
        }
    }

    std::fs::create_dir_all(&args.out)
        .with_context(|| format!("create out dir {}", args.out.display()))?;
    let mut manifest = std::fs::File::create(&args.manifest)
        .with_context(|| format!("create manifest {}", args.manifest.display()))?;
    use std::io::Write as _;

    let mut same_repo = 0usize;
    let mut cross_repo = 0usize;
    let mut flagged = 0usize;
    let mut extracted = 0usize;

    for (repo, rel_path, name) in &current {
        let repo_path = ws.join(repo);

        // 3. Match set: current basename plus every historical name in this repo.
        let mut match_set = historical_names(&repo_path, rel_path);
        if !match_set.contains(name) {
            match_set.push(name.clone());
        }

        // 4. Global earliest birth across all repos for any name in the set.
        let mut candidates: Vec<&Birth> = Vec::new();
        for n in &match_set {
            if let Some(v) = births.get(n) {
                candidates.extend(v.iter());
            }
        }
        let origin = candidates.iter().min_by_key(|b| b.unix).copied();

        let Some(origin) = origin else {
            eprintln!("  WARN no birth found for {repo}/{rel_path}");
            continue;
        };

        let mut repos_seen: Vec<String> =
            candidates.iter().map(|b| b.repo.clone()).collect();
        repos_seen.sort();
        repos_seen.dedup();

        let is_cross = &origin.repo != repo;
        let mut flags: Vec<String> = Vec::new();

        // Residual: origin in current repo but born in a bulk import commit,
        // so the real origin may predate this repo under a different name.
        if !is_cross {
            let origin_repo_path = ws.join(&origin.repo);
            let count = commit_file_count(&origin_repo_path, &origin.commit);
            if count > args.bulk_threshold {
                flags.push("possible-earlier-origin".to_string());
            }
        }

        // 5. Extract v1.
        let origin_repo_path = ws.join(&origin.repo);
        let spec = format!("{}:{}", origin.commit, origin.path);
        let content = git(&origin_repo_path, &["show", &spec])
            .with_context(|| format!("extract {spec} from {}", origin.repo))?;
        std::fs::write(args.out.join(name), &content)
            .with_context(|| format!("write {}", name))?;
        extracted += 1;

        if is_cross {
            cross_repo += 1;
        } else {
            same_repo += 1;
        }
        if !flags.is_empty() {
            flagged += 1;
        }

        // 6. Manifest row.
        let row = ManifestRow {
            basename: name.clone(),
            current_repo: repo.clone(),
            current_path: rel_path.clone(),
            origin_repo: origin.repo.clone(),
            origin_path: origin.path.clone(),
            birth_commit: origin.commit.clone(),
            birth_date: origin.iso.clone(),
            repos_seen,
            cross_repo: is_cross,
            flags,
        };
        writeln!(manifest, "{}", serde_json::to_string(&row)?)?;
    }

    manifest.flush()?;
    println!(
        "\nExtracted {extracted} v1 files to {}.\n  same-repo origin: {same_repo}\n  cross-repo origin: {cross_repo}\n  flagged uncertain: {flagged}\nManifest: {}",
        args.out.display(),
        args.manifest.display()
    );
    Ok(())
}
