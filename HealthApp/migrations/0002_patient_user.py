# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-03-01 01:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital', models.CharField(max_length=50)),
                ('doctor', models.CharField(max_length=50)),
                ('desired_hospital', models.CharField(max_length=50, verbose_name='Desired Hospital')),
                ('e_cont_fname', models.CharField(max_length=50, verbose_name='Emergency Contact: First Name')),
                ('e_cont_lname', models.CharField(max_length=50, verbose_name='Emergency Contact: Last Name')),
                ('e_cont_home_phone', models.BigIntegerField(help_text='No spaces or dashes', verbose_name='Emergency Contact: Home Phone')),
                ('e_cont_cell_phone', models.BigIntegerField(help_text='No spaces or dashes', verbose_name='Emergency Contact: Cell Phone')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('date_of_birth', models.DateField(verbose_name='Date of Birth')),
                ('social', models.IntegerField(verbose_name='Social Security Number:')),
                ('address_street', models.CharField(max_length=50, verbose_name='Street')),
                ('address_city', models.CharField(max_length=50, verbose_name='City')),
                ('address_state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=50, verbose_name='State')),
                ('address_zip', models.IntegerField(verbose_name='Zip Code')),
                ('home_phone', models.BigIntegerField(help_text='No spaces or dashes', verbose_name='Home Phone')),
                ('cell_phone', models.BigIntegerField(help_text='No spaces or dashes', verbose_name='Cell Phone')),
            ],
        ),
    ]
