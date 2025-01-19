
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props:dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        if type(props) == dict:
            self.props = props.copy()
        else:
            self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        return_str = []

        for prop in self.props:
            return_str.append(f"{prop}=\"{self.props[prop]}\"")

        return " ".join(return_str)
    
    def __repr__(self):
        l_ = []
        l_.append(f"tag={self.tag}")
        l_.append(f"value={self.value}")
        l_.append(f"children={self.children}")
        return " ".join(l_) + self.props_to_html()