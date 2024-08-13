from django.db import models
from simple_history.models import HistoricalRecords


class Region(models.Model):
    name = models.CharField(max_length=255)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Departement(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="departements"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Arrondissement(models.Model):
    name = models.CharField(max_length=255)
    departement = models.ForeignKey(
        Departement, on_delete=models.CASCADE, related_name="arrondissements"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Commune(models.Model):
    name = models.CharField(max_length=255)
    arrondissement = models.ForeignKey(
        Arrondissement, on_delete=models.CASCADE, related_name="communes"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class TypeRessource(models.Model):
    title = models.CharField(max_length=255)
    history = HistoricalRecords()


class NatureDepense(models.Model):
    title = models.CharField(max_length=255)
    type_ressources = models.ManyToManyField(
        TypeRessource, related_name="natures_depense"
    )
    history = HistoricalRecords()


class ModeGestion(models.Model):
    title = models.CharField(max_length=255)
    history = HistoricalRecords()


class Exercice(models.Model):
    annee = models.IntegerField()
    dateimport = models.DateField()
    history = HistoricalRecords()


class EtapeExecutionGlob(models.Model):
    title = models.CharField(max_length=255)
history = HistoricalRecords()

class Chapitre(models.Model):
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    history = HistoricalRecords()


class Programme(models.Model):
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    objectif = models.TextField()
    chapitre = models.ForeignKey(
        Chapitre, on_delete=models.CASCADE, related_name="programmes"
    )
    history = HistoricalRecords()


class Action(models.Model):
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    objectif = models.TextField()
    programme = models.ForeignKey(
        Programme, on_delete=models.CASCADE, related_name="actions"
    )
    history = HistoricalRecords()


class Activite(models.Model):
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    objectif = models.TextField()
    action = models.ForeignKey(
        Action, related_name="activites", on_delete=models.CASCADE
    )
    history = HistoricalRecords()


class Tache(models.Model):
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    objectif = models.TextField()
    cout_tot = models.FloatField()
    activite = models.ForeignKey(
        Activite, related_name="taches", on_delete=models.CASCADE
    )
    numero_marche = models.CharField(max_length=255, null=True, blank=True)
    montant_previsionnel = models.FloatField(null=True, blank=True)
    adjudicataire = models.CharField(max_length=255, null=True, blank=True)
    numero_notification = models.CharField(max_length=255, null=True, blank=True)
    numero_ods = models.CharField(max_length=255, null=True, blank=True)
    numero_pv = models.CharField(max_length=255, null=True, blank=True)
    montant_reel = models.FloatField(null=True, blank=True)
    history = HistoricalRecords()


class GroupeDepense(models.Model):
    title = models.CharField(max_length=255)
    history = HistoricalRecords()


class Operation(models.Model):
    title = models.CharField(max_length=255)
    history = HistoricalRecords()


class EstExecuteeModeGestion(models.Model):
    mode_gestion = models.ForeignKey(ModeGestion, on_delete=models.CASCADE)
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    etape_execution_glob = models.ForeignKey(
        EtapeExecutionGlob, on_delete=models.CASCADE
    )
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField()
    history = HistoricalRecords()


class EstExecuteeAction(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    etape_execution_glob = models.ForeignKey(
        EtapeExecutionGlob, on_delete=models.CASCADE
    )
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField()
    history = HistoricalRecords()


class EstExecuteePour(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    etape_execution_glob = models.ForeignKey(
        EtapeExecutionGlob, on_delete=models.CASCADE
    )
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField()
    history = HistoricalRecords()


class EstExecuteeOperation(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    etape_execution_glob = models.ForeignKey(
        EtapeExecutionGlob, on_delete=models.CASCADE
    )
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField()
    tache = models.ForeignKey(
        Tache, on_delete=models.CASCADE, related_name="est_executee_operations"
    )
    groupe_depense = models.ForeignKey(
        GroupeDepense, on_delete=models.CASCADE, null=True, blank=True
    )
    operation = models.ForeignKey(
        Operation, on_delete=models.CASCADE, null=True, blank=True
    )
    history = HistoricalRecords()