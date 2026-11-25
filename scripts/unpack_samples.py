#!/usr/bin/env python3
"""Unpack clinic preview PDFs from base64 jsonl shards (used only to land binary files via text-only MCP)."""
from pathlib import Path
import base64, json, sys

root = Path(__file__).resolve().parents[1]
payloads = root / "samples" / "_payloads"
dest = root / "samples"
if not payloads.is_dir():
    print("no payloads dir; nothing to do")
    sys.exit(0)

written = 0
for part in sorted(payloads.glob("part*.jsonl")):
    for line in part.read_text(encoding="ascii").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        name = rec["name"]
        if "/" in name or "\\" in name or name.startswith("."):
            raise SystemExit(f"refusing unsafe name {name!r}")
        if not name.endswith(".pdf"):
            raise SystemExit(f"refusing non-pdf {name!r}")
        out = dest / name
        out.write_bytes(base64.b64decode(rec["b64"]))
        written += 1
        print("wrote", out.name, out.stat().st_size)
print("wrote", written, "pdfs")
