# Generated by Django 5.1 on 2024-12-21 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractualisation', '0018_etapecontractualisation_unique_tache_etape'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapecontractualisation',
            name='chef_service_marche',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='etapecontractualisation',
            name='ingenieur_marche',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='etapecontractualisation',
            name='numero_marche',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='etapecontractualisation',
            name='prestataire',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='etapecontractualisation',
            name='taux_exec_physique',
            field=models.FloatField(blank=True, null=True, verbose_name="Taux d'execution physique"),
        ),
        migrations.AddField(
            model_name='historicaletapecontractualisation',
            name='chef_service_marche',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicaletapecontractualisation',
            name='ingenieur_marche',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicaletapecontractualisation',
            name='numero_marche',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicaletapecontractualisation',
            name='prestataire',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicaletapecontractualisation',
            name='taux_exec_physique',
            field=models.FloatField(blank=True, null=True, verbose_name="Taux d'execution physique"),
        ),
    ]
