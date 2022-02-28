import logging
import re
#-
from django.utils.translation import gettext as _
from docutils.parsers.rst.roles import set_classes
#-
from website.restructured_text.nodes import link
from ..models import Event

_logger = logging.getLogger(__name__)

INLINE_PATTERN = re.compile(r'^(?P<text>.+)\s*<(?P<pk>\d+)>$')


def parse_embed_event(obj_id, options, block_text=None):
    try:
        obj = Event.objects.get(pk=obj_id)
    except Event.DoesNotExist:
        obj = None

    if obj is None or obj.published_at is None or\
            obj.deleted_at is not None:
        return []

    options['uri'] = obj.get_absolute_url()
    if not 'alt' in options:
        options['alt'] = obj.title
    set_classes(options)
    link_node = link(block_text, **options)
    return [link_node]


def embed_event_role(role, rawtext, text, lineno, inliner, options=None,
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
        _nodes = []
        msg = inliner.reporter.error(_("%s is not a number.") % pk, line=lineno)
        return [], [msg]

    _nodes = parse_embed_event(pk, options)
    if not _nodes:
        msg = inliner.reporter.error(
                _("Event with id:%s was not found.") % pk,
                line=lineno)
        return [], [msg]

    return _nodes, []
