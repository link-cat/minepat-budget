# Generated by Django 5.1 on 2025-02-11 10:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('execution', '0002_groupe_rename_montant_consommation_montant_engage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='groupe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='execution.groupe'),
        ),
    ]
