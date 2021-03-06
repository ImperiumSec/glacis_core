# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-09 18:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glacis_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.TextField()),
                ('name', models.TextField(blank=True, null=True)),
                ('trapdoor_value', models.TextField()),
                ('trapdoor_mechanism', models.TextField(choices=[('BCRYPT', 'BCRYPT')])),
                ('trapdoor_data', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glacis_core.Entity')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glacis_core.Organisation')),
            ],
        ),
    ]
