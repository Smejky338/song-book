# Generated by Django 3.2.5 on 2021-08-06 15:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0010_alter_pdfrequest_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfsong',
            name='song_number',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Song number'),
        ),
    ]