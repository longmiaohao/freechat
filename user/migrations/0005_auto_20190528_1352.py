# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-28 05:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190528_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmpuserinfo',
            name='verification_code',
            field=models.CharField(max_length=32, verbose_name='验证码'),
        ),
    ]
