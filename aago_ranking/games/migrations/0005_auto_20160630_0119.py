# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-30 01:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_game_unrated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='result',
            field=models.CharField(choices=[('black', 'Black Wins'), ('white', 'White Wins'), ('draw', 'Draw'), ('both_lose', 'Both lose')], max_length=16),
        ),
        migrations.AlterField(
            model_name='game',
            name='win_reason',
            field=models.CharField(choices=[('points', 'Points'), ('resignation', 'Resignation'), ('walkover', 'Walkover'), ('timeout', 'Timeout'), ('other', 'Other')], max_length=16),
        ),
    ]
