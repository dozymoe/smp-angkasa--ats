"""Embed youtube link in the templates
"""
import logging
#-
from docutils import nodes
from docutils.parsers.rst import Directive, directives

_logger = logging.getLogger(__name__)

DEFAULT_WIDTH = 320
DEFAULT_HEIGHT = 200

def parse_embed_youtube(video_id, options, block_text=None):
    """Render youtube id as Html iframe element
    """
    template = """
<iframe src="https://www.youtube.com/embed/%(video_id)s" width="%(width)u"
    height="%(height)u" frameborder="0" webkitAllowFullScreen mozallowfullscreen
    allowfullscreen></iframe>
"""
    values = {
        'video_id': video_id,
        'width': options.get('width', DEFAULT_WIDTH),
        'height': options.get('height', DEFAULT_HEIGHT),
    }
    return [nodes.raw('', template % values, format='html')]


class EmbedYoutubeDirective(Directive):
    """Embed youtube video as a section of its own
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'alt': directives.unchanged,
        'height': directives.length_or_unitless,
        'width': directives.length_or_percentage_or_unitless,
        'name': directives.unchanged,
        'class': directives.class_option,
    }

    def run(self):
        """ Entry point.

        Check:
          * self.name
          * self.arguments
          * self.options
          * self.content
          * self.lineno
          * self.content_offset
          * self.block_text
          * self.state
          * self.state_machine

        """
        video_id = self.arguments[0]

        _nodes = parse_embed_youtube(video_id, self.options, self.block_text)
        for node in _nodes:
            self.add_name(node)

        return _nodes
