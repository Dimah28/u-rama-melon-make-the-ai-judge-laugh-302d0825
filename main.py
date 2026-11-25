#!/usr/bin/env python3
"""Make the AI Judge Laugh (make.fun bounty u-rama-melon-make-the-ai-judge-laugh-302d0825).

Writes one one-line joke about office life to /output/entry.txt.

Judge brief, in order: (1) on subject, a joke about office life;
(2) true to the office; (3) surprising turn; (4) tight, one line,
no wasted setup; (5) original, not a stock line with nouns swapped.

Why this joke (chosen draft A, 161 characters): Finance caps a
client dinner at $40; the speaker splits one $240 dinner into six
$40 receipts; audit approves all six and flags the $3.80 coffee
for missing approval. One mechanism, three beats — rigid rule,
literal evasion, cover-up that backfires in the system's favour —
adapted from the joke-demo winners (rule in AGENTS.md, agent
removes the line, does the forbidden thing, puts the line back),
but with an office scene of its own: expense caps, receipt
splitting, and an audit that rubber-stamps the fraud while
punishing the one honest item. The twist lands in the last words
("flagged my $3.80 coffee"), the numbers are specific ($40 /
$240 / six / $3.80), and the observation is true: expense
systems really do catch trivial items and miss structured ones.
No Monday/printer/coffee stock joke, nothing our earlier office
entries used (reply-all thread; IT monitor answered with a
gratitude workshop; HR "whole self" resignation letter).

Rejected alternatives:
- Draft B (149 chars): "IT banned passwords on sticky notes, so
  I wrote mine on 14 Post-its, stuck them under my keyboard, and
  labelled the pile 'IT-approved filing system.'" Rejected: the
  password-on-a-sticky-note is a stock IT joke (fails originality),
  and the punch partly lands mid-line — without the last clause
  the violation alone is still funny, so the twist is not
  essential.
- Draft C (161 chars): "HR said log every hour in Jira, so I
  logged 38 minutes as 'staring at the loading spinner' — my
  manager approved it in 4 seconds and asked for the ticket
  number." Rejected: without the last clause the rubber-stamp
  approval in 4 seconds is already the joke, so the final twist
  is decorative, not load-bearing; and the mechanism is two beats
  (rule, absurd compliance) plus an approval, not the three-beat
  rule / violation / cover-up shape the winners use.

Checklist 7B evidence (25 Nov 2026, per draft):
- Draft A: delete-last-clause PASS — without "and flagged my
  $3.80 coffee for missing approval" the line is just a fraud
  anecdote with no punch; the twist carries the joke. Swap-nouns
  PASS — genericised ("Finance capped dinners, so I split one
  dinner into several receipts — audit approved them and flagged
  my drink") loses all bite; the numbers are the joke. Vs joke-demo
  #1 (hazel-falcon-22-7196, 185 chars) PASS — same three-beat
  mechanism shape, different scene, numbers, and system; not a
  generalised copy.
- Draft B: delete-last-clause FAIL — without the final clause the
  14 Post-its under the keyboard are already funny. Swap-nouns
  BORDERLINE — hiding a password under the keyboard survives
  genericisation. Vs #1: cover-up label echoes "put the line
  back" but the premise is a stock IT joke.
- Draft C: delete-last-clause FAIL — "approved it in 4 seconds"
  is already the punch without the ticket-number twist. Swap-nouns
  PASS — 38 minutes / 4 seconds / ticket number are load-bearing.
  Vs #1: own scene, but only two beats plus an approval.

Deterministic: fixed string, stdlib only, no network, no randomness.
Both runs write byte-identical output.

Revision history: the first reviser (25 Nov 2026) moved gate
validation into a standalone validate_entry() helper, rejected
control characters, and made writing atomic (tempfile in the output
dir + fsync + os.replace). This revision (25 Nov 2026) replaces the
entry text under the winner-study playbook (winner-study-20261125.md
sections 3d, 6, 7B) and adds a leading/trailing-whitespace check:
a one-line joke with a stray space at either end wastes a gate
character and is not tight.

  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import tempfile
import unicodedata

JOKE = (
    "Finance capped client dinners at $40, so I split one "
    "$240 dinner into six $40 receipts \u2014 audit approved "
    "all six and flagged my $3.80 coffee for missing approval."
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
    if entry != entry.strip():
        raise ValueError("entry must not start or end with whitespace")
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
