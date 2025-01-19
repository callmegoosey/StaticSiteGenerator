import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_create_def(self):
        node = HTMLNode()
        self.assertTrue(node.tag == None and 
                        node.value == None and
                        node.children == None and
                        node.props == None)

    def test_create_assign(self):
        node = HTMLNode("test_tag", "test_value","test_children", "test_prop")
        self.assertTrue(node.tag == "test_tag" and 
                        node.value == "test_value" and
                        node.children == "test_children" and
                        node.props == "test_prop")
    
    def test_prop_to_html(self):
        node = HTMLNode()
        node.props = {
                        "href": "https://www.google.com",
                        "target": "_blank",
                    }
        
        self.assertEqual(node.props_to_html(), "href=\"https://www.google.com\" target=\"_blank\"")


if __name__ == "__main__":
    unittest.main()