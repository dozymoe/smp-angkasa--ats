# Generated by Django 3.1.7 on 2021-02-25 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_posting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogposting',
            name='body_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='blogposting',
            name='body_ind',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='blogposting',
            name='slug_en',
            field=models.SlugField(blank=True,
                help_text='Human friendly unique url to identify the content, will automatically be filled if left empty.', # pylint:disable=line-too-long
                max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='blogposting',
            name='slug_ind',
            field=models.SlugField(blank=True,
                help_text='Human friendly unique url to identify the content, will automatically be filled if left empty.', # pylint:disable=line-too-long
                max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='blogposting',
            name='summary_en',
            field=models.TextField(max_length=155, null=True),
        ),
        migrations.AddField(
            model_name='blogposting',
            name='summary_ind',
            field=models.TextField(max_length=155, null=True),
        ),
        migrations.AddField(
            model_name='blogposting',
            name='title_en',
            field=models.CharField(max_length=65, null=True),
        ),
        migrations.AddField(
            model_name='blogposting',
            name='title_ind',
            field=models.CharField(max_length=65, null=True),
        ),
    ]
