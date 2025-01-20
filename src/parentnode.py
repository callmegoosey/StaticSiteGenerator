from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        if not self.tag:
            raise ValueError("tag is None")
        if self.children is None:
            raise ValueError("children is None")
        
        child_list = []
        for child in self.children:
            child_list.append(child.to_html())

        return f"<{self.tag}>{"".join(child_list)}</{self.tag}>"