# Generated by Django 5.1 on 2024-09-27 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('execution', '0006_alter_estexecuteefcpdr_gc_category_ressource_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estexecuteefcpdr',
            name='gc_category_ressource',
        ),
        migrations.RemoveField(
            model_name='estexecuteegcautres',
            name='gc_category_ressource',
        ),
        migrations.RemoveField(
            model_name='estexecuteegcsub',
            name='gc_category_ressource',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteefcpdr',
            name='gc_category_ressource',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteegcautres',
            name='gc_category_ressource',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteegcsub',
            name='gc_category_ressource',
        ),
    ]
