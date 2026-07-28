// pairgen: the minimal end-to-end pair path.
//
// For a "pair" record: sharpen the bloated prompt with the instrument,
// strip em-dashes mechanically, then run two gates - execution-equivalence
// against the input, and rulebook-compliance against the instrument's
// checklist. Keep the pair only if both gates pass.
//
// For a "control" record: run gate 1 directly on a (reference, corrupted)
// pair that SHOULD fail, to prove the gate discriminates rather than
// rubber-stamps.
//
// All model calls are direct /v1/messages to claude-opus-4-8 with adaptive
// thinking at high effort. No Cursor harness, no system context.

use std::path::PathBuf;
use std::time::Duration;

use anyhow::{anyhow, Context, Result};
use clap::Parser;
use serde::{Deserialize, Serialize};

#[derive(Parser, Debug)]
#[command(about = "Sharpen, strip, and gate bloated prompts into training pairs")]
struct Args {
    #[arg(long, default_value = "sharpen-instrument.md")]
    instrument: PathBuf,

    /// JSONL of input records (kind: pair | control)
    #[arg(long)]
    input: PathBuf,

    #[arg(long, default_value = "pairgen-out.jsonl")]
    out: PathBuf,

    #[arg(long, default_value = "claude-opus-4-8")]
    model: String,

    #[arg(long, default_value = "high")]
    effort: String,

    #[arg(long, default_value_t = 32000)]
    max_tokens: u32,

    #[arg(long)]
    api_key: Option<String>,
}

const TIGHTEN: &str = "Above is a set of rules for tightening a prompt. Apply every applicable rule to the prompt below. Make it unambiguous and cut dead weight. Preserve exactly the meaning an executing model would follow: every instruction, condition, number, name, and defined behavior. Do not add, explain, or improve; only tighten. Output only the tightened prompt, with no preamble and no commentary.";

// --- API types (adaptive thinking) ---

#[derive(Serialize)]
struct ApiRequest {
    model: String,
    max_tokens: u32,
    thinking: Thinking,
    output_config: OutputConfig,
    messages: Vec<Msg>,
}
#[derive(Serialize)]
struct Thinking {
    #[serde(rename = "type")]
    kind: String,
}
#[derive(Serialize)]
struct OutputConfig {
    effort: String,
}
#[derive(Serialize)]
struct Msg {
    role: String,
    content: String,
}
#[derive(Deserialize)]
struct ApiResponse {
    content: Vec<Blk>,
}
#[derive(Deserialize)]
struct Blk {
    #[serde(rename = "type")]
    kind: String,
    #[serde(default)]
    text: String,
}

#[derive(Deserialize)]
struct InRec {
    kind: String,
    #[serde(default)]
    source: String,
    #[serde(default)]
    bloated: String,
    #[serde(default)]
    a: String,
    #[serde(default)]
    b: String,
    #[serde(default)]
    corruption: String,
}

#[derive(Serialize, Default)]
struct OutRec {
    kind: String,
    source: String,
    bloated: String,
    sharpened: String,
    control_a: String,
    control_b: String,
    corruption: String,
    gate1: String,
    gate1_reason: String,
    gate2: String,
    gate2_violations: String,
    kept: bool,
    expected_fail: bool,
    control_ok: bool,
}

/// Replace em-dashes, en-dashes, and prose double-hyphens with ASCII, while
/// leaving fenced code and inline `code` untouched. Line-based so leading
/// whitespace (list nesting, indentation) is preserved.
fn normalize_dashes(text: &str) -> String {
    let mut out = Vec::new();
    let mut in_fence = false;
    for line in text.lines() {
        if line.trim_start().starts_with("```") {
            in_fence = !in_fence;
            out.push(line.to_string());
            continue;
        }
        if in_fence {
            out.push(line.to_string());
            continue;
        }
        // Preserve leading whitespace; transform the rest.
        let lead_len = line.len() - line.trim_start().len();
        let (lead, body) = line.split_at(lead_len);
        // Structural hyphen runs (frontmatter/HR "---") are not prose dashes.
        if body.len() >= 3 && body.chars().all(|c| c == '-') {
            out.push(line.to_string());
            continue;
        }
        // Protect inline code spans: transform only the segments outside backticks.
        let mut result = String::new();
        let mut in_code = false;
        let mut buf = String::new();
        let flush = |buf: &mut String, result: &mut String| {
            let t = buf.replace('\u{2014}', " - ").replace('\u{2013}', "-");
            // Collapse a run of exactly two ASCII hyphens (prose double-dash)
            // to one. Leave single hyphens and runs of 3+ (rules, separators).
            let chars: Vec<char> = t.chars().collect();
            let mut dashed = String::with_capacity(t.len());
            let mut i = 0;
            while i < chars.len() {
                if chars[i] == '-' {
                    let mut j = i;
                    while j < chars.len() && chars[j] == '-' {
                        j += 1;
                    }
                    let run = j - i;
                    if run == 2 {
                        dashed.push('-');
                    } else {
                        for _ in 0..run {
                            dashed.push('-');
                        }
                    }
                    i = j;
                } else {
                    dashed.push(chars[i]);
                    i += 1;
                }
            }
            let t = dashed;
            // collapse runs of 2+ spaces introduced by the replacements
            let mut collapsed = String::with_capacity(t.len());
            let mut prev_space = false;
            for c in t.chars() {
                if c == ' ' {
                    if !prev_space {
                        collapsed.push(c);
                    }
                    prev_space = true;
                } else {
                    collapsed.push(c);
                    prev_space = false;
                }
            }
            result.push_str(&collapsed);
            buf.clear();
        };
        for c in body.chars() {
            if c == '`' {
                if in_code {
                    result.push_str(&buf); // code span verbatim
                    buf.clear();
                    result.push('`');
                    in_code = false;
                } else {
                    flush(&mut buf, &mut result);
                    result.push('`');
                    in_code = true;
                }
            } else {
                buf.push(c);
            }
        }
        if in_code {
            result.push_str(&buf); // unterminated span: leave verbatim
        } else {
            flush(&mut buf, &mut result);
        }
        out.push(format!("{lead}{result}"));
    }
    out.join("\n")
}

async fn call(client: &reqwest::Client, key: &str, args: &Args, prompt: &str) -> Result<String> {
    let body = ApiRequest {
        model: args.model.clone(),
        max_tokens: args.max_tokens,
        thinking: Thinking { kind: "adaptive".to_string() },
        output_config: OutputConfig { effort: args.effort.clone() },
        messages: vec![Msg { role: "user".to_string(), content: prompt.to_string() }],
    };
    let mut backoff = Duration::from_secs(3);
    for attempt in 1..=4 {
        let resp = client
            .post("https://api.anthropic.com/v1/messages")
            .header("x-api-key", key)
            .header("anthropic-version", "2023-06-01")
            .header("content-type", "application/json")
            .json(&body)
            .send()
            .await;
        match resp {
            Ok(r) if r.status().is_success() => {
                let parsed: ApiResponse = r.json().await.context("parse response")?;
                let out: String = parsed
                    .content
                    .into_iter()
                    .filter(|b| b.kind == "text")
                    .map(|b| b.text)
                    .collect::<Vec<_>>()
                    .join("");
                if out.trim().is_empty() {
                    return Err(anyhow!("empty output"));
                }
                return Ok(out.trim().to_string());
            }
            Ok(r) => {
                let s = r.status();
                let detail = r.text().await.unwrap_or_default();
                if (s.as_u16() == 429 || s.is_server_error()) && attempt < 4 {
                    tokio::time::sleep(backoff).await;
                    backoff *= 2;
                    continue;
                }
                return Err(anyhow!("API error {s}: {detail}"));
            }
            Err(e) if attempt < 4 => {
                tokio::time::sleep(backoff).await;
                backoff *= 2;
                let _ = e;
            }
            Err(e) => return Err(anyhow!("request failed: {e}")),
        }
    }
    Err(anyhow!("exhausted retries"))
}

/// Parse a gate reply: PASS or FAIL on the first non-empty line, rest is detail.
fn parse_verdict(reply: &str) -> (String, String) {
    let mut lines = reply.lines().filter(|l| !l.trim().is_empty());
    let first = lines.next().unwrap_or("").to_uppercase();
    let verdict = if first.contains("FAIL") {
        "FAIL"
    } else if first.contains("PASS") {
        "PASS"
    } else {
        "UNCLEAR"
    };
    let rest: String = reply
        .lines()
        .skip_while(|l| l.trim().is_empty())
        .skip(1)
        .collect::<Vec<_>>()
        .join(" ")
        .trim()
        .to_string();
    (verdict.to_string(), rest)
}

async fn sharpen(client: &reqwest::Client, key: &str, args: &Args, instrument: &str, bloated: &str) -> Result<String> {
    let p = format!("{instrument}\n\n---\n\n{TIGHTEN}\n\n---\n\n{bloated}");
    call(client, key, args, &p).await
}

async fn gate1(client: &reqwest::Client, key: &str, args: &Args, a: &str, b: &str) -> Result<(String, String)> {
    let p = format!(
        "You are comparing two prompts. Prompt A is the original; prompt B is a rewrite.\n\nWould any model, following B instead of A, ever behave differently on any input? Weigh dropped conditions, changed numbers, altered defaults, removed edge cases, and narrowed or widened scope.\n\nOn the first line write PASS if B preserves A's execution behavior exactly, or FAIL if it does not. If FAIL, on the next line name the single clearest divergence.\n\n--- PROMPT A ---\n{a}\n\n--- PROMPT B ---\n{b}"
    );
    Ok(parse_verdict(&call(client, key, args, &p).await?))
}

async fn gate2(client: &reqwest::Client, key: &str, args: &Args, checklist: &str, b: &str) -> Result<(String, String)> {
    let p = format!(
        "Below is a checklist of rules, then a prompt. List every checklist item the prompt violates, one per line. If it violates none, write 'none'.\n\nOn the first line write PASS if it violates nothing, or FAIL if it violates at least one.\n\n--- CHECKLIST ---\n{checklist}\n\n--- PROMPT ---\n{b}"
    );
    Ok(parse_verdict(&call(client, key, args, &p).await?))
}

#[cfg(test)]
mod tests {
    use super::normalize_dashes;

    #[test]
    fn frontmatter_and_rules_survive() {
        assert_eq!(normalize_dashes("---"), "---");
        assert_eq!(normalize_dashes("----"), "----");
        assert_eq!(normalize_dashes("  ---"), "  ---");
    }

    #[test]
    fn em_and_en_and_prose_double_dash() {
        assert_eq!(normalize_dashes("a\u{2014}b"), "a - b");
        assert_eq!(normalize_dashes("a \u{2014} b"), "a - b");
        assert_eq!(normalize_dashes("2013\u{2013}2014"), "2013-2014");
        assert_eq!(normalize_dashes("foo -- bar"), "foo - bar");
        assert_eq!(normalize_dashes("foo--bar"), "foo-bar");
    }

    #[test]
    fn single_hyphen_and_table_separator_untouched() {
        assert_eq!(normalize_dashes("well-formed"), "well-formed");
        assert_eq!(normalize_dashes("|---|---|"), "|---|---|");
    }

    #[test]
    fn code_is_protected() {
        // fenced block: em-dash left verbatim
        let fenced = "```\nx = a\u{2014}b\n```";
        assert_eq!(normalize_dashes(fenced), fenced);
        // inline code: CLI flag left verbatim, prose dash outside converted
        assert_eq!(
            normalize_dashes("run `--flag` now\u{2014}fast"),
            "run `--flag` now - fast"
        );
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    let args = Args::parse();
    let key = args
        .api_key
        .clone()
        .or_else(|| std::env::var("ANTHROPIC_API_KEY").ok())
        .ok_or_else(|| anyhow!("no API key"))?;

    let instrument = std::fs::read_to_string(&args.instrument)?;
    // The compliance gate uses the checklist section only.
    let checklist = instrument
        .split_once("## Checklist")
        .map(|(_, c)| format!("## Checklist{c}"))
        .unwrap_or_else(|| instrument.clone());

    let recs: Vec<InRec> = std::fs::read_to_string(&args.input)?
        .lines()
        .filter(|l| !l.trim().is_empty())
        .map(|l| serde_json::from_str(l).context("parse input record"))
        .collect::<Result<_>>()?;

    let client = reqwest::Client::builder().timeout(Duration::from_secs(600)).build()?;
    let mut out = std::fs::File::create(&args.out)?;
    use std::io::Write as _;

    let (mut pairs, mut g1_pass, mut g2_pass, mut kept) = (0, 0, 0, 0);
    let (mut controls, mut caught) = (0, 0);

    for r in &recs {
        let mut o = OutRec { kind: r.kind.clone(), source: r.source.clone(), ..Default::default() };
        if r.kind == "control" {
            controls += 1;
            o.control_a = r.a.clone();
            o.control_b = r.b.clone();
            o.corruption = r.corruption.clone();
            o.expected_fail = true;
            let (v, reason) = gate1(&client, &key, &args, &r.a, &r.b).await?;
            o.gate1 = v.clone();
            o.gate1_reason = reason;
            o.control_ok = v == "FAIL";
            if o.control_ok {
                caught += 1;
            }
            println!("control {}: gate1={} (want FAIL) [{}]  {}", r.source, v, if o.control_ok {"caught"} else {"MISSED"}, r.corruption);
        } else {
            pairs += 1;
            o.bloated = r.bloated.clone();
            let target = normalize_dashes(&sharpen(&client, &key, &args, &instrument, &r.bloated).await?);
            o.sharpened = target.clone();
            let (v1, r1) = gate1(&client, &key, &args, &r.bloated, &target).await?;
            o.gate1 = v1.clone();
            o.gate1_reason = r1;
            if v1 == "PASS" {
                g1_pass += 1;
                let (v2, r2) = gate2(&client, &key, &args, &checklist, &target).await?;
                o.gate2 = v2.clone();
                o.gate2_violations = r2;
                if v2 == "PASS" {
                    g2_pass += 1;
                }
            } else {
                o.gate2 = "SKIPPED".to_string();
            }
            o.kept = o.gate1 == "PASS" && o.gate2 == "PASS";
            if o.kept {
                kept += 1;
            }
            println!("pair {}: gate1={} gate2={} kept={}", r.source, o.gate1, o.gate2, o.kept);
        }
        writeln!(out, "{}", serde_json::to_string(&o)?)?;
    }

    out.flush()?;
    println!("\n=== SUMMARY ===");
    println!("pairs: {pairs} | gate1 PASS: {g1_pass} | gate2 PASS (of g1): {g2_pass} | kept: {kept}");
    println!("controls: {controls} | gate1 correctly FAILed: {caught}/{controls}");
    if controls > 0 && caught < controls {
        println!("WARNING: gate 1 missed {} corruption(s); it does not fully discriminate.", controls - caught);
    }
    Ok(())
}
