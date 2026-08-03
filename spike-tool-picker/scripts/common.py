"""Shared types and IO for the MCP tool-selection classifier spike.

A *catalog* is a list of tools drawn from one or more MCP servers. Each tool
carries the fields a real `tools/list` response provides: the server it came
from, its name, a human description, and the parameter names from its input
schema.

An *eval example* is a natural-language capability need plus the gold tool it
should resolve to within a named catalog. `gold is None` marks a hard negative:
the need matches no tool in the catalog and the correct behavior is to abstain.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parent.parent
DATA = SPIKE_ROOT / "data"
CATALOGS_DIR = DATA / "mcp_catalogs"
EVAL_DIR = DATA / "eval"
RESULTS_DIR = SPIKE_ROOT / "results"


@dataclass
class Tool:
    server: str
    name: str
    description: str
    params: list[str] = field(default_factory=list)

    @property
    def qualified(self) -> str:
        return f"{self.server}::{self.name}"

    def enriched_text(self) -> str:
        """Tool text for matching: name + description + parameter names.

        Parameter names are appended because tool descriptions are terse and
        the TDWA/Tool2Vec findings show name+params materially help retrieval.
        """
        parts = [self.name.replace("_", " "), self.description]
        if self.params:
            parts.append("parameters: " + ", ".join(self.params))
        return ". ".join(p for p in parts if p)


@dataclass
class Catalog:
    catalog_id: str
    tools: list[Tool]

    def tool_by_qualified(self, q: str) -> Tool | None:
        for t in self.tools:
            if t.qualified == q:
                return t
        return None


@dataclass
class EvalExample:
    need: str
    catalog_id: str
    gold: str | None  # qualified tool name, or None for hard negatives
    tags: list[str] = field(default_factory=list)


def save_catalog(cat: Catalog, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"catalog_id": cat.catalog_id, "tools": [asdict(t) for t in cat.tools]}, indent=2),
        encoding="utf-8",
    )


def load_catalog(path: Path) -> Catalog:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return Catalog(
        catalog_id=raw["catalog_id"],
        tools=[Tool(**t) for t in raw["tools"]],
    )


def load_all_catalogs() -> dict[str, Catalog]:
    cats: dict[str, Catalog] = {}
    for p in sorted(CATALOGS_DIR.glob("*.json")):
        cat = load_catalog(p)
        cats[cat.catalog_id] = cat
    return cats


def save_eval(examples: list[EvalExample], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(asdict(ex)) + "\n")


def load_eval(path: Path) -> list[EvalExample]:
    out: list[EvalExample] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(EvalExample(**json.loads(line)))
    return out
