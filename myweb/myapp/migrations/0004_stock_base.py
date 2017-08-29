# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-27 08:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20170827_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock_base',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('industory', models.CharField(max_length=32)),
                ('area', models.CharField(max_length=32)),
                ('pe', models.CharField(max_length=32)),
                ('outstanding', models.CharField(max_length=32)),
                ('totals', models.CharField(max_length=32)),
                ('totalAssets', models.CharField(max_length=32)),
                ('liquidAssets', models.CharField(max_length=32)),
                ('fixedAssets', models.CharField(max_length=32)),
                ('reserved', models.CharField(max_length=32)),
                ('reservedPerShare', models.CharField(max_length=32)),
                ('esp', models.CharField(max_length=32)),
                ('bvps', models.CharField(max_length=32)),
                ('pb', models.CharField(max_length=32)),
                ('timeToMarket', models.CharField(max_length=32)),
                ('undp', models.CharField(max_length=32)),
                ('perundp', models.CharField(max_length=32)),
                ('rev', models.CharField(max_length=32)),
                ('profit', models.CharField(max_length=32)),
                ('gpr', models.CharField(max_length=32)),
                ('npr', models.CharField(max_length=32)),
                ('holders', models.CharField(max_length=32)),
            ],
        ),
    ]
