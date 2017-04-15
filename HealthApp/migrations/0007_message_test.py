# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-04-15 16:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HealthApp', '0006_auto_20170408_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default='', max_length=120, verbose_name='subject')),
                ('body', models.TextField(blank=True, verbose_name='body')),
                ('sender', models.CharField(default='', max_length=100, verbose_name='sender email')),
                ('recipient', models.CharField(default='', max_length=100, verbose_name='recipient email')),
                ('sent_at', models.DateTimeField(verbose_name='sent at')),
                ('read_at', models.DateTimeField(verbose_name='read at')),
                ('unread', models.BooleanField(verbose_name='unread')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Test Date')),
                ('notes', models.CharField(default='', max_length=1000, verbose_name='Notes')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HealthApp.Doctor', verbose_name='Doctor')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HealthApp.UploadedFile', verbose_name='Test File')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HealthApp.Patient', verbose_name='Patient')),
            ],
            options={
                'verbose_name': 'Test',
                'verbose_name_plural': 'Tests',
            },
        ),
    ]