# Generated by Django 3.2.5 on 2021-08-05 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0008_auto_20200925_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfrequest',
            name='image',
            field=models.ImageField(help_text='Optional title image of the songbook', null=True, upload_to='uploads/', verbose_name='Title Image'),
        ),
        migrations.AddField(
            model_name='pdfrequest',
            name='show_date',
            field=models.BooleanField(default=True, help_text='True, if the date should be included in the final PDF', verbose_name='Show date'),
        ),
        migrations.AlterField(
            model_name='pdfrequest',
            name='filename',
            field=models.CharField(help_text='Filename of the generated PDF, please do not include .pdf', max_length=30, null=True, verbose_name='File name'),
        ),
        migrations.AlterField(
            model_name='pdfrequest',
            name='name',
            field=models.CharField(default="Jerry's songs", help_text='Name to be used on the title page of the PDF', max_length=100, verbose_name='Name'),
        ),
    ]
