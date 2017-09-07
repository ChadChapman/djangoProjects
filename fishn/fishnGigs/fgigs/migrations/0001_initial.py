# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-05 23:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crew_text', models.CharField(max_length=200)),
                ('crew_looks', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Fishery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description_text', models.CharField(max_length=200)),
                ('opening_date', models.DateTimeField(verbose_name='season start date')),
            ],
        ),
        migrations.AddField(
            model_name='crew',
            name='crew_fishery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fgigs.Fishery'),
        ),
    ]