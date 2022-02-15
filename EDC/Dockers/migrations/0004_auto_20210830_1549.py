# Generated by Django 3.2.5 on 2021-08-30 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dockers', '0003_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='dockers',
            name='createdDate',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dockers',
            name='email',
            field=models.EmailField(default='d@informatica.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dockers',
            name='expiryDate',
            field=models.CharField(default='d', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dockers',
            name='pVersion',
            field=models.CharField(default='d', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dockers',
            name='region',
            field=models.CharField(default='d', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dockers',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dockers',
            name='CaseNo',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='dockers',
            name='Host',
            field=models.GenericIPAddressField(),
        ),
    ]