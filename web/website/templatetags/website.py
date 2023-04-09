"""Django templatetags for working with the website itself
"""
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


def restructured_text(value):
    """Format reStructuredText into html
    """
    parts = publish_parts(value, writer=HtmlWriter(),
            settings_overrides=settings.RESTRUCTURED_TEXT)
    return mark_safe(parts['html_body'])

@register.filter(name='restify')
@stringfilter
def restify(value):
    """Django template tag for formatting reStructuredText
    """
    return restructured_text(value)


@register.filter
@stringfilter
def fulluri(value, request):
    """Get absolute url from url path
    """
    return request.build_absolute_uri(value)


@register.simple_tag
def stylesheets(module='main'):
    """Read stylesheet file list produced by webpack, inject into web pages
    """
    project = os.environ['PROJECT_NAME']
    try:
        with open(os.path.join(os.environ['ROOT_DIR'], 'var', project,
                'webpack-css.meta.json'),
                encoding='utf-8') as fmeta:
            webpack = json.load(fmeta, object_pairs_hook=OrderedDict)
    except OSError:
        return ''
    base_dir = os.path.join(os.environ['ROOT_DIR'], 'web', 'static', 'css')
    html = []
    for key, value in webpack.items():
        if not key.endswith('.css'):
            continue
        mtime = os.path.getmtime(os.path.join(base_dir, key))
        hmtime = hex(int(mtime))[2:]
        html.append(f'<link href="{value}?v={hmtime}" rel="stylesheet"/>')
    return mark_safe('\n'.join(html))


@register.simple_tag
def javascripts(module='main'):
    """Read javascript file list produced by webpack, inject into web pages
    """
    project = os.environ['PROJECT_NAME']
    try:
        with open(os.path.join(os.environ['ROOT_DIR'], 'var', project,
                'webpack-js.meta.json'),
                encoding='utf-8') as fmeta:
            webpack = json.load(fmeta, object_pairs_hook=OrderedDict)
    except OSError:
        return ''
    html = []
    for key, value in webpack.items():
        if not (key == 'js' or key.endswith('.js')):
            continue
        html.append(f'<script src="{value}"></script>')
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
    except ValueError as err:
        raise template.TemplateSyntaxError(
                "'capture_as' node requires a variable name.") from err
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureAsNode(nodelist, args)


@register.simple_tag
def iif(condition, truish, falsy):
    """One line if else statement in templates
    """
    if condition:
        return truish
    return falsy


@register.simple_tag
def flash_messages(messages, low, high=None):
    """Print flash messages
    """
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
    """Simple format unique html id
    """
    return f'{name}-{unique}'
