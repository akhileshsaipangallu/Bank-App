# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 06:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_auto_20170306_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
