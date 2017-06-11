# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-10 14:20
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import escrow.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Escrow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=250, null=True)),
                ('source', models.CharField(blank=True, max_length=250, null=True)),
                ('destination', models.CharField(blank=True, max_length=250, null=True)),
                ('amount', escrow.models.MoneyField(decimal_places=18, default=Decimal('0'), max_digits=28)),
                ('currency', models.CharField(blank=True, max_length=12, null=True)),
                ('description', models.TextField(blank=True, default='', max_length=500, null=True)),
                ('expiry', models.DateTimeField()),
                ('deposit_id', models.CharField(blank=True, max_length=64, null=True)),
                ('deposit_status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Complete', 'Complete'), ('Failed', 'Failed'), ('Deleted', 'Deleted'), ('Cancelled', 'Cancelled'), ('Expired', 'Expired'), ('Reversed', 'Reversed'), ('Escrowed', 'Escrowed'), ('Released', 'Released'), ('Disputed', 'Disputed'), ('Expired', 'Expired')], default='Pending', max_length=24, null=True)),
                ('transfer_id', models.CharField(blank=True, max_length=64, null=True)),
                ('transfer_status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Complete', 'Complete'), ('Failed', 'Failed'), ('Deleted', 'Deleted'), ('Cancelled', 'Cancelled'), ('Expired', 'Expired'), ('Reversed', 'Reversed'), ('Escrowed', 'Escrowed'), ('Released', 'Released'), ('Disputed', 'Disputed'), ('Expired', 'Expired')], default='Pending', max_length=24, null=True)),
                ('created', models.DateTimeField(db_index=True)),
                ('updated', models.DateTimeField()),
            ],
        ),
    ]
