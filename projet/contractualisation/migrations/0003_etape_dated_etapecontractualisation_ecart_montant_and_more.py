# Generated by Django 5.1 on 2024-10-17 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractualisation', '0002_etapecontractualisation_is_finished_and_more'),
        ('setting', '0015_historicaltache_latitude_historicaltache_longitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='etape',
            name='dated',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='etapecontractualisation',
            name='ecart_montant',
            field=models.FloatField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='etapecontractualisation',
            name='montant_prevu',
            field=models.FloatField(blank=True, null=True, verbose_name='Montant prévisionnel'),
        ),
        migrations.AddField(
            model_name='etapecontractualisation',
            name='montant_reel',
            field=models.FloatField(blank=True, null=True, verbose_name='Montant réel'),
        ),
        migrations.AddField(
            model_name='etapecontractualisation',
            name='taux_consomation',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Taux de consommation'),
        ),
        migrations.AddField(
            model_name='historicaletapecontractualisation',
            name='ecart_montant',
            field=models.FloatField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='historicaletapecontractualisation',
            name='montant_prevu',
            field=models.FloatField(blank=True, null=True, verbose_name='Montant prévisionnel'),
        ),
        migrations.AddField(
            model_name='historicaletapecontractualisation',
            name='montant_reel',
            field=models.FloatField(blank=True, null=True, verbose_name='Montant réel'),
        ),
        migrations.AddField(
            model_name='historicaletapecontractualisation',
            name='taux_consomation',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Taux de consommation'),
        ),
        migrations.AlterField(
            model_name='etapecontractualisation',
            name='date_prevue',
            field=models.DateField(blank=True, null=True, verbose_name='Date prévue'),
        ),
        migrations.AlterField(
            model_name='historicaletapecontractualisation',
            name='date_prevue',
            field=models.DateField(blank=True, null=True, verbose_name='Date prévue'),
        ),
        migrations.CreateModel(
            name='JPM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nature_prestations', models.CharField(max_length=50, verbose_name='Nature des prestations')),
                ('montant_previsionnel', models.FloatField(verbose_name='Montant prévisionnel (FCFA)')),
                ('source_financement', models.CharField(max_length=255, verbose_name='Source de financement')),
                ('autorite_contractante', models.CharField(max_length=255, verbose_name='Autorité Contractante / Administration bénéficiaire')),
                ('mode_consultation', models.CharField(max_length=255, verbose_name='Mode de consultation')),
                ('date_lancement_consultation', models.DateField(verbose_name='Date de lancement de la consultation')),
                ('date_attribution_marche', models.DateField(verbose_name="Date d'attribution du marché")),
                ('date_signature_marche', models.DateField(verbose_name='Date de signature du marché')),
                ('date_demarrage_prestations', models.DateField(verbose_name='Date de démarrage des prestations')),
                ('date_reception_prestations', models.DateField(verbose_name='Date de réception des prestations')),
                ('tache', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setting.tache')),
            ],
        ),
        migrations.CreateModel(
            name='PPM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nature_prestations', models.CharField(max_length=255)),
                ('montant_previsionnel', models.FloatField()),
                ('source_financement', models.CharField(max_length=255)),
                ('autorite_contractante', models.CharField(max_length=255)),
                ('mode_consultation_solicite', models.CharField(max_length=255)),
                ('procedure', models.CharField(max_length=255)),
                ('saisine_ac', models.DateField()),
                ('saisine_cpm', models.DateField()),
                ('examen_dao_cpm', models.DateField()),
                ('saisine_cccm_dao', models.DateField()),
                ('avis_cccm_dao', models.CharField(max_length=255)),
                ('non_objection_bf_1', models.CharField(max_length=255)),
                ('date_publication_ao', models.DateField()),
                ('depouillement_offres', models.DateField()),
                ('analyse_offres_techniques', models.DateField()),
                ('examen_rapport_offres_techniques', models.DateField()),
                ('non_objection_bf_2', models.CharField(max_length=255)),
                ('ouverture_offres_financieres', models.DateField()),
                ('analyse_offres_financieres_synthese', models.DateField()),
                ('proposition_attribution_cpm', models.CharField(max_length=255)),
                ('saisine_cccm_attribution', models.DateField()),
                ('avis_cccm_attribution', models.CharField(max_length=255)),
                ('non_objection_bf_3', models.CharField(max_length=255)),
                ('publication_resultats', models.DateField()),
                ('notification_decision_attribution', models.DateField()),
                ('preparation_projet_marche', models.DateField()),
                ('saisine_cpm_marche', models.DateField()),
                ('examen_projet_marche', models.DateField()),
                ('saisine_cccm_marche', models.DateField()),
                ('avis_cccm_projet_marche_gg', models.CharField(max_length=255)),
                ('non_objection_bf_4', models.CharField(max_length=255)),
                ('date_signature_marche', models.DateField()),
                ('notification_marche', models.DateField()),
                ('demarrage_prestations', models.DateField()),
                ('reception_provisoire', models.DateField()),
                ('reception_definitive', models.DateField()),
                ('tache', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setting.tache')),
            ],
        ),
    ]
