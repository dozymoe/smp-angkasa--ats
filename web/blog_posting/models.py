import logging
#-
from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import translation
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import rules
from rules.contrib.models import RulesModel
from translated_fields import TranslatedField, to_attribute
#-
from thing_keyword.models import ThingKeywordField
from website.mixins import MultilingualMixin, attrgetter

_logger = logging.getLogger(__name__)


class BlogPostingManager(models.Manager):
    def get_by_natural_key(self, key):
        return self.get(slug=key)


class BlogPosting(DirtyFieldsMixin, MultilingualMixin, RulesModel):
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
            {settings.LANGUAGE_CODE: {'blank': False}},
            attrgetter=attrgetter)
    slug = TranslatedField(
            models.SlugField(verbose_name=_("URL Name"), max_length=64,
                unique=True, db_index=True, blank=True, null=True,
                help_text=_("Human friendly unique url to identify the "
                "content, will automatically be filled if left empty.")),
            {settings.LANGUAGE_CODE: {'null': False}},
            attrgetter=attrgetter)

    image = models.ImageField(verbose_name=_("Image"),
            upload_to='blog_posting/original/',
            width_field='image_width', height_field='image_height', null=True,
            blank=True)
    image_height = models.SmallIntegerField(null=True, editable=False)
    image_width = models.SmallIntegerField(null=True, editable=False)

    published_at = models.DateTimeField(verbose_name=_("Publish Date"),
            db_index=True, null=True, blank=True)
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.PROTECT, null=True, blank=True,
            related_name='published_blogpostings')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.PROTECT, db_index=True,
            related_name='created_blogpostings')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(db_index=True, null=True, blank=True)

    image_xs = models.ImageField(upload_to='blog_posting/image_xs/', null=True,
            editable=False)
    image_sm = models.ImageField(upload_to='blog_posting/image_sm/', null=True,
            editable=False)
    image_md = models.ImageField(upload_to='blog_posting/image_md/', null=True,
            editable=False)
    image_lg = models.ImageField(upload_to='blog_posting/image_lg/', null=True,
            editable=False)

    objects = BlogPostingManager()
    keywords = GenericRelation(ThingKeywordField)


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
        with translation.override(self.valid_language()):
            return reverse('BlogPostingLang:Display', args=(self.slug, 'html'))


    def get_natural_key(self):
        return (self.slug,)


    def get_image_url(self):
        return reverse('BlogPosting:Image', args=(self.pk, 'lg'))


    def is_published(self):
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
                setattr(self, slug_field, slugify(getattr(self, title_field)))
                if update_fields and slug_field not in update_fields:
                    update_fields.append(slug_field)

        return super().save(update_fields=update_fields, **kwargs)


    def get_html_attr_srcset(self):
        attribute_value = []
        for name, size, _ in settings.IMAGE_SIZES:
            imgfield = getattr(self, f'image_{name}')
            if not imgfield:
                continue
            attribute_value.append('%s %sw' % (
                    reverse('BlogPosting:Image', args=(self.pk, name)),
                    size[0]))
        return ', '.join(attribute_value)


    def get_html_attr_sizes(self):
        attribute_value = []
        for name, size, viewport_width in settings.IMAGE_SIZES:
            imgfield = getattr(self, f'image_{name}')
            if not imgfield:
                continue
            if viewport_width:
                attribute_value.append('(max-width: %spx) %spx' % (
                        viewport_width,
                        size[0]))
            else:
                attribute_value.append('%spx' % size[0])
        return ', '.join(attribute_value)


    @staticmethod
    def get_microdata_type():
        return 'http://schema.org/BlogPosting'
