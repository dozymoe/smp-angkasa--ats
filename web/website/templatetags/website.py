from collections import OrderedDict
import json
import logging
import os
#-
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from docutils.core import publish_parts
#-
from website.restructured_text.html_writer import HtmlWriter

register = template.Library()
_logger = logging.getLogger(__name__)


@register.filter(name='restify')
@stringfilter
def restructured_text(value):
    parts = publish_parts(value, writer=HtmlWriter(),
            settings_overrides=settings.RESTRUCTURED_TEXT)
    return mark_safe(parts['html_body'])


@register.filter
@stringfilter
def fulluri(value, request):
    return request.build_absolute_uri(value)


@register.simple_tag
def stylesheets(module='main'):
    try:
        with open(os.path.join(os.environ['ROOT_DIR'], 'var',
                os.environ['PROJECT_NAME'], 'webpack-css.meta.json')) as f:
            webpack = json.load(f, object_pairs_hook=OrderedDict)
    except OSError:
        return ''
    html = []
    for key, value in webpack.items():
        if not key.endswith('.css'):
            continue
        html.append('<link href="%s" rel="stylesheet"/>' % value)
    return mark_safe('\n'.join(html))


@register.simple_tag
def javascripts(module='main'):
    try:
        with open(os.path.join(os.environ['ROOT_DIR'], 'var',
                os.environ['PROJECT_NAME'], 'webpack-js.meta.json')) as f:
            webpack = json.load(f, object_pairs_hook=OrderedDict)
    except OSError:
        return ''
    html = []
    for key, value in webpack.items():
        if not key.endswith('.js'):
            continue
        html.append('<script src="%s"></script>' % value)
    return mark_safe('\n'.join(html))


class CaptureAsNode(template.Node):
    """
    https://chase-seibert.github.io/blog/2010/10/01/check-if-a-block-is-defined-in-django.html
    """
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''


@register.tag
def captureas(parser, token):
    """
    https://chase-seibert.github.io/blog/2010/10/01/check-if-a-block-is-defined-in-django.html
    """
    try:
        _, args = token.contents.split(None, 1)
    except ValueError as e:
        raise template.TemplateSyntaxError(
                "'capture_as' node requires a variable name.") from e
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureAsNode(nodelist, args)


@register.simple_tag
def iif(condition, truish, falsy):
    if condition:
        return truish
    return falsy


@register.simple_tag
def flash_messages(messages, low, high=None):
    result = []
    for msg in messages:
        if msg.level < low:
            continue
        if high and msg.level >= high:
            continue
        result.append(msg.message)
    return result


@register.simple_tag
def html_id(name, unique):
    return '%s-%s' % (name, unique)
