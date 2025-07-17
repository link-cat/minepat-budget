from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from simple_history.models import HistoricalRecords

from setting.models import (
    Action,
    Exercice,
    EtapeExecutionGlob,
    Tache,
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
    ("Marché:résilié", "Marché:résilié"),
    ("Marché spécial:non signé", "Marché spécial:non signé"),
    ("Marché spécial:signé", "Marché spécial:signé"),
    ("Marché spécial:réceptionné", "Marché spécial:réceptionné"),
    ("Régie:Accord MINMAP attendu", "Régie:Accord MINMAP attendu"),
    ("Régie:Exec. en cours", "Régie:Exec. en cours"),
    ("Régie:Exec. complète", "Régie:Exec. complète"),
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
    ressource_mobilise = models.CharField(max_length=300)
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
    contrat_situation_actuelle = models.CharField(
        max_length=300, choices=CONTRAT_SITUATION_CHOICES, default="BC:Non executé"
    )
    montant_contrat = models.FloatField()
    date_demarrage_travaux = models.DateField()
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
    contrat_situation_actuelle = models.CharField(
        max_length=300, choices=CONTRAT_SITUATION_CHOICES, default="BC:Non executé"
    )
    montant_contrat = models.FloatField()
    date_demarrage_travaux = models.DateField()
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
    contrat_situation_actuelle = models.CharField(
        max_length=300, choices=CONTRAT_SITUATION_CHOICES, default="BC:Non executé"
    )
    montant_contrat = models.FloatField()
    date_demarrage_travaux = models.DateField()
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
        max_length=300, choices=CONTRAT_SITUATION_CHOICES, default="BC:Non executé"
    )
    montant_contrat = models.FloatField()
    date_demarrage_travaux = models.DateField()
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
    chemin_extrant = models.CharField(max_length=300)
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


from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver


class PieceJointeConsommation(models.Model):
    consommation = models.ForeignKey(
        "Consommation",
        on_delete=models.CASCADE,
        related_name="pieces_jointes",
    )
    document = models.FileField(
        upload_to="documents/consommation/",
        null=True,
        blank=True,
        verbose_name="Fichier",
    )
    date_upload = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Date d'upload"
    )

    def __str__(self):
        return f"{self.consommation.tache.title_fr}"


class Groupe(models.Model):
    class TypeChoices(models.TextChoices):
        FCPDR = "FCPDR", "Fond de contrepartie depense reelles"
        SUBV = "SUBV", "Transferts et subventions"
    type = models.CharField(
        max_length=50,
        choices=TypeChoices.choices,
        verbose_name="Type de groupes d'operation",
    )
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    history = HistoricalRecords()

    def __str__(self):
        return self.title_fr


class Operation(models.Model):
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE, related_name='operations')
    groupe = models.ForeignKey(Groupe, null=True, blank=True, on_delete=models.CASCADE)
    montant = models.FloatField(null=True, blank=True)
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    delai_exec = models.IntegerField(null=True, blank=True)
    montant_engage = models.FloatField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title_fr


class Consommation(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    montant_engage = models.FloatField(null=True, blank=True)
    situation_contract = models.CharField(
        max_length=300, choices=CONTRAT_SITUATION_CHOICES, default="BC:Non executé"
    )
    report_received = models.BooleanField(default=False)
    date_situation = models.DateField(null=True)
    montant_contrat = models.FloatField(null=True, blank=True)
    delai_exec = models.IntegerField(null=True, blank=True)
    observations = models.TextField(null=True, blank=True)
    pourcentage_exec_physique = models.FloatField(null=True, blank=True)
    numero_marche = models.CharField(max_length=255, null=True, blank=True)
    prestataire = models.CharField(max_length=255, null=True, blank=True)
    ingenieur_marche = models.CharField(max_length=255, null=True, blank=True)
    chef_service = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()


# @receiver(pre_save, sender=Operation)
# def validate_operation(sender, instance, **kwargs):
#     if instance.tache.montant_operation_restant is None:
#         instance.tache.montant_operation_restant = instance.tache.montant_reel
#         instance.tache.save()
#     montant_restant = instance.tache.montant_operation_restant - instance.montant
#     if montant_restant < 0:
#         raise ValidationError(
#             f"Impossible d'ajouter une opération. Montant restant insuffisant pour la tâche {instance.tache.title_fr}."
#         )
#     else:
#         instance.tache.montant_operation_restant = montant_restant
#         instance.tache.save()


# @receiver(pre_save, sender=Consommation)
# def validate_consommation(sender, instance, **kwargs):
#     montant_possible = 0
#     idOperation = instance.operation.id 
#     if instance.operation.montant_engage is None:
#         instance.operation.montant_engage = 0

#     # if instance.montant_engage > 0:
#     #     montant_possible = instance.operation.montant_engage - ins

#     montant_possible = instance.operation.montant_engage + instance.montant_engage

#     # print("idOperation :", Consommation)
#     # print("operation.montant_engage :", instance.operation.montant_engage)
#     # print("montant_possible :", montant_possible)
#     # print("Last instance.montant_engage :", instance.montant_engage)

#     if montant_possible > instance.operation.montant:
#         raise ValidationError(
#             "Impossible d'ajouter une consommation. Montant restant insuffisant pour l'opération."
#         )

#     # On applique le nouveau montant *seulement après validation*
#     instance.operation.montant_engage = montant_possible
#     instance.operation.save()


@receiver(post_delete, sender=Operation)
def restore_tache_montant(sender, instance, **kwargs):
    if instance.tache.montant_operation_restant is None:
        instance.tache.montant_operation_restant = instance.tache.montant_reel
    instance.tache.montant_operation_restant += instance.montant
    instance.tache.save()


@receiver(post_delete, sender=Consommation)
def restore_operation_montant(sender, instance, **kwargs):
    if instance.operation.montant_engage is None:
        instance.operation.montant_engage = 0
    instance.operation.montant_engage -= instance.montant_engage
    instance.operation.save()


@receiver(pre_save, sender=Tache)
def handle_type_execution_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # On ignore les créations

    try:
        previous = Tache.objects.get(pk=instance.pk)
    except Tache.DoesNotExist:
        return

    if previous.type_execution != instance.type_execution:
        if instance.type_execution and instance.type_execution not in [
            Tache.TypeExecutionChoices.FCPDR,
            Tache.TypeExecutionChoices.ETAPUB,
            Tache.TypeExecutionChoices.STRUCTRAT,
        ]:
            # On supprime les anciennes opérations liées à la tâche
            Operation.objects.filter(tache=instance).delete()

            # On crée une nouvelle opération
            Operation.objects.create(
                tache=instance,
                title_fr=instance.title_fr,
                title_en=instance.title_en,
                montant=instance.cout_tot,
                delai_exec=instance.delais_execution,
            )
