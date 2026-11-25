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

  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

JOKE = (
    "HR said to bring my whole self to work, so I brought my "
    "resignation letter too \u2014 it was the only part of me "
    "they ever read."
)


def _validate(joke: str) -> None:
    """Gate: UTF-8 text of 1-200 characters, not only whitespace,
    exactly one line. Fail loudly instead of writing an entry
    the gate would refuse."""
    if not 1 <= len(joke) <= 200:
        raise SystemExit(f"joke is {len(joke)} characters, must be 1-200")
    if not any(not ch.isspace() for ch in joke):
        raise SystemExit("joke must contain a non-whitespace character")
    if "\n" in joke or "\r" in joke:
        raise SystemExit("joke must be a single line")


def main() -> None:
    _validate(JOKE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(JOKE)


if __name__ == "__main__":
    main()
