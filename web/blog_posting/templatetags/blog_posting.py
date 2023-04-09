"""Django templatetags for working with blog posts
"""
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
#-
from ..models import BlogPosting

register = template.Library()


@register.simple_tag
def webblog(pk, alt=None):
    """Embed blog post as hyperlink in the templates
    """
    obj_id = int(pk)
    try:
        obj = BlogPosting.objects.get(pk=obj_id)
    except BlogPosting.DoesNotExist:
        obj = None

    if obj is None or obj.published_at is None or obj.deleted_at is not None:
        return f':webblog:`{pk}`'

    url = obj.get_absolute_url()
    if alt:
        text = escape(alt)
    else:
        text = escape(obj.title)
    return mark_safe(f'<a href="{url}">{text}</a>')
