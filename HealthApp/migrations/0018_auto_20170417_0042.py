# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-04-17 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthApp', '0017_auto_20170416_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medinfo',
            name='body_temp',
            field=models.IntegerField(default=0, verbose_name='Body Temperature'),
        ),
        migrations.AlterField(
            model_name='medinfo',
            name='diastolic_pressure',
            field=models.IntegerField(default=0, verbose_name='Diastolic Blood Pressure'),
        ),
        migrations.AlterField(
            model_name='medinfo',
            name='heart_rate',
            field=models.IntegerField(default=0, verbose_name='Heart Rate'),
        ),
        migrations.AlterField(
            model_name='medinfo',
            name='respiratory_rate',
            field=models.IntegerField(default=0, verbose_name='Respiratory Rate'),
        ),
        migrations.AlterField(
            model_name='medinfo',
            name='systolic_pressure',
            field=models.IntegerField(default=0, verbose_name='Systolic Blood Pressure'),
        ),
    ]
