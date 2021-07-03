# Generated by Django 3.1 on 2021-06-29 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_files', '0002_auto_20210628_0534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myfile',
            name='image',
        ),
        migrations.RemoveField(
            model_name='myfile',
            name='image_height',
        ),
        migrations.RemoveField(
            model_name='myfile',
            name='image_width',
        ),
        migrations.AlterField(
            model_name='myfile',
            name='databits',
            field=models.FileField(upload_to='files/original/',
                verbose_name='Content'),
        ),
    ]
