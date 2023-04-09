"""Alter image field attached to blog post into MyFile instance

The goal is complete image/video processing on one module, my_files.
Also auto deleting of old files.
"""
# Generated by Django 4.2 on 2023-04-06 05:53

import os
#-
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db import migrations, models
import django.db.models.deletion
from translated_fields import to_attribute
#-
from my_files.signals import file_updating, file_updated

def copy_image_into_myfile(apps, schema_editor):
    """Copy file from image field to image_new field (MyFile)
    """
    BlogPosting = apps.get_model('blog_posting', 'BlogPosting')
    MyFile = apps.get_model('my_files', 'MyFile')

    for blog in BlogPosting.objects.filter(image__isnull=False):
        fieldobj = blog.image
        fieldobj.open()
        try:
            fileobj = UploadedFile(fieldobj.file,
                    os.path.basename(fieldobj.name), size=fieldobj.size)

            data = {
                'databits': fileobj,
                'created_by': blog.created_by,
            }
            for lang_code, _ in settings.LANGUAGES:
                data[to_attribute('description', lang_code)] =\
                        getattr(blog, to_attribute('title', lang_code))

            newfile = MyFile(**data)
            file_updating(None, newfile)
            newfile.save()
            file_updated(None, newfile)

            blog.image_new = newfile
            blog.save()
        finally:
            fieldobj.close()


def copy_myfile_into_image(apps, schema_editor):
    """Copy file from image_new field (MyFile) to image field
    """
    BlogPosting = apps.get_model('blog_posting', 'BlogPosting')

    for blog in BlogPosting.objects.filter(image_new__isnull=False):
        fieldobj = blog.image_new.databits
        fieldobj.open()
        try:
            fileobj = UploadedFile(fieldobj.file,
                    os.path.basename(fieldobj.name), size=fieldobj.size)
            blog.image = fileobj
            blog.save()
        finally:
            fieldobj.close()


class Migration(migrations.Migration):
    """Automatically generated migration script
    """
    dependencies = [
        ('my_files', '0001_initial'),
        ('blog_posting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogposting',
            name='image_new',
            field=models.ForeignKey(null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='my_files.myfile', verbose_name='Image'),
        ),
        migrations.RunPython(copy_image_into_myfile, copy_myfile_into_image),
    ]
