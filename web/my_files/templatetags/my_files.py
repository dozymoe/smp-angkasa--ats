"""Django templatetags for working with files
"""
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
#-
from ..models import MyFile

register = template.Library()


@register.simple_tag
def webfile(pk, alt=None):
    """Embed file as hyperlink or image in the templates
    """
    obj_id = int(pk)
    try:
        obj = MyFile.objects.get(pk=obj_id)
    except MyFile.DoesNotExist:
        return f':webfile:`{pk}`'

    if obj.mimetype.startswith('image/'):
        url = obj.image_lg.url
        if alt:
            text = escape(alt)
        elif obj.alt_text:
            text = escape(obj.alt_text)
        elif obj.description:
            text = escape(obj.description)
        else:
            text = url
        srcset = escape(obj.get_html_attr_srcset())
        sizes = escape(obj.get_html_attr_sizes())
        return mark_safe(f'<img src="{url}" alt="{text}" srcset="{srcset}"'
                f'sizes="{sizes}">')

    url = obj.databits.url
    if alt:
        text = escape(alt)
    else:
        text = escape(obj.description)
    return mark_safe(f'<a href="{url}" target="_blank">{text}</a>')
