# Generated by Django 5.1 on 2025-04-24 18:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('execution', '0010_alter_operation_tache'),
        ('setting', '0006_alter_historicaltache_type_execution_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='tache',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setting.tache'),
        ),
    ]
