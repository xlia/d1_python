# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-17 07:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20170821_2129'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scienceobject',
            options={'ordering': ['-modified_timestamp', 'id']},
        ),
        migrations.AlterField(
            model_name='chain',
            name='sid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chain_sid', to='app.IdNamespace', unique=True),
        ),
    ]
