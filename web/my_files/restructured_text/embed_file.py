import logging
import re
#-
from django.utils.translation import gettext as _
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.roles import set_classes
#-
from website.restructured_text.link_node import link
from ..models import MyFile

_logger = logging.getLogger(__name__)

INLINE_PATTERN = re.compile(r'^(?P<text>.+)\s*<(?P<pk>\d+)>$')


def parse_embed_file(obj_id, options, block_text=None):
    try:
        obj = MyFile.objects.get(pk=obj_id)
    except MyFile.DoesNotExist:
        return []

    if obj.mimetype.startswith('image/'):
        if obj.image_lg:
            imgfield = obj.image_lg
        else:
            imgfield = obj.databits
        options['uri'] = imgfield.url

        if 'alt' in options:
            pass
        elif obj.alt_text:
            options['alt'] = obj.alt_text
        elif obj.description:
            options['alt'] = obj.description
        options['srcset'] = obj.get_html_attr_srcset()
        options['sizes'] = obj.get_html_attr_sizes()
        fn = nodes.image
    else:
        options['uri'] = obj.databits.url
        options['target'] = '_blank'
        if not 'alt' in options:
            options['alt'] = obj.description
        fn = link

    set_classes(options)
    node = fn(block_text, **options)
    return [node]


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
        try:
            pk = int(self.arguments[0])
            _nodes = parse_embed_file(pk, self.options, self.block_text)
            if _nodes:
                for node in _nodes:
                    self.add_name(node)
            else:
                msg = self.state_machine.reporter.error(
                        _("File with id:%s was not found.") % pk,
                        line=self.lineno)
                _nodes.append(msg)
        except ValueError:
            _nodes = []
            msg = self.state_machine.reporter.error(
                    _("%s is not a number.") % pk, line=self.lineno)
            _nodes.append(msg)
        return _nodes


def embed_file_role(role, rawtext, text, lineno, inliner, options=None,
        content=None):
    if options is None:
        options = {}

    # Accept text in the format of "long text <file_id>".
    match = INLINE_PATTERN.match(text)
    if match:
        options['alt'] = match.group('text')
        pk = match.group('pk')
    else:
        pk = text.strip()

    try:
        pk = int(pk)
    except ValueError:
        msg = inliner.reporter.error(_("%s is not a number.") % pk, line=lineno)
        return [], [msg]

    _nodes = parse_embed_file(pk, options)
    if not _nodes:
        msg = inliner.reporter.error(_("File with id:%s was not found.") % pk,
                line=lineno)
        return [], [msg]

    return _nodes, []
