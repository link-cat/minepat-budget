# Generated by Django 5.1 on 2024-11-28 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractualisation', '0005_remove_etapecontractualisation_document_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piecejointe',
            name='date_upload',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name="Date d'upload"),
        ),
    ]
