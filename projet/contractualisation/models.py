from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from simple_history.models import HistoricalRecords

from setting.models import Tache


class Etape(models.Model):
    class TypeChoices(models.TextChoices):
        APPEL_DOFFRES_OUVERT = "APPEL D'OFFRES OUVERT", "Appel d'offres ouvert"
        APPEL_DOFFRES_RESTREINT = "APPEL D'OFFRES RESTREINT", "Appel d'offres restreint"
        CONSULTATION_INDIVIDUELLE = (
            "CONSULTATION INDIVIDUELLE",
            "Consultation individuelle",
        )
        REGIE = "REGIE", "Régie"
        GRE_A_GRE = "GRE A GRE", "Gré à gré"

    title = models.CharField(max_length=255)
    dated = models.BooleanField(default=True)
    type = models.CharField(
        max_length=50,
        default=TypeChoices.APPEL_DOFFRES_OUVERT,
        choices=TypeChoices.choices,
        verbose_name="Type d'étape",
    )

    def __str__(self):
        return f"{self.title} - {self.get_type_display()}"

class PieceJointeContractualisation(models.Model):
    etape_contractualisation = models.ForeignKey(
        "EtapeContractualisation",
        on_delete=models.CASCADE,
        related_name="pieces_jointes",
    )
    label = models.CharField(max_length=255, verbose_name="Nom du document")
    document = models.FileField(
        upload_to="documents/contractualisation/",
        null=True,
        blank=True,
        verbose_name="Fichier",
    )
    date_upload = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Date d'upload"
    )
    date_obtention = models.DateField(
        verbose_name="Date d'obtention", null=True, blank=True
    )

    def __str__(self):
        return f"{self.label} - {self.etape_contractualisation.tache.title_fr}"


class PieceJointe(models.Model):
    etape = models.ForeignKey(
        Etape, on_delete=models.CASCADE, related_name="pieces_jointes"
    )
    label = models.CharField(max_length=255, verbose_name="Nom du document")
    document = models.FileField(
        upload_to="documents/", null=True, blank=True, verbose_name="Fichier"
    )
    date_upload = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Date d'upload"
    )
    date_obtention = models.DateField(
        verbose_name="Date d'obtention", null=True, blank=True
    )

    def __str__(self):
        return f"{self.label} - {self.etape.title}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        # Synchronise les pièces jointes avec les étapes de contractualisation associées
        etapes_contractualisation = self.etape.contractualisations.all()
        print(etapes_contractualisation)
        for etape_contractualisation in etapes_contractualisation:
            # Vérifie si une pièce jointe existe déjà
            existing_piece = PieceJointeContractualisation.objects.filter(
                 etape_contractualisation=etape_contractualisation,
                label=self.label,
            ).first()
            if existing_piece:
                existing_piece.save()
            else:
                # Créez une nouvelle pièce jointe
                new = PieceJointeContractualisation.objects.create(
                    etape_contractualisation=etape_contractualisation,
                    label=self.label,
                    document=self.document,
                    date_obtention=self.date_obtention,
               )


@receiver(post_delete, sender=PieceJointe)
def delete_related_pieces_jointes_contractualisation(sender, instance, **kwargs):
    # Trouver les `EtapeContractualisation` associées à l'étape
    etapes_contractualisation = instance.etape.contractualisations.all()

    for etape_contractualisation in etapes_contractualisation:
        # Supprimer les pièces jointes correspondantes dans les étapes contractualisation
        PieceJointeContractualisation.objects.filter(
            etape_contractualisation=etape_contractualisation,
            label=instance.label,  # Correspondance basée sur le label
        ).delete()


class EtapeContractualisation(models.Model):
    etape = models.ForeignKey(
        Etape, on_delete=models.CASCADE, related_name="contractualisations"
    )
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE, related_name="projet")
    date_prevue = models.DateField(verbose_name="Date prévue", null=True, blank=True)
    date_effective = models.DateField(
        verbose_name="Date effective", null=True, blank=True
    )
    montant_prevu = models.FloatField(
        verbose_name="Montant prévisionnel", null=True, blank=True
    )
    montant_reel = models.FloatField(verbose_name="Montant réel", null=True, blank=True)
    taux_consomation = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Taux de consommation",
    )
    observations = models.TextField(blank=True, null=True)
    ecart_jours = models.IntegerField(editable=False, null=True, blank=True)
    ecart_montant = models.FloatField(editable=False, null=True, blank=True)
    is_finished = models.BooleanField(default=False)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.tache.title_fr} - {self.etape.title}"

    def save(self, *args, **kwargs):
        # Calcul de l'écart en jours si la date effective est fournie
        if self.date_effective and self.date_prevue:
            self.ecart_jours = (self.date_effective - self.date_prevue).days
        if self.montant_reel and self.montant_prevu:
            self.ecart_montant = self.montant_reel - self.montant_prevu
            self.taux_consomation = 100 * (self.montant_reel / self.tache.montant_reel)

        # Appeler la méthode save parent
        super().save(*args, **kwargs)

        # Copier les pièces jointes de l'étape si elles n'existent pas encore
        if not self.pieces_jointes.exists():
            for piece in self.etape.pieces_jointes.all():
                PieceJointeContractualisation.objects.create(
                    etape_contractualisation=self,
                    label=piece.label,
                    document=piece.document,
                    date_obtention=piece.date_obtention,
                )


class PPM(models.Model):
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    nature_prestations = models.CharField(max_length=255)
    montant_previsionnel = models.FloatField()
    source_financement = models.CharField(max_length=255)
    autorite_contractante = models.CharField(max_length=255)
    mode_consultation_solicite = models.CharField(max_length=255)
    procedure = models.CharField(max_length=255)
    saisine_ac = models.DateField()
    saisine_cpm = models.DateField()
    examen_dao_cpm = models.DateField()
    saisine_cccm_dao = models.DateField()
    avis_cccm_dao = models.CharField(max_length=255)
    non_objection_bf_1 = models.CharField(max_length=255)
    date_publication_ao = models.DateField()
    depouillement_offres = models.DateField()
    analyse_offres_techniques = models.DateField()
    examen_rapport_offres_techniques = models.DateField()
    non_objection_bf_2 = models.CharField(max_length=255)
    ouverture_offres_financieres = models.DateField()
    analyse_offres_financieres_synthese = models.DateField()
    proposition_attribution_cpm = models.CharField(max_length=255)
    saisine_cccm_attribution = models.DateField()
    avis_cccm_attribution = models.CharField(max_length=255)
    non_objection_bf_3 = models.CharField(max_length=255)
    publication_resultats = models.DateField()
    notification_decision_attribution = models.DateField()
    preparation_projet_marche = models.DateField()
    saisine_cpm_marche = models.DateField()
    examen_projet_marche = models.DateField()
    saisine_cccm_marche = models.DateField()
    avis_cccm_projet_marche_gg = models.CharField(max_length=255)
    non_objection_bf_4 = models.CharField(max_length=255)
    date_signature_marche = models.DateField()
    notification_marche = models.DateField()
    demarrage_prestations = models.DateField()
    reception_provisoire = models.DateField()
    reception_definitive = models.DateField()

    def __str__(self):
        return self.tache.title_fr


class JPM(models.Model):

    class TypeChoices(models.TextChoices):
        APPEL_DOFFRES_OUVERT = "APPEL D'OFFRES OUVERT", "Appel d'offres ouvert"
        APPEL_DOFFRES_RESTREINT = "APPEL D'OFFRES RESTREINT", "Appel d'offres restreint"
        CONSULTATION_INDIVIDUELLE = (
            "CONSULTATION INDIVIDUELLE",
            "Consultation individuelle",
        )
        REGIE = "REGIE", "Régie"
        GRE_A_GRE = "GRE A GRE", "Gré à gré"

    tache = models.ForeignKey(
        Tache,
        on_delete=models.CASCADE,
    )
    nature_prestations = models.CharField(
        max_length=50, verbose_name="Nature des prestations"
    )
    type = models.CharField(
        max_length=50,
        default=TypeChoices.APPEL_DOFFRES_OUVERT,
        choices=TypeChoices.choices,
        verbose_name="Type d'étape",
    )
    montant_previsionnel = models.FloatField(verbose_name="Montant prévisionnel (FCFA)")
    source_financement = models.CharField(
        max_length=255, verbose_name="Source de financement"
    )
    autorite_contractante = models.CharField(
        max_length=255,
        verbose_name="Autorité Contractante / Administration bénéficiaire",
    )
    mode_consultation = models.CharField(
        max_length=255, verbose_name="Mode de consultation"
    )
    date_lancement_consultation = models.DateField(
        verbose_name="Date de lancement de la consultation"
    )
    date_attribution_marche = models.DateField(
        verbose_name="Date d'attribution du marché"
    )
    date_signature_marche = models.DateField(verbose_name="Date de signature du marché")
    date_demarrage_prestations = models.DateField(
        verbose_name="Date de démarrage des prestations"
    )
    date_reception_prestations = models.DateField(
        verbose_name="Date de réception des prestations"
    )
    current_step = models.ForeignKey(
        EtapeContractualisation, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.tache.title_fr
