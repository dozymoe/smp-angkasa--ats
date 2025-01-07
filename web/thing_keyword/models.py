"""Django models for working with keywords
"""
from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.db import models
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node, MP_NodeManager

class ThingKeywordManager(MP_NodeManager):
    """Custom Django model manager that helps with serialization
    """
    def get_by_natural_key(self, key):
        """Unique record identifier for serialization
        """
        return self.get(slug=key)


class ThingKeyword(DirtyFieldsMixin, MP_Node):
    """Model for keyword
    """
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64, db_index=True)
    node_order_by = ['name']

    description = models.CharField(max_length=255)
    slug = models.SlugField(max_length=64, unique=True, db_index=True,
            blank=True,
            help_text=_("Human friendly unique url to identify content, "
            "will automatically be filled if left empty."))

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.PROTECT, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(db_index=True, null=True, blank=True)

    objects = ThingKeywordManager()


    class Meta:
        verbose_name = "Keyword"
        ordering = ['title']


    def __str__(self): # pylint:disable=invalid-str-returned
        return self.title


    def get_absolute_url(self):
        """Unique url that represents the model instance
        """
        #return reverse('Keyword:Display',
        #        kwargs={'slug': self.slug, 'format': 'html'})


    def get_natural_key(self):
        """Unique record identifier for serialization
        """
        return (self.slug, )


    def save(self, *args, update_fields=None, **kwargs):
        dirty = self.get_dirty_fields()
        if not update_fields is None:
            dirty = {key: val for (key, val) in dirty.items()\
                    if key in update_fields}

        if 'title' in dirty and self.title and\
                ('slug' not in dirty or not self.slug):
            self.slug = slugify(self.title)
            if update_fields and 'slug' not in update_fields:
                update_fields.append('slug')

        super().save(update_fields=update_fields, **kwargs)


    @staticmethod
    def get_microdata_type():
        """Get microdata type of the model itself
        """
        return 'http://schema.org/Thing/Keyword'


class ThingKeywordField(models.Model):
    """Generic many to many relationship between content and keyword
    """
    keyword = models.ForeignKey(ThingKeyword, related_name='contents',
            on_delete=models.CASCADE)

    ## contenttypes
    entity = GenericForeignKey()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    ## timestamps
    published_at = models.DateTimeField(db_index=True, null=True,
            editable=False)
