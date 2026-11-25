#!/usr/bin/env python3
"""Make the AI Judge Laugh (make.fun bounty u-rama-melon-make-the-ai-judge-laugh-302d0825).

Writes one one-line joke about office life to /output/entry.txt.

Judge brief, in order: (1) on subject, a joke about office life;
(2) true to the office; (3) surprising turn; (4) tight, one line,
no wasted setup; (5) original, not a stock line with nouns swapped.

Why this joke: "bring your whole self to work" is real HR language
every office worker has heard in a wellness deck. The setup sounds
like compliance; the turn reframes it literally — the resignation
letter is the "whole self" that finally gets read. Concrete scene,
punch in the last words, no Monday/printer/coffee stock joke, and
nothing our earlier office entries used (reply-all thread; IT
monitor answered with a gratitude workshop).

Rejected alternatives: a meeting to discuss declining meetings
(recursive, but the punch lands mid-line, not at the end); flexible
hours letting you be exhausted any time you choose (tight, but the
turn is a shrug, not a surprise).

Deterministic: fixed string, stdlib only, no network, no randomness.
Both runs write byte-identical output.

Revision (reviser, 25 Nov 2026): gate validation moved into a
standalone validate_entry() helper so the rules are testable in
isolation; the writer now rejects control characters and writes
atomically (tempfile in the output dir + fsync + os.replace) so a
crash can never leave a half-written entry.txt. Entry text itself
is unchanged.

  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import tempfile
import unicodedata

JOKE = (
    "HR said to bring my whole self to work, so I brought my "
    "resignation letter too \u2014 it was the only part of me "
    "they ever read."
)


def validate_entry(entry: str) -> str:
    """Gate: UTF-8 text of 1-200 characters, not only whitespace,
    exactly one line, and free of control characters. Returns the
    entry unchanged on success; raises ValueError otherwise so a
    bad entry fails loudly instead of writing something the gate
    would refuse."""
    if not 1 <= len(entry) <= 200:
        raise ValueError(f"entry is {len(entry)} characters, must be 1-200")
    if not any(not ch.isspace() for ch in entry):
        raise ValueError("entry must contain a non-whitespace character")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    bad = [
        ch
        for ch in entry
        if unicodedata.category(ch) in ("Cc", "Cf")
        or ch in ("\u007f", "\ufeff")
    ]
    if bad:
        raise ValueError(
            "entry contains control characters: "
            + ", ".join(f"U+{ord(ch):04X}" for ch in bad)
        )
    return entry


def write_entry(entry: str, out_dir: str) -> str:
    """Write entry atomically to <out_dir>/entry.txt: tempfile in
    the same directory, fsync, then os.replace, so readers never
    see a partial file. No trailing newline. Returns the path."""
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp_path = tempfile.mkstemp(
        dir=out_dir, prefix=".entry.", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(entry)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    return target


def main() -> None:
    entry = validate_entry(JOKE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(entry, out_dir)


if __name__ == "__main__":
    main()
