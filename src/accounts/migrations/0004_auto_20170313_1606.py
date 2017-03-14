# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 16:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='teamInvestment',
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]