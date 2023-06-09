# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2021-05-31 09:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0011_auto_20201227_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditconfig',
            name='cache_ttl',
            field=models.PositiveIntegerField(default=0, help_text='Specified in seconds. Enable caching by setting this to a value greater than 0.', verbose_name='Cache Time To Live'),
        ),
    ]
