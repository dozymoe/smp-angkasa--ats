import logging
#-
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.roles import set_classes
#-
from website.restructured_text.link_node import link
from ..models import MyFile

_logger = logging.getLogger(__name__)


class EmbedFileDirective(Directive):

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
        obj_id = int(self.arguments[0])
        try:
            obj = MyFile.objects.get(pk=obj_id)
        except MyFile.DoesNotExist:
            return []

        if obj.mimetype.startswith('image/'):
            self.options['uri'] = obj.image_lg.url
            if 'alt' in self.options:
                pass
            elif obj.alt_text:
                self.options['alt'] = obj.alt_text
            elif obj.description:
                self.options['alt'] = obj.description
            self.options['srcset'] = obj.get_html_attr_srcset()
            self.options['sizes'] = obj.get_html_attr_sizes()

            set_classes(self.options)
            image_node = nodes.image(self.block_text, **self.options)
            self.add_name(image_node)
            return [image_node]

        self.options['uri'] = obj.databits.url
        self.options['target'] = '_blank'
        if not 'alt' in self.options:
            self.options['alt'] = obj.description
        set_classes(self.options)
        link_node = link(self.block_text, **self.options)
        self.add_name(link_node)
        return [link_node]
