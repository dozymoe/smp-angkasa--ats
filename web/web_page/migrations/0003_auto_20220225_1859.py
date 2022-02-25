# Generated by Django 3.1 on 2022-02-25 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_page', '0002_auto_20220117_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='webpage',
            name='summary',
            field=models.TextField(default='', verbose_name='Summary'),
        ),
        migrations.AddField(
            model_name='webpage',
            name='summary_en',
            field=models.TextField(default='', null=True,
                verbose_name='Summary'),
        ),
        migrations.AddField(
            model_name='webpage',
            name='summary_ind',
            field=models.TextField(default='', null=True,
                verbose_name='Summary'),
        ),
    ]
