# Generated by Django 5.1 on 2024-08-18 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0007_alter_estexecuteefcpdr_dateimport_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estexecuteefcpdr',
            name='etape_execution_glob',
        ),
        migrations.RemoveField(
            model_name='estexecuteefcpdr',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='estexecuteefcpdr',
            name='tache',
        ),
        migrations.RemoveField(
            model_name='estexecuteefcptdd',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='estexecuteefcptdd',
            name='tache',
        ),
        migrations.RemoveField(
            model_name='estexecuteegcautres',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='estexecuteegcautres',
            name='tache',
        ),
        migrations.RemoveField(
            model_name='estexecuteegcsub',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='estexecuteegcsub',
            name='tache',
        ),
        migrations.RemoveField(
            model_name='estexecuteemodegestion',
            name='etape_execution_glob',
        ),
        migrations.RemoveField(
            model_name='estexecuteemodegestion',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='estexecuteemodegestion',
            name='nature_depense',
        ),
        migrations.RemoveField(
            model_name='estexecuteeoperationfdcdr',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='estexecuteeoperationfdcdr',
            name='groupe_depense',
        ),
        migrations.RemoveField(
            model_name='estexecuteeoperationfdcdr',
            name='operation',
        ),
        migrations.RemoveField(
            model_name='estexecuteesur',
            name='etape_execution',
        ),
        migrations.RemoveField(
            model_name='estexecuteesur',
            name='tache',
        ),
        migrations.RemoveField(
            model_name='estprogramme',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='estprogramme',
            name='tache',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteeaction',
            name='action',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteeaction',
            name='etape_execution_glob',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteeaction',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteeaction',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteefcpdr',
            name='etape_execution_glob',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteefcpdr',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteefcpdr',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteefcpdr',
            name='tache',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteefcptdd',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteefcptdd',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteefcptdd',
            name='tache',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteegcautres',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteegcautres',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteegcautres',
            name='tache',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteegcsub',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteegcsub',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteegcsub',
            name='tache',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteemodegestion',
            name='etape_execution_glob',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteemodegestion',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteemodegestion',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteemodegestion',
            name='nature_depense',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteeoperationfdcdr',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteeoperationfdcdr',
            name='groupe_depense',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteeoperationfdcdr',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteeoperationfdcdr',
            name='operation',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteesur',
            name='etape_execution',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteesur',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalestexecuteesur',
            name='tache',
        ),
        migrations.RemoveField(
            model_name='historicalestprogramme',
            name='exercice',
        ),
        migrations.RemoveField(
            model_name='historicalestprogramme',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalestprogramme',
            name='tache',
        ),
        migrations.DeleteModel(
            name='EstExecuteeAction',
        ),
        migrations.DeleteModel(
            name='EstExecuteeFCPDR',
        ),
        migrations.DeleteModel(
            name='EstExecuteeFCPTDD',
        ),
        migrations.DeleteModel(
            name='EstExecuteeGCAUTRES',
        ),
        migrations.DeleteModel(
            name='EstExecuteeGCSUB',
        ),
        migrations.DeleteModel(
            name='EstExecuteeModeGestion',
        ),
        migrations.DeleteModel(
            name='EstExecuteeOperationFDCDR',
        ),
        migrations.DeleteModel(
            name='EstExecuteeSur',
        ),
        migrations.DeleteModel(
            name='EstProgramme',
        ),
        migrations.DeleteModel(
            name='HistoricalEstExecuteeAction',
        ),
        migrations.DeleteModel(
            name='HistoricalEstExecuteeFCPDR',
        ),
        migrations.DeleteModel(
            name='HistoricalEstExecuteeFCPTDD',
        ),
        migrations.DeleteModel(
            name='HistoricalEstExecuteeGCAUTRES',
        ),
        migrations.DeleteModel(
            name='HistoricalEstExecuteeGCSUB',
        ),
        migrations.DeleteModel(
            name='HistoricalEstExecuteeModeGestion',
        ),
        migrations.DeleteModel(
            name='HistoricalEstExecuteeOperationFDCDR',
        ),
        migrations.DeleteModel(
            name='HistoricalEstExecuteeSur',
        ),
        migrations.DeleteModel(
            name='HistoricalEstProgramme',
        ),
    ]
