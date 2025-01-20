from enum import Enum
from parentnode import ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):

    ss = markdown.split("\n\n")
    a = list(map(lambda x: x.strip(), ss))
    return a

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
            pass
        case BlockType.HEADING:
            pass
        case BlockType.CODE:
            pass
        case BlockType.QUOTE:
            pass
        case BlockType.UNORDERED_LIST:
            pass
        case BlockType.ORDERED_LIST:
            pass       
        case _:
            raise Exception("Unsupported block type")

# markdown => blocks => html_node
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        blocktype = block_to_html_node(block)

        print()

    return ParentNode("div", children, None)