# wordcount-cli

A small, dependency-free command-line tool that reports line, word, and
character counts for a piece of text, plus its most frequent words.

## Why

`wc` gives you counts; it doesn't tell you what the text is actually
about. `wordcount-cli` adds a quick frequency breakdown on top of the
usual counts — handy for a first look at a transcript, a log file, or a
draft, without reaching for a notebook and a tokenizer.

## Install

```bash
pip install .
```

This installs a `wordcount-cli` command on your PATH.

## Usage

```bash
$ printf 'the quick brown fox jumps over the lazy dog\nthe dog barks at the fox\n' | wordcount-cli --top 5
Lines: 2
Words: 15
Characters: 69

Top 5 word(s):
  the: 4
  fox: 2
  dog: 2
  quick: 1
  brown: 1
```

Read from a file instead of stdin by passing its path:

```bash
wordcount-cli notes.txt
```

### Options

| Flag       | Description                                                |
|------------|--------------------------------------------------------------|
| `--top N`  | Number of most frequent words to show (default: 10)          |
| `--json`   | Emit machine-readable JSON instead of text                   |

```bash
$ echo "go go go stop" | wordcount-cli --top 1 --json
{
  "lines": 1,
  "words": 4,
  "chars": 14,
  "top_words": [
    {
      "word": "go",
      "count": 3
    }
  ]
}
```

### How counting works

- **Lines** use `str.splitlines()`, so a trailing newline at the end of
  the file doesn't count as an extra blank line.
- **Words** are counted by whitespace splitting (`str.split()`).
- **Top words** use a separate, punctuation-stripped tokenization:
  everything is lowercased and split into runs of letters/digits, so
  "Dog," "dog!" and "DOG" all count as the same word. This means the
  word-frequency total can differ slightly from the plain **Words**
  count above (e.g. a lone `--` or `...` counts as a "word" for spacing
  purposes but produces no token for frequency counting).

### Exit codes

- `0` — completed successfully
- `2` — the input file couldn't be read, or `--top` is negative

## Development

```bash
pip install -e .
python -m unittest discover -s tests -v
```

## License

All rights reserved. This code is public for viewing and reference only —
no license is granted to use, copy, modify, or redistribute it. See
[LICENSE](LICENSE) for details.
