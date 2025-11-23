from django.db import models

class Rapport(models.Model):
    titre = models.CharField(max_length=200, default="CADRE DE CONCERTATION")
    mois = models.CharField(max_length=50)  # Ex: "JUILLET 2025"
    annee = models.IntegerField(default=2025)
    
    # Ces champs recevront le HTML de TinyMCE
    resume_analytique = models.TextField(null=True, blank=True, verbose_name="Résumé Analytique")
    introduction = models.TextField(null=True, blank=True, verbose_name="Introduction")
    etat_mise_en_oeuvre = models.TextField(null=True, blank=True, verbose_name="etat de mise en oeuvre")
    presentation_du_budget = models.TextField(null=True, blank=True, verbose_name="presentation du budget")
    situation = models.TextField(null=True, blank=True, verbose_name="situation")
    conclusion = models.TextField(null=True, blank=True, verbose_name="Conclusion")
    
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.mois}"