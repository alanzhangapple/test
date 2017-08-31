# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-31 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20170831_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrapy_b',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='ICG'),
        ),
        migrations.AddField(
            model_name='scrapy_c',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='ICG'),
        ),
        migrations.AddField(
            model_name='scrapy_d',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='ICG'),
        ),
        migrations.AddField(
            model_name='scrapy_d',
            name='hightest_price_delta_180_date',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='scrapy_d',
            name='hightest_price_delta_30_date',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='scrapy_d',
            name='hightest_price_delta_60_date',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='scrapy_d',
            name='hightest_price_delta_90_date',
            field=models.FloatField(default=0.0),
        ),
    ]
