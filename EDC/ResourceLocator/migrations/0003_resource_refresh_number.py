# Generated by Django 3.2.5 on 2021-08-01 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ResourceLocator', '0002_alter_resource_type_scanner_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='Refresh_Number',
            field=models.BigIntegerField(default=0),
        ),
    ]
