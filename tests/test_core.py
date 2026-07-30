import unittest

from wordcount_cli.core import analyze, tokenize, top_words


class TestTokenize(unittest.TestCase):
    def test_lowercases(self) -> None:
        self.assertEqual(tokenize("Hello World"), ["hello", "world"])

    def test_strips_punctuation(self) -> None:
        self.assertEqual(tokenize("Hello, world!!"), ["hello", "world"])

    def test_keeps_numbers(self) -> None:
        self.assertEqual(tokenize("Top 10 tips"), ["top", "10", "tips"])


class TestTopWords(unittest.TestCase):
    def test_counts_frequency(self) -> None:
        result = top_words("the cat sat on the mat the cat ran")
        self.assertEqual(result[0], ("the", 3))
        self.assertEqual(result[1], ("cat", 2))

    def test_respects_top_n(self) -> None:
        result = top_words("a b c d e", top_n=2)
        self.assertEqual(len(result), 2)

    def test_zero_top_n_returns_empty(self) -> None:
        self.assertEqual(top_words("a a b", top_n=0), [])

    def test_case_insensitive(self) -> None:
        result = dict(top_words("Cat cat CAT"))
        self.assertEqual(result, {"cat": 3})


class TestAnalyze(unittest.TestCase):
    def test_line_word_char_counts(self) -> None:
        stats = analyze("hello world\nsecond line\n")
        self.assertEqual(stats.lines, 2)
        self.assertEqual(stats.words, 4)
        self.assertEqual(stats.chars, len("hello world\nsecond line\n"))

    def test_empty_text(self) -> None:
        stats = analyze("")
        self.assertEqual(stats.lines, 0)
        self.assertEqual(stats.words, 0)
        self.assertEqual(stats.chars, 0)
        self.assertEqual(stats.top_words, [])

    def test_top_words_included(self) -> None:
        stats = analyze("go go go stop", top_n=1)
        self.assertEqual(stats.top_words, [("go", 3)])


if __name__ == "__main__":
    unittest.main()
