# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-03-06 01:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='primary_nurse',
        ),
    ]