# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-27 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='auth',
            field=models.SmallIntegerField(default=0, verbose_name='认证状态'),
        ),
    ]
