#!/usr/bin/env python3
"""Museum of the Year 3000 - one museum label, written to entry.txt.

The entry is a single fixed line: the deadpan label a museum in the year
3000 puts beside a selfie stick. The program writes it to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt) as UTF-8 with no
trailing newline, then reads the file back and checks the competition gate
(1-200 characters, exactly one line, not only whitespace) against the bytes
actually on disk.
"""

import os
import sys
from pathlib import Path

LABEL = "Selfie stick, c. 2023. An extendable arm that let a human photograph themself from the distance of a stranger, so the picture could pretend they had friends."

MAX_CHARS = 200


def gate(text):
    """Return a list of gate failures for `text` (empty list means it passes)."""
    problems = []
    if not text:
        problems.append("empty")
    if len(text) > MAX_CHARS:
        problems.append(f"{len(text)} chars exceeds {MAX_CHARS}")
    if text.strip() == "":
        problems.append("only whitespace")
    if text.splitlines() != [text]:
        problems.append("not exactly one line")
    return problems


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    problems = gate(LABEL)
    if problems:
        print("label fails the gate:", "; ".join(problems), file=sys.stderr)
        return 1
    target.write_bytes(LABEL.encode("utf-8"))
    on_disk = target.read_bytes().decode("utf-8")
    if on_disk != LABEL:
        print("round-trip mismatch", file=sys.stderr)
        return 1
    problems = gate(on_disk)
    if problems:
        print("written file fails the gate:", "; ".join(problems), file=sys.stderr)
        return 1
    print(f"{LABEL} ({len(LABEL)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
