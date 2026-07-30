"""Command-line entry point for wordcount-cli."""
from __future__ import annotations

import argparse
import json
import sys

from .core import TextStats, analyze


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wordcount-cli",
        description="Report line/word/character counts and top word frequencies for a text file or stdin.",
    )
    parser.add_argument("file", nargs="?", help="Path to a text file (default: read from stdin)")
    parser.add_argument(
        "--top", type=int, default=10, help="Number of most frequent words to show (default: 10)"
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of text")
    return parser


def _print_human(stats: TextStats) -> None:
    print(f"Lines: {stats.lines}")
    print(f"Words: {stats.words}")
    print(f"Characters: {stats.chars}")
    if stats.top_words:
        print()
        print(f"Top {len(stats.top_words)} word(s):")
        for word, count in stats.top_words:
            print(f"  {word}: {count}")


def _print_json(stats: TextStats) -> None:
    print(
        json.dumps(
            {
                "lines": stats.lines,
                "words": stats.words,
                "chars": stats.chars,
                "top_words": [{"word": w, "count": c} for w, c in stats.top_words],
            },
            indent=2,
        )
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.top < 0:
        print("wordcount-cli: error: --top must be >= 0", file=sys.stderr)
        return 2

    try:
        if args.file:
            with open(args.file, "r", encoding="utf-8") as fh:
                text = fh.read()
        else:
            text = sys.stdin.read()
    except OSError as exc:
        print(f"wordcount-cli: error: {exc}", file=sys.stderr)
        return 2

    stats = analyze(text, top_n=args.top)

    if args.json:
        _print_json(stats)
    else:
        _print_human(stats)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
