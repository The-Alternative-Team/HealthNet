# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-03-04 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userMail', models.CharField(default='', max_length=100, verbose_name='User Email')),
                ('time', models.DateTimeField(default=None, verbose_name='Date Logged')),
                ('action', models.CharField(default='', max_length=1000, verbose_name='Action')),
            ],
        ),
    ]