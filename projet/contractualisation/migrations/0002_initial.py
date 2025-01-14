# Generated by Django 5.1 on 2025-01-13 18:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contractualisation', '0001_initial'),
        ('setting', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='etapecontractualisation',
            name='tache',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projet', to='setting.tache'),
        ),
        migrations.AddField(
            model_name='historicaletapecontractualisation',
            name='etape',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contractualisation.etape'),
        ),
        migrations.AddField(
            model_name='historicaletapecontractualisation',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaletapecontractualisation',
            name='tache',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='setting.tache'),
        ),
        migrations.AddField(
            model_name='maturation',
            name='tache',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setting.tache'),
        ),
        migrations.AddField(
            model_name='piecejointe',
            name='etape',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pieces_jointes', to='contractualisation.etape'),
        ),
        migrations.AddField(
            model_name='piecejointecontractualisation',
            name='etape_contractualisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pieces_jointes', to='contractualisation.etapecontractualisation'),
        ),
        migrations.AddField(
            model_name='ppm',
            name='tache',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setting.tache'),
        ),
        migrations.AddConstraint(
            model_name='etapecontractualisation',
            constraint=models.UniqueConstraint(fields=('tache', 'etape'), name='unique_tache_etape'),
        ),
    ]
