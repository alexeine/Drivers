# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20170313_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='area',
            field=models.IntegerField(),
        ),
    ]