from docutils import nodes


class link(nodes.General, nodes.Inline, nodes.Element):

    def astext(self):
        return self.get('alt', '')
