# Generated by Django 4.2 on 2023-04-08 01:43
# pylint:disable=line-too-long,missing-module-docstring,missing-class-docstring

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_front_content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frontcontent',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
