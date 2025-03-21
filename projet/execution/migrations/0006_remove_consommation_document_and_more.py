# Generated by Django 5.1 on 2025-02-20 07:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('execution', '0005_alter_historicaloperation_title_en_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consommation',
            name='document',
        ),
        migrations.RemoveField(
            model_name='historicalconsommation',
            name='document',
        ),
        migrations.CreateModel(
            name='PieceJointeConsommation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(blank=True, null=True, upload_to='documents/consommation/', verbose_name='Fichier')),
                ('date_upload', models.DateTimeField(auto_now_add=True, null=True, verbose_name="Date d'upload")),
                ('consommation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pieces_jointes', to='execution.consommation')),
            ],
        ),
    ]
