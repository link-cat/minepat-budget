from django.utils import timezone
from django.db import models
from simple_history.models import HistoricalRecords


class Region(models.Model):
    name_fr = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name_fr} / {self.name_en}"


class Departement(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Arrondissement(models.Model):
    name = models.CharField(max_length=255)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class TypeRessource(models.Model):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class GroupeDepense(models.Model):
    title = models.CharField(max_length=255)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class ModeGestion(models.Model):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    type_ressource = models.ForeignKey(TypeRessource, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class NatureDepense(models.Model):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    groupe = models.ForeignKey(GroupeDepense, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class Exercice(models.Model):
    annee = models.IntegerField()
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.annee}"


class Chapitre(models.Model):
    code = models.CharField(max_length=15)
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    history = HistoricalRecords()

    def __str__(self):
        return self.title_fr


class Programme(models.Model):
    code = models.CharField(max_length=255)
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    objectif = models.TextField()
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.title_fr


class Action(models.Model):
    code = models.CharField(max_length=255)
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    objectif = models.TextField()
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.title_fr


class Activite(models.Model):
    code = models.CharField(max_length=255)
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    objectif = models.TextField()
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.title_fr


class Tache(models.Model):
    code = models.CharField(max_length=255)
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    objectif = models.TextField()
    cout_tot = models.FloatField()
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    numero_marche = models.CharField(max_length=255, null=True, blank=True)
    montant_previsionnel = models.FloatField(null=True, blank=True)
    adjudicataire = models.CharField(max_length=255, null=True, blank=True)
    numero_notification = models.CharField(max_length=255, null=True, blank=True)
    numero_ods = models.CharField(max_length=255, null=True, blank=True)
    numero_pv = models.CharField(max_length=255, null=True, blank=True)
    montant_reel = models.FloatField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title_fr


class Operation(models.Model):
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    history = HistoricalRecords()


class EtapeContractualisation(models.Model):
    title = models.CharField(max_length=255)
    history = HistoricalRecords()


class EtapeExecution(models.Model):
    title = models.CharField(max_length=255)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    history = HistoricalRecords()


class EtapeExecutionGlob(models.Model):
    title = models.CharField(max_length=255)
    history = HistoricalRecords()
