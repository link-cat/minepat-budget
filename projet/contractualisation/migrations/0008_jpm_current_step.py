# Generated by Django 5.1 on 2024-12-04 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractualisation', '0007_alter_piecejointe_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='jpm',
            name='current_step',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contractualisation.etapecontractualisation'),
        ),
    ]
