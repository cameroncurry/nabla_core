# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 18:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nabla_core', '0002_auto_20171030_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qtaccess',
            name='access_token',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='qtaccess',
            name='refresh_token',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='qtaccess',
            name='token_type',
            field=models.CharField(max_length=64),
        ),
    ]
