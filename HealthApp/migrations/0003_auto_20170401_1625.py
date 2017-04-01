# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-04-01 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthApp', '0002_remove_patient_primary_nurse'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('file', models.FileField(upload_to='/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='logentry',
            options={'verbose_name': 'Log entry', 'verbose_name_plural': 'Log entries'},
        ),
    ]