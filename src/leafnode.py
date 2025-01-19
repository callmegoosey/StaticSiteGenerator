from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props:dict = None):
        super().__init__(tag, value,None,props)

    def to_html(self):
        if not self.value and type(self.value) != str:
            raise ValueError("LeafNode value is None")

        l_ = []

        match(self.tag):
            case "a":
                return f"<a {self.props_to_html()}>{self.value}</a>"
            case None:
                return self.value
            case _:
                return f"<{self.tag}>{self.value}</{self.tag}>"

# def main():
#     ln = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
#     print(ln.to_html())
#     ln2 = LeafNode("p", "This is a paragraph of text.")
#     print(ln2.to_html())

# main()