# Generated by Django 3.1.4 on 2020-12-31 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContactBook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='phoneNumber',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
