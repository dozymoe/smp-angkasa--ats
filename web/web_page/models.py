"""Django models for working with web pages
"""
import logging
#-
from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import translation
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import rules
from rules.contrib.models import RulesModel
from translated_fields import TranslatedField, to_attribute
#-
from website.mixins import MultilingualMixin, attrgetter
from website.models_utils import uniqueness

_logger = logging.getLogger(__name__)


class WebPageManager(models.Manager):
    """Custom Django model manager that helps with serialization
    """
    def get_by_natural_key(self, key):
        """Unique record identifier for serialization
        """
        return self.get(slug=key)


class WebPage(DirtyFieldsMixin, MultilingualMixin, RulesModel):
    """Model for web page
    """
    REQUIRED_TRANSLATED_FIELDS = ('title', 'body', 'summary', 'slug')

    title = TranslatedField(
            models.CharField(verbose_name=_("Title"), max_length=65,
                blank=True),
            {settings.LANGUAGE_CODE: {'blank': False}},
            attrgetter=attrgetter)
    body = TranslatedField(
            models.TextField(verbose_name=_("Body"), blank=True),
            {settings.LANGUAGE_CODE: {'blank': False}},
            attrgetter=attrgetter)
    summary = TranslatedField(
            models.TextField(verbose_name=_("Summary"), blank=True),
            attrgetter=attrgetter)
    slug = TranslatedField(
            models.SlugField(verbose_name=_("URL Name"), max_length=64,
                unique=True, db_index=True, blank=True, null=True,
                help_text=_("Human friendly unique url to identify the "
                "content, will automatically be filled if left empty.")),
            {settings.LANGUAGE_CODE: {'null': False}},
            attrgetter=attrgetter)

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
        """Unique url that represents the model instance
        """
        with translation.override(self.valid_language()):
            return reverse('WebPageLang:Display', args=(self.slug, 'html'))


    def get_natural_key(self):
        """Unique record identifier for serialization
        """
        return (self.slug,)


    def is_published(self):
        """Check instance has been published
        """
        return self.published_at and not self.deleted_at


    def save(self, update_fields=None, **kwargs):
        dirty = self.get_dirty_fields()
        if not update_fields is None:
            dirty = {key: val for (key, val) in dirty.items()\
                    if key in update_fields}

        for langcode, _ in settings.LANGUAGES:
            title_field = to_attribute('title', langcode)
            slug_field = to_attribute('slug', langcode)
            if title_field in dirty and getattr(self, title_field) and\
                    (slug_field not in dirty or not getattr(self, slug_field)):

                setattr(self, slug_field,
                        uniqueness(slugify(getattr(self, title_field))))

                if update_fields and slug_field not in update_fields:
                    update_fields.append(slug_field)

        return super().save(update_fields=update_fields, **kwargs)


    @staticmethod
    def get_microdata_type():
        """Get microdata type of the model itself
        """
        return 'http://schema.org/WebPage'
