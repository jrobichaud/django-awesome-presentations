# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-15 01:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing_migrations', '0005_migrate_to_kitten_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitten',
            name='name',
            field=models.CharField(default='', max_length=100, blank=True),
        ),
    ]