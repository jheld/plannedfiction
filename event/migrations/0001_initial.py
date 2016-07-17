# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-17 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('location', models.CharField(blank=True, max_length=250, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('order', models.PositiveIntegerField(blank=True, null=True)),
                ('characters', models.ManyToManyField(blank=True, null=True, to='subject.Character')),
            ],
        ),
    ]