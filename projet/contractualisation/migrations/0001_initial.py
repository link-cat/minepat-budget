# Generated by Django 5.1 on 2024-10-15 14:24

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Etape',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EtapeContractualisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_prevue', models.DateField(verbose_name='Date prévue')),
                ('date_effective', models.DateField(blank=True, null=True, verbose_name='Date effective')),
                ('observations', models.TextField(blank=True, null=True)),
                ('document', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('ecart_jours', models.IntegerField(blank=True, editable=False, null=True)),
                ('etape', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractualisations', to='contractualisation.etape')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalEtapeContractualisation',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date_prevue', models.DateField(verbose_name='Date prévue')),
                ('date_effective', models.DateField(blank=True, null=True, verbose_name='Date effective')),
                ('observations', models.TextField(blank=True, null=True)),
                ('document', models.TextField(blank=True, max_length=100, null=True)),
                ('ecart_jours', models.IntegerField(blank=True, editable=False, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('etape', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contractualisation.etape')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical etape contractualisation',
                'verbose_name_plural': 'historical etape contractualisations',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
