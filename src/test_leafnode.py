import unittest

from leafnode import *

class TestLeafnode(unittest.TestCase):
    def test_to_html_none(self):
        with self.assertRaises(ValueError):
            node = LeafNode(None, None, None)
            node.to_html()

    def test_to_html(self):
        test_cases = [
            LeafNode("a", "Click me!", {"href": "https://www.google.com"}),
            LeafNode("p", "This is a paragraph of text."),
        ]

        results = [
            "<a href=\"https://www.google.com\">Click me!</a>",
            "<p>This is a paragraph of text.</p>"
        ]

        for i in range(0, 2):
            self.assertEqual(test_cases[i].to_html(), results[i])


if __name__ == "__main__":
    unittest.main()