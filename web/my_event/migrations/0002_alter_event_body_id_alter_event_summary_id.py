# Generated by Django 4.2 on 2023-04-08 01:34
# pylint:disable=line-too-long,missing-module-docstring,missing-class-docstring

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='body_id',
            field=models.TextField(blank=True, verbose_name='Body'),
        ),
        migrations.AlterField(
            model_name='event',
            name='summary_id',
            field=models.TextField(blank=True, verbose_name='Summary'),
        ),
    ]
