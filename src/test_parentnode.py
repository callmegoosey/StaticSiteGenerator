import unittest

from parentnode import *
from leafnode import *

class TestParentNode(unittest.TestCase):

    def test_create_with_values(self):
        tag = "a"
        children = ["a", "b", "c"]
        props = "some_prop"

        node = ParentNode(tag, children, props)

        self.assertEqual(node.tag, tag)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_to_html_none(self):
        with self.assertRaises(ValueError):
            test_case = [
                ParentNode(None, {"a"}),
                ParentNode(None, None)
            ]
            
            for node in test_case:
                node.to_html()


    def test_to_html(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
        )

        result = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        self.assertEqual(node.to_html(), result)

if __name__=="__main__":
    unittest.main()