# Generated by Django 3.1 on 2022-03-01 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_slide', '0002_auto_20220208_0315'),
    ]

    operations = [
        migrations.AddField(
            model_name='myslide',
            name='position',
            field=models.PositiveIntegerField(db_index=True, default=0,
                verbose_name='Position'),
        ),
    ]
