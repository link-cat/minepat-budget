# Generated by Django 5.1 on 2025-01-14 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractualisation', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapecontractualisation',
            name='date_saisine',
            field=models.DateField(blank=True, null=True, verbose_name='Date de saisine'),
        ),
        migrations.AddField(
            model_name='historicaletapecontractualisation',
            name='date_saisine',
            field=models.DateField(blank=True, null=True, verbose_name='Date de saisine'),
        ),
    ]