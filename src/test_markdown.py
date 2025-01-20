import unittest
from markdown import *

class TestMiscFunc(unittest.TestCase):

    def test_markdown_to_blocks(self):
        input ="""
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        output =    [
                    "# This is a heading",
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
"""* This is the first list item in a list block
* This is a list item
* This is another list item"""
                    ]

        self.assertEqual(markdown_to_blocks(input), output)

    def test_block_to_block_type(self):
        block = "### heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "```\n code \n ```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = "> some quote \n> other quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "- some quote \n- other quote"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        block = "* some quote \n* other quote"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        block = "1. some quote \n2. other quote"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

#     def test_paragraph(self):
#         md = """
# This is **bolded** paragraph
# text in a p
# tag here

# """

#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(
#             html,
#             "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
#         )



if __name__ == "__main__":
    unittest.main()