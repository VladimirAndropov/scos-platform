# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-09-02 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_admin', '0010_auto_20200902_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiaccessrequest',
            name='reason',
            field=models.TextField(help_text='The reason this user wants to access the API.'),
        ),
        migrations.AlterField(
            model_name='apiaccessrequest',
            name='status',
            field=models.CharField(choices=[(b'pending', 'Pending'), (b'denied', 'Denied'), (b'approved', 'Approved')], db_index=True, default=b'pending', help_text='Status of this API access request', max_length=255),
        ),
        migrations.AlterField(
            model_name='apiaccessrequest',
            name='website',
            field=models.URLField(help_text='The URL of the website associated with this API user.'),
        ),
    ]
