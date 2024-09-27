from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from setting.models import (
    Action,
    Exercice,
    EtapeExecutionGlob,
    Tache,
    Operation,
    NatureDepense,
    GroupeDepense,
    EtapeExecution,
    SUBGroupe,
)

CONTRAT_SITUATION_CHOICES = [
    ("BC:Non executé", "BC:Non executé"),
    ("BC:Exec. en cours", "BC:Exec. en cours"),
    ("BC:Executé", "BC:Executé"),
    (
        "Marché:Gré-a-Gré,Accord MINMAP attendu",
        "Marché:Gré-a-Gré,Accord MINMAP attendu",
    ),
    ("Marché:ASMI/AMI en cours", "Marché:ASMI/AMI en cours"),
    ("Marché:DAO non transmis", "Marché:DAO non transmis"),
    ("Marché:DAO en CCC", "Marché:DAO en CCC"),
    ("Marché:DAO transmis en CIPM", "Marché:DAO transmis en CIPM"),
    ("Marché:AO lancé", "Marché:AO lancé"),
    ("Marché:AO infructueux", "Marché:AO infructueux"),
    ("Marché:Gré-a-Gré,proc. en cours", "Marché:Gré-a-Gré,proc. en cours"),
    ("Marché:Analyse offres en cours", "Marché:Analyse offres en cours"),
    ("Marché:Prop. attrib. en CCC", "Marché:Prop. attrib. en CCC"),
    ("Marché:Attribué", "Marché:Attribué"),
    ("Marché:Gré-a-Gré,proj. Marché en CCC", "Marché:Gré-a-Gré,proj. Marché en CCC"),
    ("Marché:Signé", "Marché:Signé"),
    ("Marché:OS Dem. trav. notifié", "Marché:OS Dem. trav. notifié"),
    ("Marché:OS Susp. trav. notifié", "Marché:OS Susp. trav. notifié"),
    ("Marché:Avenant en cours", "Marché:Avenant en cours"),
    ("Marché:receptionné", "Marché:receptionné"),
    ("Marché pluriannuel signé avant 2024", "Marché pluriannuel signé avant 2024"),
    ("Marché:chantier abandonné", "Marché:chantier abandonné"),
    ("Marché:resilié", "Marché:resilié"),
    ("Marché spécial:non signé", "Marché spécial:non signé"),
    ("Marché spécial:signé", "Marché spécial:signé"),
    ("Marché spécial:receptionné", "Marché spécial:receptionné"),
    ("Régie:Accord MINMAP attendu", "Régie:Accord MINMAP attendu"),
    ("Régie:Exec. en cours", "Régie:Exec. en cours"),
    ("Régie:Exec. complete", "Régie:Exec. complete"),
    ("Convention:signature en cours", "Convention:signature en cours"),
    ("Convention:signée", "Convention:signée"),
    ("Convention:Commande receptionnée", "Convention:Commande receptionnée"),
    ("Arriérée:liasse incomplete", "Arriérée:liasse incomplete"),
    ("Arriérée:liasse complete", "Arriérée:liasse complete"),
    ("Autre Opération Fonct.:Non executé", "Autre Opération Fonct.:Non executé"),
    ("Autre Opération Fonct.:Executé", "Autre Opération Fonct.:Executé"),
    ("Dotation non repartie", "Dotation non repartie"),
]


class EstExecuteeAction(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    etape_execution_glob = models.ForeignKey(
        EtapeExecutionGlob, on_delete=models.CASCADE, null=True, blank=True
    )
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField(default=timezone.now)
    montant_ae_eng = models.FloatField()
    montant_cp_eng = models.FloatField()
    montant_liq = models.FloatField()
    pourcentage_ae_eng = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_cp_eng = models.DecimalField(max_digits=4, decimal_places=2)
    ordonancement = models.FloatField()
    pourcentage_liq = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_ord = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_RPHY_cp = models.DecimalField(max_digits=4, decimal_places=2)
    ressource_mobilise = models.CharField(max_length=50)
    history = HistoricalRecords()


class EstExecuteeFCPDR(models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    etape_execution_glob = models.ForeignKey(
        EtapeExecutionGlob, on_delete=models.SET_NULL, null=True
    )
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField(default=timezone.now)
    montant_ae_eng = models.FloatField()
    montant_cp_eng = models.FloatField()
    montant_liq = models.FloatField()
    pourcentage_ae_eng = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_cp_eng = models.DecimalField(max_digits=4, decimal_places=2)
    ordonancement = models.FloatField()
    pourcentage_liq = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_ord = models.DecimalField(max_digits=4, decimal_places=2)
    gc_category_ressource = models.CharField(max_length=45)
    contrat_situation_actuelle = models.CharField(
        max_length=100, choices=CONTRAT_SITUATION_CHOICES, default="BC:Non executé"
    )
    montant_contrat = models.FloatField()
    date_demarrage_travaux = models.DateTimeField()
    delai_execution_contrat = models.IntegerField()
    prise_en_charge_TTC = models.FloatField()
    paiement_net_HT = models.FloatField()
    pourcentage_execution_physique_au_demarrage = models.FloatField()
    pourcentage_execution_physique_a_date = models.FloatField()
    observations = models.TextField()
    history = HistoricalRecords()


class EstExecuteeFCPTDD(models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField(default=timezone.now)
    montant_ae_eng = models.FloatField()
    montant_cp_eng = models.FloatField()
    montant_liq = models.FloatField()
    pourcentage_ae_eng = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_cp_eng = models.DecimalField(max_digits=4, decimal_places=2)
    ordonancement = models.FloatField()
    pourcentage_liq = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_ord = models.DecimalField(max_digits=4, decimal_places=2)
    observations = models.TextField()
    history = HistoricalRecords()


class EstExecuteeGCAUTRES(models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField(default=timezone.now)
    montant_ae_eng = models.FloatField()
    montant_cp_eng = models.FloatField()
    montant_liq = models.FloatField()
    pourcentage_ae_eng = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_cp_eng = models.DecimalField(max_digits=4, decimal_places=2)
    ordonancement = models.FloatField()
    pourcentage_liq = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_ord = models.DecimalField(max_digits=4, decimal_places=2)
    gc_category_ressource = models.CharField(max_length=45)
    contrat_situation_actuelle = models.CharField(
        max_length=100, choices=CONTRAT_SITUATION_CHOICES, default="BC:Non executé"
    )
    montant_contrat = models.FloatField()
    date_demarrage_travaux = models.DateTimeField()
    delai_execution_contrat = models.IntegerField()
    prise_en_charge_TTC = models.FloatField()
    paiement_net_HT = models.FloatField()
    pourcentage_execution_physique_au_demarrage = models.FloatField()
    pourcentage_execution_physique_a_date = models.FloatField()
    observations = models.TextField()
    history = HistoricalRecords()


class EstExecuteeGCSUB(models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField(default=timezone.now)
    montant_ae_eng = models.FloatField()
    montant_cp_eng = models.FloatField()
    montant_liq = models.FloatField()
    pourcentage_ae_eng = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_cp_eng = models.DecimalField(max_digits=4, decimal_places=2)
    ordonancement = models.FloatField()
    pourcentage_liq = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_ord = models.DecimalField(max_digits=4, decimal_places=2)
    gc_category_ressource = models.CharField(max_length=45)
    contrat_situation_actuelle = models.CharField(
        max_length=100, choices=CONTRAT_SITUATION_CHOICES, default="BC:Non executé"
    )
    montant_contrat = models.FloatField()
    date_demarrage_travaux = models.DateTimeField()
    delai_execution_contrat = models.IntegerField()
    prise_en_charge_TTC = models.FloatField()
    paiement_net_HT = models.FloatField()
    pourcentage_execution_physique_au_demarrage = models.FloatField()
    pourcentage_execution_physique_a_date = models.FloatField()
    observations = models.TextField()
    history = HistoricalRecords()


class EstExecuteeModeGestion(models.Model):
    nature_depense = models.ForeignKey(NatureDepense, on_delete=models.CASCADE)
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    etape_execution_glob = models.ForeignKey(
        EtapeExecutionGlob, on_delete=models.SET_NULL, null=True
    )
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField(default=timezone.now)
    montant_ae_eng = models.FloatField()
    montant_cp_eng = models.FloatField()
    montant_liq = models.FloatField()
    pourcentage_ae_eng = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_cp_eng = models.DecimalField(max_digits=4, decimal_places=2)
    ordonancement = models.FloatField()
    pourcentage_liq = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_ord = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_RPHY_cp = models.DecimalField(max_digits=4, decimal_places=2)
    history = HistoricalRecords()


class EstExecuteeOperationFDCDR(models.Model):
    groupe = models.ForeignKey(SUBGroupe, on_delete=models.CASCADE)
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    montant_ae = models.FloatField()
    montant_cp = models.FloatField()
    dateimport = models.DateField(default=timezone.now)
    contrat_situation_actuelle = models.CharField(
        max_length=100, choices=CONTRAT_SITUATION_CHOICES, default="BC:Non executé"
    )
    montant_contrat = models.FloatField()
    date_demarrage_travaux = models.DateTimeField()
    delai_execution_contrat = models.IntegerField()
    observation = models.TextField()
    difficultes = models.TextField()
    montant_engage = models.FloatField()
    pourcentage_execution_physique_au_demarrage = models.FloatField()
    pourcentage_execution_physique_a_date = models.DecimalField(
        max_digits=4, decimal_places=2
    )
    history = HistoricalRecords()


class EstExecuteeSur(models.Model):
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    etape_execution = models.ForeignKey(
        EtapeExecution, on_delete=models.SET_NULL, null=True
    )
    date_debut = models.DateField()
    date_fin = models.DateField()
    chemin_extrant = models.CharField(max_length=150)
    ecart = models.IntegerField()
    difficultes_rencontrees = models.TextField()
    history = HistoricalRecords()


class EstProgramme(models.Model):
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    history = HistoricalRecords()
