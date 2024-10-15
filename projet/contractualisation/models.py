from django.db import models
from simple_history.models import HistoricalRecords


class Etape(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class EtapeContractualisation(models.Model):
    etape = models.ForeignKey(
        Etape, on_delete=models.CASCADE, related_name="contractualisations"
    )
    date_prevue = models.DateField(verbose_name="Date prévue")
    date_effective = models.DateField(
        verbose_name="Date effective", null=True, blank=True
    )
    observations = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to="documents/", null=True, blank=True)
    ecart_jours = models.IntegerField(editable=False, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.etape.title} - {self.date_prevue}"

    def save(self, *args, **kwargs):
        # Calcul de l'écart en jours si la date effective est fournie
        if self.date_effective and self.date_prevue:
            self.ecart_jours = (self.date_effective - self.date_prevue).days
        super().save(*args, **kwargs)
