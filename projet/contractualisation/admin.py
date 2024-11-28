from django.contrib import admin
from .models import Etape, EtapeContractualisation, PieceJointe, PPM, JPM


class PieceJointeInline(admin.TabularInline):
    model = PieceJointe
    fields = ("label", "document", "date_upload", "date_obtention")
    readonly_fields = ("date_upload",)  # La date d'upload est générée automatiquement
    extra = 1  # Nombre de pièces jointes supplémentaires affichées dans le formulaire


@admin.register(Etape)
class EtapeAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    inlines = [PieceJointeInline]  # Ajout des pièces jointes directement dans l'admin


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
    search_fields = ("etape__title", "observations")
    readonly_fields = (
        "ecart_jours",
        "ecart_montant",
    )  # Rendre ces champs non modifiables

    # Affichage des pièces jointes liées
    def related_pieces_jointes(self, obj):
        pieces = obj.etape.pieces_jointes.all()  # Accès aux pièces jointes liées
        if not pieces.exists():
            return "Aucune pièce jointe"
        return ", ".join(
            [
                f'<a href="{piece.document.url}" target="_blank">{piece.label}</a>'
                for piece in pieces
            ]
        )

    related_pieces_jointes.short_description = "Pièces jointes liées"
    related_pieces_jointes.allow_tags = True


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
