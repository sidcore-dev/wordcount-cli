"""Core text-analysis logic — pure functions, no I/O."""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field

_WORD_RE = re.compile(r"[A-Za-z0-9]+")


@dataclass
class TextStats:
    lines: int
    words: int
    chars: int
    top_words: list[tuple[str, int]] = field(default_factory=list)


def tokenize(text: str) -> list[str]:
    """Split text into lowercase, punctuation-stripped word tokens."""
    return _WORD_RE.findall(text.lower())


def top_words(text: str, top_n: int = 10) -> list[tuple[str, int]]:
    """Return the `top_n` most frequent words as (word, count) pairs."""
    if top_n <= 0:
        return []
    counts = Counter(tokenize(text))
    return counts.most_common(top_n)


def analyze(text: str, top_n: int = 10) -> TextStats:
    """Compute line/word/character counts and top word frequencies.

    Line count uses `str.splitlines()`, so a trailing newline doesn't
    count as an extra blank line. Word count uses whitespace splitting
    (`str.split()`), which differs slightly from the punctuation-stripped
    tokenization used for the top-words frequency list.
    """
    return TextStats(
        lines=len(text.splitlines()),
        words=len(text.split()),
        chars=len(text),
        top_words=top_words(text, top_n),
    )
