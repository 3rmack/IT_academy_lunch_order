# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 08:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish', models.CharField(max_length=100)),
                ('byr', models.IntegerField(blank=True, null=True)),
                ('byn', models.FloatField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=300)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
