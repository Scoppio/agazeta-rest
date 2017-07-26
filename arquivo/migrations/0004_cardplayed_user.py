# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 07:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('arquivo', '0003_auto_20170717_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardplayed',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
