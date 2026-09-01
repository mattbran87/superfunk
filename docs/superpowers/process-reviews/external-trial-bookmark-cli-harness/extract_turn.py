"""Dump every assistant *text* block written to the child session transcript
after a given line offset. `claude -p` prints only the final message, which
made earlier turns look like they dropped user questions when the answer was
in fact in an earlier (unprinted) assistant message.

Usage: python extract_turn.py <jsonl> <start_line> [--count]
"""
import io
import json
import sys

path = sys.argv[1]
start = int(sys.argv[2])

if "--count" in sys.argv:
    n = sum(1 for _ in io.open(path, encoding="utf-8", errors="replace"))
    print(n)
    sys.exit(0)

blocks = []
for idx, line in enumerate(io.open(path, encoding="utf-8", errors="replace"), 1):
    if idx <= start:
        continue
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get("type") != "assistant":
        continue
    # skip subagent output: those carry a parent tool use id
    if o.get("parentUuid") and o.get("isSidechain"):
        continue
    content = o.get("message", {}).get("content", [])
    if not isinstance(content, list):
        continue
    for b in content:
        if b.get("type") == "text":
            t = b.get("text", "").strip()
            if t:
                blocks.append((idx, t))

for i, t in blocks:
    print(f"\n----- assistant message @line {i} -----")
    print(t)
