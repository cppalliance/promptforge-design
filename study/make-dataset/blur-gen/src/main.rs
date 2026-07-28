// Blur dataset generator.
//
// Reads a markdown file, splits it into sections, and blurs each section
// through N chained passes of the Anthropic API, rotating models. Each pass
// output is written as a training pair mapping back to the sharp original.
// The blur is the training signal: a model asked to "rewrite" resamples
// toward the mean, expanding and hedging without being told to.

use std::io::Write as _;
use std::path::PathBuf;
use std::time::Duration;

use anyhow::{anyhow, Context, Result};
use clap::Parser;
use serde::{Deserialize, Serialize};

#[derive(Parser, Debug)]
#[command(about = "Generate a blur training dataset from a markdown file")]
struct Args {
    /// Input markdown file
    #[arg(long)]
    input: PathBuf,

    /// Output JSONL file
    #[arg(long, default_value = "dataset.jsonl")]
    output: PathBuf,

    /// Number of chained blur passes (each takes the previous pass as input)
    #[arg(long, default_value_t = 10)]
    passes: usize,

    /// Independent blur runs per source section, giving diverse blur paths
    #[arg(long, default_value_t = 2)]
    variants: usize,

    /// Comma-separated Anthropic model IDs to rotate through, one per pass
    #[arg(
        long,
        default_value = "claude-sonnet-4-20250514,claude-3-5-haiku-20241022,claude-opus-4-20250514"
    )]
    models: String,

    /// Anthropic API key; falls back to ANTHROPIC_API_KEY env var
    #[arg(long)]
    api_key: Option<String>,

    /// Milliseconds to wait between API calls
    #[arg(long, default_value_t = 1000)]
    delay_ms: u64,

    /// Max output tokens per API call
    #[arg(long, default_value_t = 4096)]
    max_tokens: u32,
}

const BLUR_PROMPT: &str = "Rewrite the following text. Preserve all meaning.";

/// One training pair: a blurred rendering mapped back to the sharp original.
#[derive(Serialize)]
struct Pair {
    original: String,
    blurred: String,
    pass: usize,
    variant: usize,
    model: String,
    source: String,
    original_words: usize,
    blurred_words: usize,
}

// --- Anthropic Messages API types ---

#[derive(Serialize)]
struct ApiRequest {
    model: String,
    max_tokens: u32,
    messages: Vec<ApiMessage>,
}

#[derive(Serialize)]
struct ApiMessage {
    role: String,
    content: String,
}

#[derive(Deserialize)]
struct ApiResponse {
    content: Vec<ContentBlock>,
}

#[derive(Deserialize)]
struct ContentBlock {
    #[serde(default)]
    text: String,
}

fn word_count(s: &str) -> usize {
    s.split_whitespace().count()
}

/// Split markdown at H2/H3 headings. A section is the heading line plus the
/// body up to the next heading. When the file has no such headings, the whole
/// file is one section. Blank-only sections are dropped.
fn split_sections(text: &str) -> Vec<String> {
    let is_heading = |line: &str| {
        let t = line.trim_start();
        t.starts_with("## ") || t.starts_with("### ")
    };

    if !text.lines().any(is_heading) {
        let trimmed = text.trim();
        return if trimmed.is_empty() {
            vec![]
        } else {
            vec![trimmed.to_string()]
        };
    }

    let mut sections = Vec::new();
    let mut current = String::new();
    for line in text.lines() {
        if is_heading(line) && !current.trim().is_empty() {
            sections.push(current.trim().to_string());
            current.clear();
        }
        current.push_str(line);
        current.push('\n');
    }
    if !current.trim().is_empty() {
        sections.push(current.trim().to_string());
    }
    sections
}

/// One Anthropic Messages API call with retry on 429 and 5xx.
async fn call_api(
    client: &reqwest::Client,
    api_key: &str,
    model: &str,
    max_tokens: u32,
    text: &str,
) -> Result<String> {
    let body = ApiRequest {
        model: model.to_string(),
        max_tokens,
        messages: vec![ApiMessage {
            role: "user".to_string(),
            content: format!("{BLUR_PROMPT}\n\n{text}"),
        }],
    };

    let mut backoff = Duration::from_secs(2);
    for attempt in 1..=5 {
        let resp = client
            .post("https://api.anthropic.com/v1/messages")
            .header("x-api-key", api_key)
            .header("anthropic-version", "2023-06-01")
            .header("content-type", "application/json")
            .json(&body)
            .send()
            .await;

        match resp {
            Ok(r) if r.status().is_success() => {
                let parsed: ApiResponse = r.json().await.context("parse API response")?;
                let text = parsed
                    .content
                    .into_iter()
                    .map(|b| b.text)
                    .collect::<Vec<_>>()
                    .join("");
                if text.trim().is_empty() {
                    return Err(anyhow!("empty completion from {model}"));
                }
                return Ok(text.trim().to_string());
            }
            Ok(r) => {
                let status = r.status();
                let detail = r.text().await.unwrap_or_default();
                let retriable = status.as_u16() == 429 || status.is_server_error();
                if retriable && attempt < 5 {
                    eprintln!("  {status} on attempt {attempt}, backing off {backoff:?}");
                    tokio::time::sleep(backoff).await;
                    backoff *= 2;
                    continue;
                }
                return Err(anyhow!("API error {status}: {detail}"));
            }
            Err(e) if attempt < 5 => {
                eprintln!("  request error on attempt {attempt}: {e}, backing off {backoff:?}");
                tokio::time::sleep(backoff).await;
                backoff *= 2;
            }
            Err(e) => return Err(anyhow!("request failed: {e}")),
        }
    }
    Err(anyhow!("exhausted retries for {model}"))
}

#[tokio::main]
async fn main() -> Result<()> {
    let args = Args::parse();

    let api_key = args
        .api_key
        .clone()
        .or_else(|| std::env::var("ANTHROPIC_API_KEY").ok())
        .ok_or_else(|| anyhow!("no API key: pass --api-key or set ANTHROPIC_API_KEY"))?;

    let models: Vec<String> = args
        .models
        .split(',')
        .map(|s| s.trim().to_string())
        .filter(|s| !s.is_empty())
        .collect();
    if models.is_empty() {
        return Err(anyhow!("no models given"));
    }

    let source_name = args
        .input
        .file_name()
        .map(|s| s.to_string_lossy().to_string())
        .unwrap_or_else(|| "input".to_string());

    let text = std::fs::read_to_string(&args.input)
        .with_context(|| format!("read {}", args.input.display()))?;
    let sections = split_sections(&text);
    if sections.is_empty() {
        return Err(anyhow!("no non-empty sections in input"));
    }
    println!(
        "Split {source_name} into {} section(s). {} passes, {} variants, {} model(s).",
        sections.len(),
        args.passes,
        args.variants,
        models.len()
    );

    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(120))
        .build()?;

    let mut out = std::fs::File::create(&args.output)
        .with_context(|| format!("create {}", args.output.display()))?;
    let mut pairs_written = 0usize;

    for (si, original) in sections.iter().enumerate() {
        let orig_words = word_count(original);
        for variant in 1..=args.variants {
            // Chain: each pass blurs the previous pass's output.
            let mut current = original.clone();
            for pass in 1..=args.passes {
                let model = &models[(pass - 1) % models.len()];
                println!(
                    "section {}/{}, variant {}/{}, pass {}/{}, model {model}",
                    si + 1,
                    sections.len(),
                    variant,
                    args.variants,
                    pass,
                    args.passes
                );
                let blurred =
                    call_api(&client, &api_key, model, args.max_tokens, &current).await?;
                let bw = word_count(&blurred);
                println!("  {} -> {} words", word_count(&current), bw);

                let pair = Pair {
                    original: original.clone(),
                    blurred: blurred.clone(),
                    pass,
                    variant,
                    model: model.clone(),
                    source: source_name.clone(),
                    original_words: orig_words,
                    blurred_words: bw,
                };
                writeln!(out, "{}", serde_json::to_string(&pair)?)?;
                pairs_written += 1;

                current = blurred;
                tokio::time::sleep(Duration::from_millis(args.delay_ms)).await;
            }
        }
    }

    out.flush()?;
    println!(
        "Wrote {pairs_written} pairs to {}",
        args.output.display()
    );
    Ok(())
}
