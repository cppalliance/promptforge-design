"""Shared types and IO for the MCP tool-picker study.

Compact, id-referenced representation - never per-case catalog files:
  - catalog.jsonl : one line per tool, with a stable integer `id`.
  - needs.jsonl   : one line per eval case, referencing tools by id only.
  - embeddings/catalog_<model>.npy : cached catalog vectors keyed by catalog hash.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
EMB = ROOT / "embeddings"


@dataclass
class Tool:
    id: int
    server: str
    name: str
    description: str
    params: list[str] = field(default_factory=list)

    @property
    def qualified(self) -> str:
        return f"{self.server}::{self.name}"

    def enriched_text(self) -> str:
        parts = [self.name.replace("_", " "), self.description]
        if self.params:
            parts.append("parameters: " + ", ".join(self.params))
        return ". ".join(p for p in parts if p)


def load_catalog(path: Path | None = None) -> list[Tool]:
    path = path or (DATA / "catalog.jsonl")
    out = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(Tool(**json.loads(line)))
    return out


def catalog_hash(tools: list[Tool]) -> str:
    h = hashlib.sha256()
    for t in tools:
        h.update(t.enriched_text().encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()[:16]


def load_needs(path: Path | None = None) -> list[dict]:
    path = path or (DATA / "needs.jsonl")
    out = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out
