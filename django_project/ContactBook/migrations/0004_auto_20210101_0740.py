# Generated by Django 3.1.4 on 2021-01-01 07:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContactBook', '0003_auto_20201231_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='contact_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'", regex='^(\\+?1?)?\\d{9,15}$')]),
        ),
    ]
