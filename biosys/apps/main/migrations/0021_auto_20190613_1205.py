# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-13 04:05
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_form_dataset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='layout',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
