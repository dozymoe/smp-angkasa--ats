"""Django templatetags for working with files
"""
from django import template
from django.utils.safestring import mark_safe
#-
from ..models import MyFile

register = template.Library()


@register.simple_tag
def webfile(obj, **kwargs):
    """Embed file as hyperlink or image in the templates
    """
    return mark_safe(obj.render(**kwargs))
