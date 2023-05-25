# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2023-05-13 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0015_courseoverview_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseoverview',
            name='duration',
        ),
        migrations.AddField(
            model_name='courseoverview',
            name='competences',
            field=models.TextField(null=True),
        ),
    ]