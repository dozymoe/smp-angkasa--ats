import os
#-
from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import rules
from rules.contrib.models import RulesModel


class MyFileManager(models.Manager):
    def get_by_natural_key(self, key):
        return self.get(filehash=key)


class MyFile(DirtyFieldsMixin, RulesModel):
    filehash = models.CharField(verbose_name=_("Title"), max_length=65,
            editable=False)
    mimetype = models.CharField(verbose_name=_("Mime Type"), max_length=50,
            editable=False)
    description = models.TextField(verbose_name=_("Description"))
    alt_text  = models.TextField(verbose_name=_("Alternate Text (alt text)"),
            null=True, blank=True,
            help_text=_("Only need to fill this if you were uploading "
            "an image."))
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

    objects = MyFileManager()


    class Meta:

        get_latest_by = 'created_at'
        ordering = ['-created_at']
        rules_permissions = {
            'add': rules.is_authenticated,
            'read': rules.always_allow,
            'change': rules.is_staff,
            'delete': rules.is_staff,
        }


    def __str__(self): # pylint:disable=invalid-str-returned
        return self.filehash


    def get_absolute_url(self):
        if self.is_image():
            return reverse('MyFile:Display', args=(self.pk, 'xs'))
        return reverse('MyFile:Display', args=(self.pk,))


    def get_natural_key(self):
        return (self.filehash,)


    def is_image(self):
        return self.mimetype.startswith('image/')


    def get_filename(self):
        return os.path.basename(self.databits.name)


    def get_html_attr_srcset(self):
        attribute_value = []
        for name, size, _ in settings.IMAGE_SIZES:
            imgfield = getattr(self, f'image_{name}')
            if not imgfield:
                continue
            attribute_value.append('%s %sw' % (
                    reverse('MyFile:Display', args=(self.pk, name)), size[0]))
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
