# Generated by Django 3.2.5 on 2021-10-08 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dockers', '0009_alter_dockers_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='dockers',
            name='refreshNumber',
            field=models.BigIntegerField(default=0),
        ),
    ]
