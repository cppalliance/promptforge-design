"""Build catalog.jsonl (id-indexed) from the automatelab tool parquet.

Source parquet is copied from the earlier spike (automatelab/mcp-servers-tool-catalog:
9,922 real MCP tools with name, description, input schema). One line per usable tool.
"""

from __future__ import annotations

import json

import pandas as pd

from common import DATA

SRC = DATA.parent.parent / "spike-tool-picker" / "data" / "automatelab_tools.parquet"


def main():
    df = pd.read_parquet(SRC)
    out = DATA / "catalog.jsonl"
    n = 0
    with out.open("w", encoding="utf-8") as f:
        for _, r in df.iterrows():
            name = str(r["tool_name"]).strip()
            desc = str(r["tool_description"]).strip()
            server = str(r["server_name"]).strip()
            if not name or not desc or desc == "None":
                continue
            params = []
            try:
                sch = json.loads(r["input_schema"]) if isinstance(r["input_schema"], str) else r["input_schema"]
                params = list((sch or {}).get("properties", {}).keys())[:8]
            except Exception:  # noqa: BLE001
                pass
            f.write(json.dumps({"id": n, "server": server, "name": name, "description": desc, "params": params}) + "\n")
            n += 1
    print(f"catalog.jsonl: {n} tools")


if __name__ == "__main__":
    main()
