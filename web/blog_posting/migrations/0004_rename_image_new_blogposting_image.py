# Generated by Django 4.2 on 2023-04-07 11:51
# pylint:disable=line-too-long,missing-module-docstring,missing-class-docstring

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_posting', '0003_remove_blogposting_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogposting',
            old_name='image_new',
            new_name='image',
        ),
    ]
