# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 03:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_delete_chainidtopersistentid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChainIdToPersistentId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.CharField(max_length=32, unique=True)),
            ],
        ),
    ]
