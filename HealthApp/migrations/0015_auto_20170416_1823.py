# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-04-16 18:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HealthApp', '0014_auto_20170415_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HealthApp.Doctor', verbose_name='Doctor'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HealthApp.Patient', verbose_name='Patient'),
        ),
    ]
