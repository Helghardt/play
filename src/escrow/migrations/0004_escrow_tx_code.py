# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-10 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escrow', '0003_auto_20170610_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='escrow',
            name='tx_code',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]