#!/usr/bin/env python3
"""Fortune Cookie for an AI Agent — one funny fortune line for an AI agent.

Writes one fortune-cookie line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Standard library only. Deterministic: the same
bytes on every run, so the two grading runs agree.

Version history:
  v1 — initial line plus gate self-check (single line, 1-140 chars,
       not only whitespace, no control characters).
  v2 — added round-trip verification: after writing, the file is read
       back and must match the line byte for byte.
"""

import os
import sys

LINE = "Your lucky numbers are 404, 429, and the token limit you just hit."

MAX_CHARS = 140


def main() -> int:
    text = LINE.strip()
    # Gate self-check: single line, 1-140 chars, not only whitespace.
    if not text:
        print("error: entry is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print("error: entry is %d chars, over %d" % (len(text), MAX_CHARS),
              file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 for ch in text):
        print("error: entry holds a control character", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # Round-trip verification: the file must read back byte for byte.
    with open(path, "rb") as f:
        if f.read().decode("utf-8") != text:
            print("error: entry.txt does not match the line", file=sys.stderr)
            return 1
    print("wrote %d chars to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
