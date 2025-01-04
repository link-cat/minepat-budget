from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path

from setting.imports import importer_etapes
from .models import Etape, EtapeContractualisation, PieceJointe


class PieceJointeInline(admin.TabularInline):
    model = PieceJointe
    fields = ("label", "document", "date_upload", "date_obtention")
    readonly_fields = ("date_upload",)  # La date d'upload est générée automatiquement
    extra = 1  # Nombre de pièces jointes supplémentaires affichées dans le formulaire


@admin.register(Etape)
class EtapeAdmin(admin.ModelAdmin):
    list_display = ("title","type",)
    search_fields = ("title","type",)
    list_filter = ("type",)
    inlines = [PieceJointeInline]  # Ajout des pièces jointes directement dans l'admin

    def get_urls(self):
        """
        Ajoutez une URL personnalisée pour le bouton d'action.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "create-steps/",
                self.admin_site.admin_view(self.create_steps),
                name="create_steps",
            ),
        ]
        return custom_urls + urls

    def create_steps(self, request):
        """
        Vue pour exécuter l'action de création d'étapes.
        """
        file_path = "ressources/etapes.xlsx"
        try:
            importer_etapes(f"media/{file_path}")
            self.message_user(
                request,
                "Les étapes de contractualisation ont été créées avec succès.",
                level=messages.SUCCESS,
            )
        except Exception as e:
            self.message_user(
                request,
                f"Erreur lors de la création des étapes : {e}",
                level=messages.ERROR,
            )
        return redirect("..")


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


# @admin.register(PPM)
# class PPMAdmin(admin.ModelAdmin):
#     list_display = (
#         "tache",
#         "nature_prestations",
#         "montant_previsionnel",
#         "date_publication_ao",
#         "saisine_ac",
#     )
#     search_fields = ("tache__title_fr", "nature_prestations", "source_financement")
#     list_filter = ("tache", "date_publication_ao", "saisine_ac")


# @admin.register(JPM)
# class JPMAdmin(admin.ModelAdmin):
#     list_display = (
#         "tache",
#         "nature_prestations",
#         "montant_previsionnel",
#         "date_lancement_consultation",
#         "date_signature_marche",
#     )
#     search_fields = ("tache__title_fr", "nature_prestations", "source_financement")
#     list_filter = ("tache", "date_lancement_consultation", "date_signature_marche")
