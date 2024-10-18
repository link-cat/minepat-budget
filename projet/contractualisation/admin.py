from traceback import format_tb
from django.contrib import admin
from .models import Etape, EtapeContractualisation, PPM, JPM


@admin.register(Etape)
class EtapeAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(EtapeContractualisation)
class EtapeContractualisationAdmin(admin.ModelAdmin):
    list_display = (
        "etape",
        "date_prevue",
        "date_effective",
        "ecart_jours",
        "observations",
    )
    list_filter = ("etape", "date_prevue", "date_effective")
    search_fields = ("etape__nom", "observations")
    readonly_fields = ("ecart_jours",)

    def document_link(self, obj):
        if obj.document:
            return format_tb(
                '<a href="{}" target="_blank">Télécharger</a>', obj.document.url
            )
        return "Pas de document"

    document_link.short_description = "Document"


@admin.register(PPM)
class PPMAdmin(admin.ModelAdmin):
    list_display = (
        "tache",
        "nature_prestations",
        "montant_previsionnel",
        "date_publication_ao",
        "saisine_ac",
    )
    search_fields = ("tache__title_fr", "nature_prestations", "source_financement")
    list_filter = ("tache", "date_publication_ao", "saisine_ac")


@admin.register(JPM)
class JPMAdmin(admin.ModelAdmin):
    list_display = (
        "tache",
        "nature_prestations",
        "montant_previsionnel",
        "date_lancement_consultation",
        "date_signature_marche",
    )
    search_fields = ("tache__title_fr", "nature_prestations", "source_financement")
    list_filter = ("tache", "date_lancement_consultation", "date_signature_marche")
