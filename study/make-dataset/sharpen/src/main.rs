// Sharpen: tighten a bloated prompt by applying the sharpening instrument,
// via a direct Anthropic API call with extended thinking. No Cursor harness,
// no system prompt, no injected context. The request carries only the
// instrument, the tighten instruction, and the bloated input.

use std::path::PathBuf;
use std::time::Duration;

use anyhow::{anyhow, Context, Result};
use clap::Parser;
use serde::{Deserialize, Serialize};

#[derive(Parser, Debug)]
#[command(about = "Tighten bloated prompts with the sharpening instrument via Opus + max thinking")]
struct Args {
    /// The sharpening instrument (the distilled rule-list)
    #[arg(long, default_value = "sharpen-instrument.md")]
    instrument: PathBuf,

    /// Input .md file, or a directory of .md files, to tighten
    #[arg(long)]
    input: PathBuf,

    /// Output directory for sharpened files
    #[arg(long, default_value = "sharpen-out")]
    out: PathBuf,

    /// Model id
    #[arg(long, default_value = "claude-opus-4-8")]
    model: String,

    /// Thinking effort level (controls reasoning depth): low, medium, high
    #[arg(long, default_value = "high")]
    effort: String,

    /// Max output tokens
    #[arg(long, default_value_t = 32000)]
    max_tokens: u32,

    /// Anthropic API key; falls back to ANTHROPIC_API_KEY
    #[arg(long)]
    api_key: Option<String>,
}

// The tighten instruction. Deliberately spare: apply the rules, preserve
// meaning, output only the result. No "improve", which would pull toward the
// verbose mean; tightening is disambiguate-plus-cut-dead-weight.
const TIGHTEN: &str = "Above is a set of rules for tightening a prompt. Apply every applicable rule to the prompt below. Make it unambiguous and cut dead weight. Preserve exactly the meaning an executing model would follow: every instruction, condition, number, name, and defined behavior. Do not add, explain, or improve; only tighten. Output only the tightened prompt, with no preamble and no commentary.";

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
    content: Vec<Block>,
}

#[derive(Deserialize)]
struct Block {
    #[serde(rename = "type")]
    kind: String,
    #[serde(default)]
    text: String,
}

fn words(s: &str) -> usize {
    s.split_whitespace().count()
}

async fn sharpen_one(
    client: &reqwest::Client,
    key: &str,
    args: &Args,
    instrument: &str,
    bloated: &str,
) -> Result<String> {
    let prompt = format!("{instrument}\n\n---\n\n{TIGHTEN}\n\n---\n\n{bloated}");
    let body = ApiRequest {
        model: args.model.clone(),
        max_tokens: args.max_tokens,
        thinking: Thinking { kind: "adaptive".to_string() },
        output_config: OutputConfig { effort: args.effort.clone() },
        messages: vec![Msg { role: "user".to_string(), content: prompt }],
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
                // Take only text blocks; thinking blocks are dropped.
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
                    eprintln!("  {s} attempt {attempt}, backoff {backoff:?}");
                    tokio::time::sleep(backoff).await;
                    backoff *= 2;
                    continue;
                }
                return Err(anyhow!("API error {s}: {detail}"));
            }
            Err(e) if attempt < 4 => {
                eprintln!("  request error attempt {attempt}: {e}");
                tokio::time::sleep(backoff).await;
                backoff *= 2;
            }
            Err(e) => return Err(anyhow!("request failed: {e}")),
        }
    }
    Err(anyhow!("exhausted retries"))
}

#[tokio::main]
async fn main() -> Result<()> {
    let args = Args::parse();
    let key = args
        .api_key
        .clone()
        .or_else(|| std::env::var("ANTHROPIC_API_KEY").ok())
        .ok_or_else(|| anyhow!("no API key: pass --api-key or set ANTHROPIC_API_KEY"))?;

    let instrument = std::fs::read_to_string(&args.instrument)
        .with_context(|| format!("read instrument {}", args.instrument.display()))?;

    let mut inputs: Vec<PathBuf> = Vec::new();
    if args.input.is_dir() {
        for e in std::fs::read_dir(&args.input)? {
            let p = e?.path();
            if p.extension().and_then(|s| s.to_str()) == Some("md") {
                inputs.push(p);
            }
        }
    } else {
        inputs.push(args.input.clone());
    }
    inputs.sort();

    std::fs::create_dir_all(&args.out)?;
    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(600))
        .build()?;

    println!(
        "Model {}, thinking adaptive, effort {}, {} input(s).\n",
        args.model, args.effort, inputs.len()
    );

    for path in &inputs {
        let name = path.file_name().unwrap().to_string_lossy().to_string();
        let bloated = std::fs::read_to_string(path)?;
        print!("{name}: {} words -> ", words(&bloated));
        use std::io::Write as _;
        std::io::stdout().flush().ok();
        let sharp = sharpen_one(&client, &key, &args, &instrument, &bloated).await?;
        println!("{} words", words(&sharp));
        std::fs::write(args.out.join(&name), &sharp)?;
    }

    println!("\nWrote sharpened files to {}", args.out.display());
    Ok(())
}
