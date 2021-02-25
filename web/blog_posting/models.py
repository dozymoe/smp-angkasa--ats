from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
#from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import rules
from rules.contrib.models import RulesModel
#-
from thing_keyword.models import ThingKeywordField

COVER_SIZE = (300, 600)


class BlogPostingManager(models.Manager):
    def get_by_natural_key(self, key):
        return self.get(slug=key)


class BlogPosting(DirtyFieldsMixin, RulesModel):
    title = models.CharField(max_length=65)
    body = models.TextField()
    summary = models.TextField(max_length=155)
    slug = models.SlugField(max_length=64, unique=True, db_index=True,
            blank=True,
            help_text=_("Human friendly unique url to identify the content, "
            "will automatically be filled if left empty."))
    image = models.ImageField(upload_to='blog_posting/original/',
            width_field='image_width', height_field='image_height', null=True,
            blank=True)
    image_height = models.SmallIntegerField(null=True, editable=False)
    image_width = models.SmallIntegerField(null=True, editable=False)
    cover = models.ImageField(upload_to='blog_posting/cover/', null=True,
            editable=False)

    published_at = models.DateTimeField(verbose_name="publish date",
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

    objects = BlogPostingManager()
    keywords = GenericRelation(ThingKeywordField)


    class Meta:

        get_latest_by = 'published_at'
        ordering = ['-modified_at']
        rules_permissions = {
            'add': rules.is_authenticated,
            'read': rules.is_staff,
            'change': rules.is_staff,
            'delete': rules.is_staff,
        }


    def __str__(self): # pylint:disable=invalid-str-returned
        return self.title


    def get_absolute_url(self):
        pass


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
        return 'http://schema.org/BlogPosting'
