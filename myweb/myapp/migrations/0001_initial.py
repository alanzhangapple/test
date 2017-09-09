# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-09-07 02:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analyst',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('company', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Analyst_power_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('company', models.CharField(max_length=32)),
                ('power_30', models.FloatField()),
                ('power_60', models.FloatField()),
                ('power_90', models.FloatField()),
                ('power_180', models.FloatField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Analyst_power_today',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('company', models.CharField(max_length=32)),
                ('power_30', models.FloatField()),
                ('power_30_high', models.FloatField(default=0.0)),
                ('power_60', models.FloatField()),
                ('power_60_high', models.FloatField(default=0.0)),
                ('power_90', models.FloatField()),
                ('power_90_high', models.FloatField(default=0.0)),
                ('power_180', models.FloatField()),
                ('power_180_high', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='CSH_price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('date', models.CharField(max_length=32)),
                ('open', models.FloatField()),
                ('close', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('volume', models.FloatField()),
                ('code', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Power_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100, verbose_name='ICG')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Scrapy_B',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True, null=True, verbose_name='ICG')),
            ],
        ),
        migrations.CreateModel(
            name='Scrapy_C',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100, verbose_name='ICG')),
                ('name', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True, null=True, verbose_name='ICG')),
            ],
        ),
        migrations.CreateModel(
            name='Scrapy_D',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('company', models.CharField(default='ICG', max_length=100)),
                ('name', models.CharField(default='ICG', max_length=100)),
                ('content', models.TextField(blank=True, null=True, verbose_name='ICG')),
                ('boolean_str', models.IntegerField(default=0)),
                ('price_publish_date', models.FloatField(default=0.0)),
                ('delta_30_date', models.DateField(default=datetime.date(2017, 9, 7))),
                ('price_delta_30_date', models.FloatField(default=0.0)),
                ('charge_delta_30_date', models.FloatField(default=0.0)),
                ('hightest_price_delta_30_date', models.FloatField(default=0.0)),
                ('delta_60_date', models.DateField(default=datetime.date(2017, 9, 7))),
                ('price_delta_60_date', models.FloatField(default=0.0)),
                ('charge_delta_60_date', models.FloatField(default=0.0)),
                ('hightest_price_delta_60_date', models.FloatField(default=0.0)),
                ('delta_90_date', models.DateField(default=datetime.date(2017, 9, 7))),
                ('price_delta_90_date', models.FloatField(default=0.0)),
                ('charge_delta_90_date', models.FloatField(default=0.0)),
                ('hightest_price_delta_90_date', models.FloatField(default=0.0)),
                ('delta_180_date', models.DateField(default=datetime.date(2017, 9, 7))),
                ('price_delta_180_date', models.FloatField(default=0.0)),
                ('charge_delta_180_date', models.FloatField(default=0.0)),
                ('hightest_price_delta_180_date', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Stock_base',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32, null=True)),
                ('name', models.CharField(max_length=32, null=True)),
                ('industry', models.CharField(max_length=32, null=True)),
                ('area', models.CharField(max_length=32, null=True)),
                ('pe', models.FloatField(null=True)),
                ('outstanding', models.FloatField(null=True)),
                ('totals', models.FloatField(null=True)),
                ('totalAssets', models.FloatField(null=True)),
                ('liquidAssets', models.FloatField(null=True)),
                ('fixedAssets', models.FloatField(null=True)),
                ('reserved', models.FloatField(null=True)),
                ('reservedPerShare', models.FloatField(null=True)),
                ('esp', models.FloatField(null=True)),
                ('bvps', models.FloatField(null=True)),
                ('pb', models.FloatField(null=True)),
                ('timeToMarket', models.IntegerField(null=True)),
                ('undp', models.FloatField(null=True)),
                ('perundp', models.FloatField(null=True)),
                ('rev', models.FloatField(null=True)),
                ('profit', models.FloatField(null=True)),
                ('gpr', models.FloatField(null=True)),
                ('npr', models.FloatField(null=True)),
                ('holders', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock_detail_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date(2017, 9, 7))),
                ('index', models.IntegerField()),
                ('code', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('changepercent', models.FloatField()),
                ('trade', models.FloatField()),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('settlement', models.FloatField()),
                ('volume', models.IntegerField()),
                ('turnoverratio', models.FloatField()),
                ('amount', models.IntegerField()),
                ('per', models.FloatField()),
                ('pb', models.FloatField()),
                ('mktcap', models.FloatField()),
                ('nmc', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Stock_detail_today',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('code', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('changepercent', models.FloatField()),
                ('trade', models.FloatField()),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('settlement', models.FloatField()),
                ('volume', models.IntegerField()),
                ('turnoverratio', models.FloatField()),
                ('amount', models.IntegerField()),
                ('per', models.FloatField()),
                ('pb', models.FloatField()),
                ('mktcap', models.FloatField()),
                ('nmc', models.FloatField()),
            ],
        ),
    ]