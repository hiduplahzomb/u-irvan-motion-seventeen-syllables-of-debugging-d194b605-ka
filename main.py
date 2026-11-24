"""Seventeen Syllables of Debugging — KA entry.

A haiku about the 3 AM production bug that turns out to be one typo.
The pager screams, production burns, and the fix is a single line number.

Gate: entry.txt must be exactly 3 lines with syllable counts 5-7-5
(17 syllables total), counted by a simple vowel-group counter that
skips punctuation-only tokens (the em dash) and counts hyphenated
compounds part by part ("four-one-nine" is 3, not 4).
"""

import os
import re
import sys

# The haiku — 5 / 7 / 5 syllables, verified below by the counter.
TEXT = (
    "Pager screams at three\n"
    "production burns \u2014 one typo\n"
    "fix line four-one-nine"
)

VOWELS = "aeiouy"


def count_syllables(word):
    """Count syllables by vowel groups, minus a trailing silent 'e'.

    Hyphenated compounds are counted part by part, so each part gets
    its own silent-'e' treatment ("four-one-nine" is 3, not 4).
    """
    word = word.strip(".,;:!?\"'()[]{}").lower()
    if not word or not re.search(r"[a-z0-9]", word):
        return 0
    total = 0
    for part in word.split("-"):
        if not part:
            continue
        groups = len(re.findall(r"[aeiouy]+", part))
        if part.endswith("e") and groups > 1:
            groups -= 1
        total += max(groups, 1)
    return total


def main():
    lines = TEXT.split("\n")
    if len(lines) != 3:
        print(f"gate failed: expected 3 lines, got {len(lines)}", file=sys.stderr)
        return 1
    if not TEXT.strip():
        print("gate failed: empty entry", file=sys.stderr)
        return 1
    expected = (5, 7, 5)
    for i, line in enumerate(lines):
        count = sum(count_syllables(w) for w in line.split())
        if count != expected[i]:
            print(
                f"gate failed: line {i + 1} has {count} syllables, "
                f"expected {expected[i]}: {line!r}",
                file=sys.stderr,
            )
            return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(TEXT)
    with open(path, encoding="utf-8") as f:
        if f.read() != TEXT:
            print("gate failed: read-back mismatch", file=sys.stderr)
            return 1
    print(f"wrote {path} ({len(TEXT)} chars, 5-7-5)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
