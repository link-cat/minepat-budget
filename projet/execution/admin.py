from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    EstExecuteeAction,
    EstExecuteeFCPDR,
    EstExecuteeFCPTDD,
    EstExecuteeGCAUTRES,
    EstExecuteeGCSUB,
    EstExecuteeModeGestion,
    EstExecuteeOperationFDCDR,
    EstExecuteeSur,
    EstProgramme,
    Operation,
    Groupe,
    Consommation,
)


class BaseEstExecuteeAdmin(SimpleHistoryAdmin):
    readonly_fields = (
        "montant_ae_init",
        "montant_cp_init",
        "montant_ae_rev",
        "montant_cp_rev",
    )
    list_display = ("exercice", "dateimport", "montant_ae_eng", "montant_cp_eng")
    list_filter = ("exercice", "dateimport")
    search_fields = ("exercice__nom", "montant_ae_eng", "montant_cp_eng")
    date_hierarchy = "dateimport"


@admin.register(EstExecuteeAction)
class EstExecuteeActionAdmin(BaseEstExecuteeAdmin):
    pass


@admin.register(EstExecuteeFCPDR)
class EstExecuteeFCPDRAdmin(BaseEstExecuteeAdmin):
    list_display = BaseEstExecuteeAdmin.list_display + ("tache",)


@admin.register(EstExecuteeFCPTDD)
class EstExecuteeFCPTDDAdmin(BaseEstExecuteeAdmin):
    list_display = BaseEstExecuteeAdmin.list_display + ("tache",)


@admin.register(EstExecuteeGCAUTRES)
class EstExecuteeGCAUTRESAdmin(BaseEstExecuteeAdmin):
    list_display = BaseEstExecuteeAdmin.list_display + ("tache",)


@admin.register(EstExecuteeGCSUB)
class EstExecuteeGCSUBAdmin(BaseEstExecuteeAdmin):
    list_display = BaseEstExecuteeAdmin.list_display + ("tache",)


@admin.register(EstExecuteeModeGestion)
class EstExecuteeModeGestionAdmin(BaseEstExecuteeAdmin):
    list_display = BaseEstExecuteeAdmin.list_display + ("nature_depense",)


@admin.register(EstExecuteeOperationFDCDR)
class EstExecuteeOperationFDCDRAdmin(SimpleHistoryAdmin):
    list_display = (
        "groupe",
        "exercice",
        "dateimport",
        "montant_ae",
        "montant_cp",
    )
    search_fields = (
        "exercice",
        "dateimport",
        "groupe__title_fr",
        "groupe_activite__title_fr",
        "groupe_activite__title_en",
    )
    list_filter = (
        "groupe",
        "groupe__activite",
    )


@admin.register(EstExecuteeSur)
class EstExecuteeSurAdmin(SimpleHistoryAdmin):
    list_display = ("tache", "date_debut", "date_fin", "ecart")
    search_fields = ("tache__nom",)
    list_filter = ("date_debut", "date_fin")


@admin.register(EstProgramme)
class EstProgrammeAdmin(SimpleHistoryAdmin):
    list_display = ("tache", "exercice", "montant_ae_init", "montant_cp_init")
    readonly_fields = (
        "montant_ae_init",
        "montant_cp_init",
        "montant_ae_rev",
        "montant_cp_rev",
    )
    search_fields = ("tache__nom", "exercice__nom")
    list_filter = ("exercice",)

@admin.register(Operation)
class OperationAdmin(SimpleHistoryAdmin):
    list_display = ("tache","montant", "groupe",)
    list_filter = ("tache", "groupe")

@admin.register(Groupe)
class GroupeAdmin(SimpleHistoryAdmin):
    list_display = ("type","title_fr", "title_en",)
    list_filter = ("type",)

@admin.register(Consommation)
class ConsommationAdmin(SimpleHistoryAdmin):
    list_display = (
        "operation",
        "montant_engage",
        "situation_contract",
        "numero_marche",
        "prestataire",
        "ingenieur_marche",
        "chef_service",
    )
    list_filter = ("operation",)
