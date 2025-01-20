import unittest
from textnode import *
from misc_func import *

class TestMiscFunc(unittest.TestCase):
    def test_text_node_to_html_node_none(self):
        with self.assertRaises(Exception):
            node = TextNode("a", None)
            text_node_to_html_node(node)

    def test_text_node_to_html_node_text(self):
        text = "this is raw text"
        textnode = TextNode(text, TextType.TEXT)
        leafnode = LeafNode(None, text)
        self.assertEqual(text_node_to_html_node(textnode),leafnode.to_html())

    def test_text_node_to_html_node_bold(self):
        text = "this is bold text"
        textnode = TextNode(text, TextType.BOLD)
        leafnode = LeafNode("b", text)
        self.assertEqual(text_node_to_html_node(textnode),leafnode.to_html())

    def test_text_node_to_html_node_ITALIC(self):
        text = "this is ITALIC text"
        textnode = TextNode(text, TextType.ITALIC)
        leafnode = LeafNode("i", text)
        self.assertEqual(text_node_to_html_node(textnode),leafnode.to_html())

    def test_text_node_to_html_node_CODE(self):
        text = "this is CODE"
        textnode = TextNode(text, TextType.CODE)
        leafnode = LeafNode("code", text)
        self.assertEqual(text_node_to_html_node(textnode),leafnode.to_html())

    def test_text_node_to_html_node_LINK(self):
        text = "this is a LINK"
        textnode = TextNode(text, TextType.LINK, "https://www.google.com")
        leafnode = LeafNode("a", text, {"href": "https://www.google.com"})
        self.assertEqual(text_node_to_html_node(textnode), leafnode.to_html())

    def test_text_node_to_html_node_IMAGE(self):
        text = "this is an IMAGE"
        textnode = TextNode(text, TextType.IMAGE, "pp.png")
        leafnode = LeafNode("img", "", {
                                            "src": "pp.png",
                                            "alt": "this is an IMAGE"
                                        })
        
        self.assertEqual(text_node_to_html_node(textnode), leafnode.to_html())


    # def test_split_node_no_closing_delimiter(self):
    #     with self.assertRaises(Exception):
    #         node = TextNode("This is text with a `code block word", TextType.TEXT)
    #         split_nodes_delimiter(node, "`", TextType.CODE)


    def test_split_nodes_create(self):
        inputs =     [
                        ["This is text with a **bolded phrase** in the middle", "**", TextType.BOLD],
                        ["This is text with a `code block` word", "`", TextType.CODE]
        ]
        outputs =    [
                        [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("bolded phrase", TextType.BOLD),
                            TextNode(" in the middle", TextType.TEXT),
                        ],
                        [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                        ]
        ]
        
        for i in range(0, len(inputs)):
            node = TextNode(inputs[i][0], TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], inputs[i][1], inputs[i][2])

            self.assertEqual(outputs[i], new_nodes)

    def test_extract_markdown_images(self):
        text =      """This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) 
                    and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"""
        output =    [   
                        ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
                        ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
                    ]
        
        self.assertEqual(extract_markdown_images(text), output)

    def test_extract_markdown_links(self):
        text =      """This is text with a link [to boot dev](https://www.boot.dev) 
                    and [to youtube](https://www.youtube.com/@bootdotdev)"""
        output =    [   
                        ("to boot dev", "https://www.boot.dev"), 
                        ("to youtube", "https://www.youtube.com/@bootdotdev")
                    ]
        
        self.assertEqual(extract_markdown_links(text), output)

    def test_split_nodes_images(self):
        text =      "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)" 
        output =    [
                        TextNode("This is text with a ", TextType.TEXT),
                        TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                        TextNode(" and ", TextType.TEXT),
                        TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg" ),
                    ]
              
        node = TextNode (text, TextType.TEXT)
        self.assertEqual(split_nodes_images([node]), output)

    def test_split_nodes_links(self):
        text =      "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        output =    [
                        TextNode("This is text with a link ", TextType.TEXT),
                        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                        TextNode(" and ", TextType.TEXT),
                        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                    ]
              
        node = TextNode (text, TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), output)

    def test_text_to_textnodes(self):
        text =      "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output =    [
                        TextNode("This is ", TextType.TEXT),
                        TextNode("text", TextType.BOLD),
                        TextNode(" with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word and a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and an ", TextType.TEXT),
                        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", TextType.TEXT),
                        TextNode("link", TextType.LINK, "https://boot.dev"),
                    ]
        self.assertEqual(text_to_textnodes(text), output)
        
if __name__ == "__main__":
    unittest.main()