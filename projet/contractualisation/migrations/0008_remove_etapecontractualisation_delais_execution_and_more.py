# Generated by Django 5.1 on 2025-02-01 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contractualisation', '0007_piecejointematuration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etapecontractualisation',
            name='delais_execution',
        ),
        migrations.RemoveField(
            model_name='historicaletapecontractualisation',
            name='delais_execution',
        ),
    ]
