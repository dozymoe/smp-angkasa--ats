import logging
import os
import re
import sys
#-
from docutils import nodes
from docutils.writers import html4css1
from docutils.writers._html_base import PIL, url2pathname

_logger = logging.getLogger(__name__)


class HtmlTranslator(html4css1.HTMLTranslator): # pylint:disable=abstract-method

    def visit_image(self, node):
        """ Please keep this copy in sync with: python_modules/docutils/writers/html4css1/__init__.py
        """ # pylint:disable=line-too-long
        atts = {}
        uri = node['uri']
        ext = os.path.splitext(uri)[1].lower()
        if ext in self.object_image_types:
            atts['data'] = uri
            atts['type'] = self.object_image_types[ext]
        else:
            atts['src'] = uri
            atts['alt'] = node.get('alt', uri)
        # new html attributes
        for attr in ('sizes', 'srcset'):
            if attr in node:
                atts[attr] = node[attr]
        # image size
        if 'width' in node:
            atts['width'] = node['width']
        if 'height' in node:
            atts['height'] = node['height']
        if 'scale' in node:
            if (PIL and not ('width' in node and 'height' in node)
                and self.settings.file_insertion_enabled):
                imagepath = url2pathname(uri)
                try:
                    img = PIL.Image.open(
                            imagepath.encode(sys.getfilesystemencoding()))
                except (IOError, UnicodeEncodeError):
                    pass # TODO: warn?
                else:
                    self.settings.record_dependencies.add(
                        imagepath.replace('\\', '/'))
                    if 'width' not in atts:
                        atts['width'] = '%dpx' % img.size[0]
                    if 'height' not in atts:
                        atts['height'] = '%dpx' % img.size[1]
                    del img
            for att_name in 'width', 'height':
                if att_name in atts:
                    match = re.match(r'([0-9.]+)(\S*)$', atts[att_name])
                    assert match
                    atts[att_name] = '%s%s' % (
                        float(match.group(1)) * (float(node['scale']) / 100),
                        match.group(2))
        style = []
        for att_name in 'width', 'height':
            if att_name in atts:
                if re.match(r'^[0-9.]+$', atts[att_name]):
                    # Interpret unitless values as pixels.
                    atts[att_name] += 'px'
                style.append('%s: %s;' % (att_name, atts[att_name]))
                del atts[att_name]
        if style:
            atts['style'] = ' '.join(style)
        if (isinstance(node.parent, nodes.TextElement) or
            (isinstance(node.parent, nodes.reference) and
             not isinstance(node.parent.parent, nodes.TextElement))):
            # Inline context or surrounded by <a>...</a>.
            suffix = ''
        else:
            suffix = '\n'
        if 'align' in node:
            atts['class'] = 'align-%s' % node['align']
        if ext in self.object_image_types:
            # do NOT use an empty tag: incorrect rendering in browsers
            self.body.append(self.starttag(node, 'object', '', **atts) +
                             node.get('alt', uri) + '</object>' + suffix)
        else:
            self.body.append(self.emptytag(node, 'img', suffix, **atts))


    def visit_link(self, node):
        atts = {'href': node['uri']}
        for att_name in ('target',):
            if att_name in node:
                atts[att_name] = node[att_name]

        self.body.append(self.starttag(node, 'a', **atts))
        self.body.append(node.astext())


    def depart_link(self, node):
        if (isinstance(node.parent, nodes.TextElement) or
            (isinstance(node.parent, nodes.reference) and
             not isinstance(node.parent.parent, nodes.TextElement))):
            # Inline context or surrounded by <a>...</a>.
            suffix = ''
        else:
            suffix = '\n'
        self.body.append('</a>' + suffix)


    def visit_video(self, node):
        atts = {}
        source_atts = {}

        if 'width' in node:
            atts['width'] = node['width']
        if 'height' in node:
            atts['height'] = node['height']
        if 'class' in node:
            atts['class'] = node['class']
        if node.get('autoplay'):
            atts['autoplay'] = 'autoplay'
        if not node.get('nocontrols'):
            atts['controls'] = ''
        if 'type' in node:
            source_atts['type'] = node['type']
        source_atts['src'] = node['uri']

        self.body.append(self.starttag(node, 'video', '\n', **atts))
        self.body.append(self.emptytag(node, 'source', '\n', **source_atts))
        if 'alt' in node:
            self.body.append(node['alt'])


    def depart_video(self, node):
        self.body.append('</video>\n')


class HtmlWriter(html4css1.Writer):

    def __init__(self):
        super().__init__()
        self.translator_class = HtmlTranslator
