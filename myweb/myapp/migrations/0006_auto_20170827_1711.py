# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-27 09:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20170827_1710'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock_base',
            old_name='industory',
            new_name='industry',
        ),
    ]
