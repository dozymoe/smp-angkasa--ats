"""Django models for working with events
"""
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
from website.models_utils import uniqueness
from website.mixins import MultilingualMixin, attrgetter

class EventManager(models.Manager):
    """Custom Django model manager that helps with serialization
    """
    def get_by_natural_key(self, key):
        """Unique record identifier for serialization
        """
        return self.get(slug=key)


class Event(DirtyFieldsMixin, MultilingualMixin, RulesModel):
    """Model for web page
    """
    REQUIRED_TRANSLATED_FIELDS = ('title', 'slug')

    started_at = models.DateTimeField(verbose_name=_("Started At"),
            db_index=True)
    stopped_at = models.DateTimeField(verbose_name=_("Stopped At"),
            db_index=True, null=True, blank=True)

    title = TranslatedField(
            models.CharField(verbose_name=_("Title"), max_length=65,
                blank=True),
            {settings.LANGUAGE_CODE: {'blank': False}},
            attrgetter=attrgetter)
    body = TranslatedField(
            models.TextField(verbose_name=_("Body"), blank=True, null=True),
            attrgetter=attrgetter)
    summary = TranslatedField(
            models.TextField(verbose_name=_("Summary"), blank=True, null=True),
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
            related_name='published_events')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.PROTECT, db_index=True,
            related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(db_index=True, null=True, blank=True)

    objects = EventManager()


    class Meta:
        get_latest_by = 'created_at'
        ordering = ['-created_at']
        rules_permissions = {
            'add': rules.is_staff,
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
            return reverse('EventLang:Display', args=(self.slug, 'html'))


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
