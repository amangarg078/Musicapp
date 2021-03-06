# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-11 23:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170212_0423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trackgenre',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='trackgenre',
            name='track',
        ),
        migrations.AddField(
            model_name='tracks',
            name='genres',
            field=models.ManyToManyField(related_name='tracks', to='app.Genres'),
        ),
        migrations.DeleteModel(
            name='TrackGenre',
        ),
    ]
