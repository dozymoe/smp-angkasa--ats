"""Django templatetags for working with web pages
"""
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
#-
from ..models import WebPage

register = template.Library()


@register.simple_tag
def webpage(pk, alt=None):
    """Embed web page as hyperlink in the templates
    """
    obj_id = int(pk)
    try:
        obj = WebPage.objects.get(pk=obj_id)
    except WebPage.DoesNotExist:
        obj = None

    if obj is None or obj.published_at is None or obj.deleted_at is not None:
        return f':webpage:`{pk}`'

    url = obj.get_absolute_url()
    if alt:
        text = escape(alt)
    else:
        text = escape(obj.title)
    return mark_safe(f'<a href="{url}">{text}</a>')


@register.simple_tag
def webpage_url(pk):
    """Print the web page absolute url
    """
    obj_id = int(pk)
    try:
        obj = WebPage.objects.get(pk=obj_id)
    except WebPage.DoesNotExist:
        obj = None

    if obj is None or obj.published_at is None or obj.deleted_at is not None:
        return f':webpage:`{pk}`'

    return obj.get_absolute_url()
