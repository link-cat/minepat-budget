import random
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


class Groupe(models.Model):
    code = models.CharField(max_length=255)
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    objectif = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return self.title_fr


class SUBGroupe(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    objectif = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return self.title_fr


class Tache(models.Model):

    class TypeChoices(models.TextChoices):
        APPEL_DOFFRES_OUVERT = "APPEL D'OFFRES OUVERT", "Appel d'offres ouvert"
        APPEL_DOFFRES_RESTREINT = "APPEL D'OFFRES RESTREINT", "Appel d'offres restreint"
        CONSULTATION_INDIVIDUELLE = (
            "CONSULTATION INDIVIDUELLE",
            "Consultation individuelle",
        )
        REGIE = "REGIE", "Régie"
        GRE_A_GRE = "GRE A GRE", "Gré à gré"

    code = models.CharField(max_length=255)
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    objectif = models.TextField(null=True, blank=True)
    cout_tot = models.FloatField()
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    numero_marche = models.CharField(max_length=255, null=True, blank=True)
    montant_previsionnel = models.FloatField(null=True, blank=True)
    adjudicataire = models.CharField(max_length=255, null=True, blank=True)
    numero_notification = models.CharField(max_length=255, null=True, blank=True)
    numero_ods = models.CharField(max_length=255, null=True, blank=True)
    numero_pv = models.CharField(max_length=255, null=True, blank=True)
    montant_reel = models.FloatField(null=True, blank=True)
    montant_operation_restant = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    groupe = models.ForeignKey(Groupe,on_delete=models.SET_NULL,null=True, blank=True)
    type = models.CharField(
        max_length=50,
        default=TypeChoices.APPEL_DOFFRES_OUVERT,
        choices=TypeChoices.choices,
        verbose_name="Type d'étape",
    )
    current_step = models.ForeignKey(
        "contractualisation.EtapeContractualisation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_step"
    )
    exercices = models.ManyToManyField(Exercice, related_name="taches")
    history = HistoricalRecords()

    def __str__(self):
        return self.title_fr

    def save(self, *args, **kwargs):
        if not self.latitude and not self.longitude:
            # Latitude et longitude générées aléatoirement dans les bornes du Cameroun
            self.latitude = round(random.uniform(2.0, 13.0), 6)
            self.longitude = round(random.uniform(8.5, 16.0), 6)
        super(Tache, self).save(*args, **kwargs)

class EtapeExecution(models.Model):
    title = models.CharField(max_length=255)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    history = HistoricalRecords()


class EtapeExecutionGlob(models.Model):
    title = models.CharField(max_length=255)
    history = HistoricalRecords()
