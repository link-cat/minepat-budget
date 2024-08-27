# Generated by Django 5.1 on 2024-08-27 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0009_historicalnaturedepense_code_naturedepense_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmodegestion',
            name='code',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalmodegestion',
            name='source',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicaltyperessource',
            name='code',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modegestion',
            name='code',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modegestion',
            name='source',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='typeressource',
            name='code',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]