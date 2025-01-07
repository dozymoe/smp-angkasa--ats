"""Django models for working with files
"""
import os
#-
from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import rules
from rules.contrib.models import RulesModel
from translated_fields import TranslatedField
#-
from website.mixins import MultilingualMixin, attrgetter
from website.rules import is_creator_or_staff

class MyFileManager(models.Manager):
    """Custom Django model manager that helps with serialization
    """
    def get_by_natural_key(self, key):
        """Unique record identifier for serialization
        """
        return self.get(filehash=key)


class MyFile(DirtyFieldsMixin, MultilingualMixin, RulesModel):
    """Model for file object
    """
    REQUIRED_TRANSLATED_FIELDS = ('description',)

    filehash = models.CharField(verbose_name=_("Title"), max_length=65,
            editable=False)
    mimetype = models.CharField(verbose_name=_("Mime Type"), max_length=50,
            editable=False)

    description = TranslatedField(
            models.TextField(verbose_name=_("Description"), null=True,
                blank=True),
            attrgetter=attrgetter)
    alt_text = TranslatedField(
            models.TextField(verbose_name=_("Alternate Text (alt text)"),
                null=True, blank=True,
                help_text=_("Textual representation of media or hyperlink text.")), # pylint:disable=line-too-long
            {settings.LANGUAGE_CODE: {'blank': False}},
            attrgetter=attrgetter)
    databits = models.FileField(verbose_name=_("Content"),
            upload_to='files/original/')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.PROTECT, db_index=True,
            related_name='created_files')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(db_index=True, null=True, blank=True)

    image_xs = models.ImageField(upload_to='files/image_xs/', null=True,
            editable=False)
    image_sm = models.ImageField(upload_to='files/image_sm/', null=True,
            editable=False)
    image_md = models.ImageField(upload_to='files/image_md/', null=True,
            editable=False)
    image_lg = models.ImageField(upload_to='files/image_lg/', null=True,
            editable=False)
    image_xlg = models.ImageField(upload_to='files/image_xlg/', null=True,
            editable=False)

    objects = MyFileManager()


    class Meta:

        get_latest_by = 'created_at'
        ordering = ['-created_at']
        rules_permissions = {
            'add': rules.is_authenticated,
            'read': rules.always_allow,
            'change': is_creator_or_staff,
            'delete': is_creator_or_staff,
        }


    def __str__(self): # pylint:disable=invalid-str-returned
        return self.filehash


    def get_absolute_url(self):
        """Unique url that represents the model instance
        """
        if self.is_image():
            for name, _t, _t in settings.IMAGE_SIZES:
                field = getattr(self, f'image_{name}', None)
                if not field:
                    continue
                return reverse('MyFile:Display', args=(self.pk, name))
        return reverse('MyFile:Display', args=(self.pk,))


    def get_natural_key(self):
        """Unique record identifier for serialization
        """
        return (self.filehash,)


    def is_image(self):
        """Is file object an image
        """
        return self.mimetype.startswith('image/')


    def is_video(self):
        """Is file object a video
        """
        return self.mimetype.startswith('video/')


    def get_filename(self):
        """File object filename
        """
        return os.path.basename(self.databits.name)


    def render(self, theme='default', classlist=None):
        """Render the instance as html
        """
        context = {
            'object': self,
            'media': None,
            'class': classlist,
        }
        if self.is_image():
            obj_type = 'image'
            items = []
            for name, _t, viewport_width in settings.IMAGE_SIZES:
                fieldobj = getattr(self, f'image_{name}')
                if not fieldobj:
                    break
                if not context['media']:
                    context['media'] = fieldobj
                else:
                    items.append((fieldobj, viewport_width + 1))
            if fieldobj:
                items.append((self.databits, settings.IMAGE_SIZE_MAX + 1))
            context['items'] = items
        elif self.is_video():
            obj_type = 'video'
        else:
            obj_type = 'link'
        return render_to_string(f'my_files/tpl_{obj_type}-{theme}.html',
                context)
