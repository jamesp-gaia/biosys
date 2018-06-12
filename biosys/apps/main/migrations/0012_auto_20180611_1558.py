# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-11 07:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_record_client_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=main.models.media_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='datasetfile',
            name='dataset',
        ),
        migrations.RemoveField(
            model_name='datasetfile',
            name='uploaded_by',
        ),
        migrations.AlterField(
            model_name='record',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Site'),
        ),
        migrations.DeleteModel(
            name='DatasetFile',
        ),
        migrations.AddField(
            model_name='media',
            name='record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Record'),
        ),
    ]
