"""docutils custom nodes
"""
from docutils import nodes

class link(nodes.General, nodes.Inline, nodes.Element):
    """Hyperlink with text in them
    """
    def astext(self):
        return self.get('alt', '')


class video(nodes.General, nodes.Element):
    """HTML video element
    """


class rawhtml(nodes.Text):
    """Raw HTML
    """
