# Generated by Django 3.2.5 on 2021-09-12 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='HowHelped',
            field=models.TextField(max_length=700),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='WhatImproved',
            field=models.TextField(max_length=700),
        ),
    ]
