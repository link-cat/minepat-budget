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
    title = models.CharField(max_length=255)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class ModeGestion(models.Model):
    title = models.CharField(max_length=255)
    type_ressource = models.ForeignKey(TypeRessource, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class NatureDepense(models.Model):
    title = models.CharField(max_length=255)
    mode = models.ForeignKey(ModeGestion, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class Exercice(models.Model):
    annee = models.IntegerField()
    history = HistoricalRecords()


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


class Operation(models.Model):
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    history = HistoricalRecords()


class GroupeDepense(models.Model):
    title = models.CharField(max_length=255)
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


class EstExecuteeAction(models.Model):
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
    montant_ae_eng = models.FloatField()
    montant_cp_eng = models.FloatField()
    montant_liq = models.FloatField()
    pourcentage_ae_eng = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_cp_eng = models.DecimalField(max_digits=4, decimal_places=2)
    liquidation = models.FloatField()
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
    dateimport = models.DateField()
    montant_ae_eng = models.FloatField()
    montant_cp_eng = models.FloatField()
    montant_liq = models.FloatField()
    pourcentage_ae_eng = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_cp_eng = models.DecimalField(max_digits=4, decimal_places=2)
    liquidation = models.FloatField()
    ordonancement = models.FloatField()
    pourcentage_liq = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_ord = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_RPHY_cp = models.DecimalField(max_digits=4, decimal_places=2)
    gc_category_ressource = models.CharField(max_length=45)
    contrat_situation_actuelle = models.TextField()
    montant_contrat = models.FloatField()
    date_demarrage_travaux = models.DateTimeField()
    delai_execution_contrat = models.IntegerField()
    history = HistoricalRecords()


class EstExecuteeFCPTDD(models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField()
    montant_ae_eng = models.FloatField()
    montant_cp_eng = models.FloatField()
    montant_liq = models.FloatField()
    pourcentage_ae_eng = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_cp_eng = models.DecimalField(max_digits=4, decimal_places=2)
    liquidation = models.FloatField()
    ordonancement = models.FloatField()
    pourcentage_liq = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_ord = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_RPHY_cp = models.DecimalField(max_digits=4, decimal_places=2)
    gc_category_ressource = models.CharField(max_length=45)
    contrat_situation_actuelle = models.TextField()
    montant_contrat = models.FloatField()
    date_demarrage_travaux = models.DateTimeField()
    delai_execution_contrat = models.IntegerField()
    history = HistoricalRecords()


class EstExecuteeGCAUTRES(models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField()
    montant_ae_eng = models.FloatField()
    montant_cp_eng = models.FloatField()
    montant_liq = models.FloatField()
    pourcentage_ae_eng = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_cp_eng = models.DecimalField(max_digits=4, decimal_places=2)
    liquidation = models.FloatField()
    ordonancement = models.FloatField()
    pourcentage_liq = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_ord = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_RPHY_cp = models.DecimalField(max_digits=4, decimal_places=2)
    gc_category_ressource = models.CharField(max_length=45)
    contrat_situation_actuelle = models.TextField()
    montant_contrat = models.FloatField()
    date_demarrage_travaux = models.DateTimeField()
    delai_execution_contrat = models.IntegerField()
    history = HistoricalRecords()


class EstExecuteeGCSUB(models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField()
    montant_ae_eng = models.FloatField()
    montant_cp_eng = models.FloatField()
    montant_liq = models.FloatField()
    pourcentage_ae_eng = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_cp_eng = models.DecimalField(max_digits=4, decimal_places=2)
    liquidation = models.FloatField()
    ordonancement = models.FloatField()
    pourcentage_liq = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_ord = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_RPHY_cp = models.DecimalField(max_digits=4, decimal_places=2)
    gc_category_ressource = models.CharField(max_length=45)
    contrat_situation_actuelle = models.TextField()
    montant_contrat = models.FloatField()
    date_demarrage_travaux = models.DateTimeField()
    delai_execution_contrat = models.IntegerField()
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
    dateimport = models.DateField()
    montant_ae_eng = models.FloatField()
    montant_cp_eng = models.FloatField()
    montant_liq = models.FloatField()
    pourcentage_ae_eng = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_cp_eng = models.DecimalField(max_digits=4, decimal_places=2)
    liquidation = models.FloatField()
    ordonancement = models.FloatField()
    pourcentage_liq = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_ord = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_RPHY_cp = models.DecimalField(max_digits=4, decimal_places=2)
    history = HistoricalRecords()


class EstExecuteeOperationFDCDR(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    groupe_depense = models.ForeignKey(GroupeDepense, on_delete=models.CASCADE)
    montant_ae_init = models.FloatField()
    montant_cp_init = models.FloatField()
    montant_ae_rev = models.FloatField()
    montant_cp_rev = models.FloatField()
    dateimport = models.DateField()
    montant_ae_eng = models.FloatField()
    montant_cp_eng = models.FloatField()
    montant_liq = models.FloatField()
    pourcentage_ae_eng = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_cp_eng = models.DecimalField(max_digits=4, decimal_places=2)
    liquidation = models.FloatField()
    ordonancement = models.FloatField()
    pourcentage_liq = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_ord = models.DecimalField(max_digits=4, decimal_places=2)
    pourcentage_RPHY_cp = models.DecimalField(max_digits=4, decimal_places=2)
    gc_category_ressource = models.CharField(max_length=45)
    contrat_situation_actuelle = models.TextField()
    montant_contrat = models.FloatField()
    date_demarrage_travaux = models.DateTimeField()
    delai_execution_contrat = models.IntegerField()
    observation = models.TextField()
    difficultes = models.TextField()
    montant_engage = models.FloatField()
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
