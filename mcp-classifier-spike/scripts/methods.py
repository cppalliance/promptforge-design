"""Scoring methods for tool selection.

Every method implements `score(need, tools) -> list[float]`, one score per tool
in order, higher = better match. The eval harness turns scores into a ranking
and an accept/abstain decision by thresholding, so methods only need to produce
comparable scores within a single (need, catalog) call.

Methods:
  - NLIScorer: zero-shot entailment. premise=need, hypothesis=tool text.
    Uses the MNLI entailment probability as the relevance score. This is the
    candidate the whole spike exists to evaluate.
  - EmbeddingScorer: bi-encoder cosine similarity (sentence-transformers).
  - BM25Scorer: lexical baseline (rank_bm25).
  - LLMScorer: optional upper-bound; asks an OpenAI-compatible chat model to
    pick the best tool. Only runs if an API key is configured.
"""

from __future__ import annotations

import os
import re
from functools import lru_cache

from common import Tool


def auto_device() -> str:
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:  # noqa: BLE001
        return "cpu"


def _apply_thread_cap() -> None:
    """Cap torch threads so several model processes can run concurrently.

    Set SPIKE_THREADS to bound intra-op parallelism per process; with N parallel
    processes keep N*SPIKE_THREADS <= physical cores to avoid oversubscription.
    """
    n = os.environ.get("SPIKE_THREADS")
    if n:
        try:
            import torch

            torch.set_num_threads(int(n))
        except Exception:  # noqa: BLE001
            pass


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _tool_text(t: Tool, mode: str) -> str:
    if mode == "name":
        return t.name.replace("_", " ")
    if mode == "description":
        return t.description
    if mode == "name_desc":
        return f"{t.name.replace('_', ' ')}: {t.description}"
    return t.enriched_text()  # "enriched"


class NLIScorer:
    """Zero-shot NLI relevance scorer, with configurable framing.

    NLI is directional and sensitive to phrasing, so the framing is a first-class
    knob, not a detail:
      - direction "need_premise": premise=need, hypothesis=template.format(tool=<tool text>)
      - direction "tool_premise": premise=<tool text>, hypothesis=template.format(need=need)
    tool_field selects how much of the tool goes into the string (name / description
    / name_desc / enriched). The score is the entailment probability.
    """

    def __init__(
        self,
        model_id: str,
        template: str,
        direction: str = "need_premise",
        tool_field: str = "description",
        device: str | None = None,
        max_length: int = 256,
    ):
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        self.model_id = model_id
        self.template = template
        self.direction = direction
        self.tool_field = tool_field
        self.max_length = max_length
        self.torch = torch
        _apply_thread_cap()
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_id)
        self.model.eval()
        self.device = device or auto_device()
        self.model.to(self.device)
        self.batch = 128 if self.device == "cuda" else 16

        label2id = {k.lower(): v for k, v in (self.model.config.label2id or {}).items()}
        if "entailment" in label2id:
            self.entail_idx = label2id["entailment"]
        else:
            self.entail_idx = self.model.config.num_labels - 1

    def _pair(self, need: str, tool: Tool) -> tuple[str, str]:
        tt = _tool_text(tool, self.tool_field)
        if self.direction == "tool_premise":
            return tt, self.template.format(need=need)
        return need, self.template.format(tool=tt)

    def score(self, need: str, tools: list[Tool]) -> list[float]:
        torch = self.torch
        pairs = [self._pair(need, t) for t in tools]
        premises = [p for p, _ in pairs]
        hypotheses = [h for _, h in pairs]
        scores: list[float] = []
        batch = self.batch
        with torch.no_grad():
            for i in range(0, len(tools), batch):
                enc = self.tokenizer(
                    premises[i : i + batch],
                    hypotheses[i : i + batch],
                    return_tensors="pt",
                    truncation=True,
                    max_length=self.max_length,
                    padding=True,
                ).to(self.device)
                logits = self.model(**enc).logits
                probs = torch.softmax(logits, dim=-1)[:, self.entail_idx]
                scores.extend(probs.cpu().tolist())
        return scores


class EmbeddingScorer:
    def __init__(self, model_id: str, device: str | None = None):
        from sentence_transformers import SentenceTransformer

        self.model_id = model_id
        try:
            self.model = SentenceTransformer(model_id, device=device or auto_device(), trust_remote_code=True)
        except TypeError:
            self.model = SentenceTransformer(model_id, device=device or auto_device())

    def score(self, need: str, tools: list[Tool]) -> list[float]:
        from sentence_transformers import util

        tool_texts = [t.enriched_text() for t in tools]
        q = self.model.encode(need, convert_to_tensor=True, normalize_embeddings=True)
        d = self.model.encode(tool_texts, convert_to_tensor=True, normalize_embeddings=True)
        sims = util.cos_sim(q, d)[0]
        return sims.cpu().tolist()


class CrossEncoderScorer:
    """Cross-encoder reranker: scores (need, tool) jointly for relevance.

    Unlike a bi-encoder, the query and tool are encoded together so they interact,
    which is more accurate at the cost of one model call per candidate. Over our
    small catalogs we score every tool directly (the accuracy ceiling); in
    production this would run only over an embedding-retrieved top-k.
    """

    def __init__(self, model_id: str, device: str | None = None):
        from sentence_transformers import CrossEncoder

        self.model_id = model_id
        self.device = device or auto_device()
        self.model = CrossEncoder(model_id, device=self.device, max_length=512)

    def score(self, need: str, tools: list[Tool]) -> list[float]:
        pairs = [[need, t.enriched_text()] for t in tools]
        scores = self.model.predict(pairs, convert_to_numpy=True, show_progress_bar=False)
        return [float(s) for s in scores]


class BM25Scorer:
    model_id = "bm25"

    def score(self, need: str, tools: list[Tool]) -> list[float]:
        from rank_bm25 import BM25Okapi

        corpus = [_tokenize(t.enriched_text()) for t in tools]
        bm25 = BM25Okapi(corpus)
        return list(bm25.get_scores(_tokenize(need)))


class LLMScorer:
    """Optional upper-bound. Picks the best tool via an OpenAI-compatible chat API.

    Enabled only when an API key is present. Returns 1.0 for the chosen tool and
    0.0 for the rest (plus a small confidence read from the model when possible).
    """

    def __init__(self, model: str | None = None):
        self.base_url = os.environ.get("SPIKE_LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1"
        self.api_key = os.environ.get("SPIKE_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
        self.model = model or os.environ.get("SPIKE_LLM_MODEL") or "gpt-4o-mini"
        self.model_id = f"llm:{self.model}"

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def score(self, need: str, tools: list[Tool]) -> list[float]:
        import json as _json
        import urllib.request

        listing = "\n".join(f"{i}. {t.name}: {t.description}" for i, t in enumerate(tools))
        prompt = (
            "You match a capability need to the single best tool.\n"
            f"Need: {need}\n\nTools:\n{listing}\n\n"
            "Reply with a JSON object {\"index\": <int or -1 if none fit>, "
            "\"confidence\": <0..1>}. -1 means no tool fits."
        )
        body = _json.dumps(
            {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "response_format": {"type": "json_object"},
            }
        ).encode()
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=body,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
        )
        scores = [0.0] * len(tools)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = _json.loads(resp.read())
            content = data["choices"][0]["message"]["content"]
            parsed = _json.loads(content)
            idx = int(parsed.get("index", -1))
            conf = float(parsed.get("confidence", 1.0))
            if 0 <= idx < len(tools):
                scores[idx] = conf
        except Exception as e:  # noqa: BLE001 - spike; log and continue
            print(f"  [LLMScorer] call failed: {e}")
        return scores


class AnthropicLLMScorer:
    """LLM upper-bound baseline using the Anthropic Messages API.

    Asks the model to pick the single best tool (or -1 for none) and returns a
    one-hot-ish score vector (chosen index gets the model's confidence). Used to
    bound how much accuracy a full generative reader buys over NLI.
    """

    def __init__(self, model: str | None = None):
        self.model = model or os.environ.get("SPIKE_LLM_MODEL") or "claude-haiku-4-5"
        self.model_id = f"anthropic:{self.model}"
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def score(self, need: str, tools: list[Tool]) -> list[float]:
        import json as _json
        import time as _time
        import urllib.request

        listing = "\n".join(f"{i}. {t.name}: {t.description}" for i, t in enumerate(tools))
        prompt = (
            "Pick the single tool that best satisfies the user's need. "
            "If none fit, use -1.\n"
            f"Need: {need}\n\nTools:\n{listing}\n\n"
            'Reply ONLY with JSON: {"index": <int>, "confidence": <0..1>}.'
        )
        body = _json.dumps(
            {"model": self.model, "max_tokens": 60, "messages": [{"role": "user", "content": prompt}]}
        ).encode()
        scores = [0.0] * len(tools)
        for attempt in range(3):
            try:
                req = urllib.request.Request(
                    "https://api.anthropic.com/v1/messages",
                    data=body,
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = _json.loads(resp.read())
                text = "".join(b.get("text", "") for b in data.get("content", []))
                parsed = _json.loads(text[text.find("{") : text.rfind("}") + 1])
                idx = int(parsed.get("index", -1))
                conf = float(parsed.get("confidence", 1.0))
                if 0 <= idx < len(tools):
                    scores[idx] = conf
                return scores
            except Exception:  # noqa: BLE001
                _time.sleep(1.5 * (attempt + 1))
        return scores


HYPOTHESIS_TEMPLATES = {
    "capability": "This request requires a tool that can {tool}",
    "usage": "The user needs to use {tool}",
    "example": "This example is about using a tool: {tool}",
}

# Named NLI framings. The framing sweep showed direction dominates: putting the
# tool text in the premise and the need in the hypothesis ("does this tool entail
# that it can do X") far outperforms the reverse. `best` is the sweep winner.
NLI_CONFIGS = {
    "best": {"template": "This tool can be used to {need}", "direction": "tool_premise", "tool_field": "name_desc"},
    "best_desc": {"template": "This tool can be used to {need}", "direction": "tool_premise", "tool_field": "description"},
    "usefulto": {"template": "This is useful to {need}", "direction": "tool_premise", "tool_field": "name_desc"},
    "naive": {"template": "This request requires a tool that can {tool}", "direction": "need_premise", "tool_field": "enriched"},
}


@lru_cache(maxsize=None)
def _cached_note() -> str:
    return "methods module loaded"
