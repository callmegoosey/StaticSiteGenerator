import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_text_type_update(self):
        node = TextNode("This is a text node", TextType.BOLD)
        new_text = "this is a new text papi"
        node.text = new_text
        self.assertEqual(node.text, new_text)
    
        
if __name__ == "__main__":
    unittest.main()