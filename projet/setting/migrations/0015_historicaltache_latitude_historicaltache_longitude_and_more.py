# Generated by Django 5.1 on 2024-10-15 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0014_delete_etapecontractualisation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltache',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicaltache',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tache',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tache',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]