# Generated by Django 4.0.4 on 2022-04-20 05:03
# pylint:disable=line-too-long

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
