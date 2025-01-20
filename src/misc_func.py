from textnode import *
from htmlnode import *
import re

def text_node_to_html_node(text_node: TextNode):
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text).to_html()
        case TextType.BOLD:
            return LeafNode("b", text_node.text).to_html()
        case TextType.ITALIC:
            return LeafNode("i", text_node.text).to_html()
        case TextType.CODE:
            return LeafNode("code", text_node.text).to_html()
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url}).to_html()
        case TextType.IMAGE:
            prop = {}
            prop.update({"src":text_node.url})
            prop.update({"alt":text_node.text})
            return LeafNode("img", "", prop).to_html()

        case _:
            raise Exception(f"TextType is not supported: {text_node.text_type}")
        
#accepts both textnode or list
def split_nodes_delimiter(old_nodes: TextNode|dict, delimiter:str, text_type:TextType):

    return_list = []

    #edge case when old_node != list
    _nodes = []

    #if it's a single node, just toss it
    #so it doesn't break the code
    if type(old_nodes) == TextNode:
        _nodes.append(old_nodes)
    else:
        _nodes.extend(old_nodes)

    for node in _nodes:
        if node.text_type != TextType.TEXT:
            return_list.append(node)
        else:
            string_split = node.text.split(delimiter, 2)

            return_list.append(TextNode(string_split[0], TextType.TEXT))
            return_list.append(TextNode(string_split[1],text_type))
            return_list.append(TextNode(string_split[2], TextType.TEXT))

    return return_list


def extract_markdown_images(text:str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_base(old_nodes, node_type:TextType):
    new_nodes = []
    return_list = []
    return_node_type = lambda _tuple: TextNode(_tuple[0], node_type, _tuple[1])

    if type(old_nodes) == TextNode:
        new_nodes.append(old_nodes)
    else:
        new_nodes.extend(old_nodes)

    for node in new_nodes:
        extracted_nodes = []
        if node_type == TextType.IMAGE:
            extracted_nodes = extract_markdown_images(node.text)
        elif node_type == TextType.LINK:
            extracted_nodes = extract_markdown_links(node.text)
        else:
            raise Exception("not supported type")
        
        if not extracted_nodes:
            return_list.append(node)
            continue
        
        cur_text = node.text
        for e_nodes in extracted_nodes:
            delimiter = ""
            
            if node_type == TextType.IMAGE:
                delimiter += "!"

            delimiter += f"[{e_nodes[0]}]({e_nodes[1]})"

            ss = cur_text.split(delimiter,1)

            #there are 3 cases only
            #case 1: edge case 
            # ![rick roll](https://i.imgur.com/aKaOqIh.gif)
            # result = "" + extracted + ""
            if not ss[0] and not ss[1]:
                return_list.append(return_node_type(e_nodes))
                continue

            #case 2
            # ![rick roll](https://i.imgur.com/aKaOqIh.gif) and
            # result = "" + extracted + reminder text
            if not ss[0]:
                return_list.append(return_node_type(e_nodes))
                cur_text = ss[1]
                continue
            
            #case 3
            # This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)
            # results = text + extracted + ""

            return_list.append(TextNode(ss[0], TextType.TEXT))
            return_list.append(return_node_type(e_nodes))
            cur_text = ss[1]

    if cur_text:
        return_list.append(TextNode(cur_text, TextType.TEXT))

    return return_list


def split_nodes_images(old_nodes):
    return split_nodes_base(old_nodes, TextType.IMAGE)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
   
def split_nodes_link(old_nodes):
    return split_nodes_base(old_nodes, TextType.LINK)

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    input_str = text
    return_list = []

    while input_str:
        # check for **(bold)
        node = split_nodes_delimiter(node, "**", TextType.BOLD)
        last_node = node.pop()
        input_str = last_node.text
        return_list.extend(node)
        node = last_node

        # check for *(italic)
        node = split_nodes_delimiter(node, "*", TextType.ITALIC)
        last_node = node.pop()
        input_str = last_node.text
        return_list.extend(node)
        node = last_node

        # check for `(code)
        node = split_nodes_delimiter(node, "`", TextType.CODE)
        last_node = node.pop()
        input_str = last_node.text
        return_list.extend(node)
        node = last_node

        # check for image
        node = split_nodes_images(node)
        last_node = node.pop()
        input_str = last_node.text
        return_list.extend(node)
        node = last_node

        # check for link
        node = split_nodes_link(node)
        if len(node) > 2:
            last_node = node.pop()
            input_str = last_node.text
        else:
            input_str = ""

        return_list.extend(node)
        node = last_node
    
    return return_list