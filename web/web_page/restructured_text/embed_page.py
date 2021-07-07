import logging
#-
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.roles import set_classes
#-
from website.restructured_text.link_node import link
from ..models import WebPage

_logger = logging.getLogger(__name__)


class EmbedPageDirective(Directive):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'alt': directives.unchanged,
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
            obj = WebPage.objects.get(pk=obj_id)
        except WebPage.DoesNotExist:
            obj = None

        if obj is None or obj.published_at is None or\
                obj.deleted_at is not None:
            return []

        self.options['uri'] = obj.get_absolute_url()
        if not 'alt' in self.options:
            self.options['alt'] = obj.title
        set_classes(self.options)
        link_node = link(self.block_text, **self.options)
        self.add_name(link_node)
        return [link_node]
