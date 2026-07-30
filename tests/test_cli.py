import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from wordcount_cli.cli import main


class TestCli(unittest.TestCase):
    def test_reads_from_stdin_by_default(self) -> None:
        out = io.StringIO()
        with patch("sys.stdin", io.StringIO("the cat sat on the mat\n")):
            with redirect_stdout(out):
                code = main([])
        self.assertEqual(code, 0)
        text = out.getvalue()
        self.assertIn("Lines: 1", text)
        self.assertIn("Words: 6", text)

    def test_reads_from_file(self) -> None:
        with TemporaryDirectory() as tmp:
            f = Path(tmp) / "sample.txt"
            f.write_text("hello world\n")
            out = io.StringIO()
            with redirect_stdout(out):
                code = main([str(f)])
            self.assertEqual(code, 0)
            self.assertIn("Words: 2", out.getvalue())

    def test_missing_file_errors(self) -> None:
        code = main(["/nonexistent/path/nope.txt"])
        self.assertEqual(code, 2)

    def test_negative_top_errors(self) -> None:
        code = main(["--top", "-1"])
        self.assertEqual(code, 2)

    def test_json_output(self) -> None:
        out = io.StringIO()
        with patch("sys.stdin", io.StringIO("go go stop")):
            with redirect_stdout(out):
                code = main(["--json", "--top", "1"])
        self.assertEqual(code, 0)
        data = json.loads(out.getvalue())
        self.assertEqual(data["words"], 3)
        self.assertEqual(data["top_words"], [{"word": "go", "count": 2}])

    def test_top_option_limits_output(self) -> None:
        out = io.StringIO()
        with patch("sys.stdin", io.StringIO("a a b b c c d")):
            with redirect_stdout(out):
                main(["--top", "2"])
        self.assertIn("Top 2 word(s):", out.getvalue())


if __name__ == "__main__":
    unittest.main()
