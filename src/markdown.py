from enum import Enum
from parentnode import ParentNode
from textnode import TextNode, TextType
from misc_func import text_node_to_html_node, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):

    ss = markdown.split("\n\n")
    return_list = []
    
    for s in ss:
        if s == "":
            continue
        return_list.append(s.strip())
        
    return return_list

def block_to_block_type(block:str):

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")

    def check_for_block_type(input:list, symbol:str):
        valid = False

        for line in input:
            if line.startswith(symbol):
                valid = True
            break

        return valid

    if block.startswith(">"):
        if check_for_block_type(lines, ">"):
            return BlockType.QUOTE
        return BlockType.PARAGRAPH
    
    if block.startswith("* "):
        if check_for_block_type(lines, "* "):
            return BlockType.UNORDERED_LIST
        return BlockType.PARAGRAPH
    
    if block.startswith("- "):
        if check_for_block_type(lines, "- "):
            return BlockType.UNORDERED_LIST
        return BlockType.PARAGRAPH
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1

        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def block_to_html_node(block):
    blocktype = block_to_block_type(block)

    match(blocktype):
        case BlockType.PARAGRAPH:
            lines = block.split("\n")
            textnodes = text_to_textnodes(" ".join(lines))
            return block_to_paragraph_html_node(textnodes)
        case BlockType.HEADING:
            lines = block.split("\n")
            textnodes = text_to_textnodes(" ".join(lines))
            return block_to_heading_HTMLNode(textnodes)
        case BlockType.CODE:
            return block_to_code_HTMLNode(block)
        case BlockType.QUOTE:
            return block_to_quote_HTMLNode(block)
        case BlockType.UNORDERED_LIST:
            return block_to_unordered_HTMLNode(block)
        case BlockType.ORDERED_LIST:
            return block_to_ordered_HTMLNode(block)       
        case _:
            raise Exception("Unsupported block type")

def block_to_ordered_HTMLNode(block):
    lines = block.split("\n")
    children = []
    index = 1
    for line in lines:
        if not line.startswith(f"{index}. "):
            raise Exception("Not a valid ordered list")
        a = text_to_textnodes(line.strip(f"{index}. "))
        b = []
        for node in a:
            b.append(text_node_to_html_node(node))
        children.append(ParentNode("li", b))
        index += 1

    return ParentNode("ol", children)

def block_to_unordered_HTMLNode(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        if not line.startswith("- ") and not line.startswith("* "):
            raise Exception("Not a valid unordered list")
        marker = line[:2]
        a = text_to_textnodes(line.strip(marker))
        b = []
        for node in a:
            b.append(text_node_to_html_node(node))
        children.append(ParentNode("li", b))

    return ParentNode("ul", children)

def block_to_quote_HTMLNode(blocks):
    lines = blocks.split("\n")

    newline = []
    for line in lines:
        if not line.startswith("> "):
            raise Exception("Invalid quote line")
        newline.append(line.strip("> "))
    
    r = text_to_textnodes(" ".join(newline))

    children = []

    for child in r:
        children.append(text_node_to_html_node(child))

    return ParentNode("blockquote", children)

def block_to_code_HTMLNode(blocks):
    children = []
    if not blocks.startswith("'''") and not blocks.endswith("```"):
        raise Exception("No matching ``` at start and end")
    
    blocks = blocks.strip("```")
    textnodes = text_to_textnodes(blocks)
    for textnode in textnodes:
        children.append(text_node_to_html_node(textnode))

    return ParentNode("pre", [ParentNode("code", children)])

def block_to_heading_HTMLNode(textnodes):
    h_count = 0
    children = []

    for textnode in textnodes:
        for char in textnode.text:
            if char == "#":
                h_count += 1
        textnode.text = textnode.text.strip("#" * h_count + " ")
        r = text_node_to_html_node(textnode)
        children.append(r)

    return ParentNode(f"h{h_count}", children)

def block_to_paragraph_html_node(textnodes:TextNode):
    children = []
    for textnode in textnodes:
        r = text_node_to_html_node(textnode)
        children.append(r)

    return ParentNode("p", children)

# markdown => blocks => html_node
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        result = block_to_html_node(block)
        children.append(result)

    return ParentNode("div", children, None)

