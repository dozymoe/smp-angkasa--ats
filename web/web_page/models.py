from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import rules
from rules.contrib.models import RulesModel


class WebPageManager(models.Manager):
    def get_by_natural_key(self, key):
        return self.get(slug=key)


class WebPage(DirtyFieldsMixin, RulesModel):
    title = models.CharField(verbose_name=_("Title"), max_length=65)
    body = models.TextField(verbose_name=_("Body"))
    slug = models.SlugField(max_length=64, unique=True, db_index=True,
            blank=True,
            help_text=_("Human friendly unique url to identify the content, "
            "will automatically be filled if left empty."))

    published_at = models.DateTimeField(verbose_name=_("Publish Date"),
            db_index=True, null=True, blank=True)
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.PROTECT, null=True, blank=True,
            related_name='published_webpages')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.PROTECT, db_index=True,
            related_name='created_webpages')
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(db_index=True, null=True, blank=True)

    objects = WebPageManager()


    class Meta:

        get_latest_by = 'published_at'
        ordering = ['-modified_at']
        rules_permissions = {
            'add': rules.is_authenticated,
            'read': rules.always_allow,
            'change': rules.is_staff,
            'delete': rules.is_staff,
        }


    def __str__(self): # pylint:disable=invalid-str-returned
        return self.title


    def get_absolute_url(self):
        return reverse('WebPage:Display', args=(self.slug, 'html'))


    def get_natural_key(self):
        return (self.slug,)


    def save(self, update_fields=None, **kwargs):
        dirty = self.get_dirty_fields()
        if not update_fields is None:
            dirty = {key: val for (key, val) in dirty.items()\
                    if key in update_fields}

        if 'title' in dirty and self.title and\
                ('slug' not in dirty or not self.slug):
            self.slug = slugify(self.title)
            if update_fields and 'slug' not in update_fields:
                update_fields.append('slug')

        return super().save(update_fields=update_fields, **kwargs)


    @staticmethod
    def get_microdata_type():
        return 'http://schema.org/WebPage'
