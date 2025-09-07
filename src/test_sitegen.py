import unittest
from sitegen import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_with_whitespace(self):
        self.assertEqual(extract_title("   #   World   "), "World")

    def test_ignore_h2(self):
        md = "## Not Title\n# Real Title"
        self.assertEqual(extract_title(md), "Real Title")

    def test_no_h1(self):
        with self.assertRaises(ValueError):
            extract_title("## Only H2\ntext")

if __name__ == "__main__":
    unittest.main()
