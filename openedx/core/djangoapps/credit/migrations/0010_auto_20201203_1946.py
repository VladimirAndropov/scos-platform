# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-12-03 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0009_auto_20200902_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditconfig',
            name='cache_ttl',
            field=models.PositiveIntegerField(default=0, help_text='Specified in seconds. Enable caching by setting this to a value greater than 0.', verbose_name='Cache Time To Live'),
        ),
    ]
