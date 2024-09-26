from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    TypeRessource,
    NatureDepense,
    ModeGestion,
    Exercice,
    GroupeDepense,
    EtapeContractualisation,
    EtapeExecution,
    EtapeExecutionGlob,
    Chapitre,
    Programme,
    Action,
    Activite,
    Tache,
    Groupe,
    SUBGroupe,
    GroupeDepense,
    Operation,
    Region,
    Departement,
    Arrondissement,
)


class TypeRessourceAdmin(SimpleHistoryAdmin):
    list_display = ("title",)


class NatureDepenseAdmin(SimpleHistoryAdmin):
    list_display = (
        "code",
        "title",
        "groupe",
    )
    list_filter = ("groupe",)


class ModeGestionAdmin(SimpleHistoryAdmin):
    list_display = ("title", "source", "type_ressource")


class ExerciceAdmin(SimpleHistoryAdmin):
    list_display = ("annee",)


class GroupeDepenseAdmin(SimpleHistoryAdmin):
    list_display = ("annee",)


class EtapeContractualisationAdmin(SimpleHistoryAdmin):
    list_display = ("title",)


class EtapeExecutionAdmin(SimpleHistoryAdmin):
    list_display = ("title",)


class EtapeExecutionGlobAdmin(SimpleHistoryAdmin):
    list_display = ("title",)


class ChapitreAdmin(SimpleHistoryAdmin):
    list_display = ("code", "title_fr", "title_en")
    search_fields = ("title_fr", "title_en")


class ProgrammeAdmin(SimpleHistoryAdmin):
    list_display = ("code", "title_fr", "title_en", "chapitre")
    search_fields = ("title_fr", "title_en")


class ActionAdmin(SimpleHistoryAdmin):
    list_display = ("code", "title_fr", "title_en", "programme")
    search_fields = ("title_fr", "title_en")


class ActiviteAdmin(SimpleHistoryAdmin):
    list_display = ("code", "title_fr", "title_en", "action")
    search_fields = ("title_fr", "title_en")


class TacheAdmin(SimpleHistoryAdmin):
    list_display = ("code", "title_fr", "title_en", "activite", "cout_tot")
    search_fields = ("title_fr", "title_en")
class GroupeAdmin(SimpleHistoryAdmin):
    list_display = ("code", "title_fr", "title_en")
    search_fields = ("title_fr", "title_en")
class SUBGroupeAdmin(SimpleHistoryAdmin):
    list_display = ("groupe", "title_fr", "title_en")
    search_fields = ("title_fr", "title_en")


class OperationAdmin(SimpleHistoryAdmin):
    list_display = ("title_fr", "title_en")


class GroupeDepenseAdmin(SimpleHistoryAdmin):
    list_display = ("title",)


class RegionAdmin(SimpleHistoryAdmin):
    list_display = ("name_fr", "name_en")
    search_fields = ("name_fr", "name_en")


class DepartementAdmin(SimpleHistoryAdmin):
    list_display = ("name", "region")
    search_fields = ("name",)
    list_filter = ("region",)


class ArrondissementAdmin(SimpleHistoryAdmin):
    list_display = ("name", "departement")
    search_fields = ("name",)
    list_filter = ("departement",)


admin.site.register(TypeRessource, TypeRessourceAdmin)
admin.site.register(NatureDepense, NatureDepenseAdmin)
admin.site.register(ModeGestion, ModeGestionAdmin)
admin.site.register(Exercice, ExerciceAdmin)
admin.site.register(EtapeContractualisation, EtapeContractualisationAdmin)
admin.site.register(EtapeExecution, EtapeExecutionAdmin)
admin.site.register(EtapeExecutionGlob, EtapeExecutionGlobAdmin)
admin.site.register(Chapitre, ChapitreAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Activite, ActiviteAdmin)
admin.site.register(Tache, TacheAdmin)
admin.site.register(Groupe, GroupeAdmin)
admin.site.register(SUBGroupe, SUBGroupeAdmin)
admin.site.register(GroupeDepense, GroupeDepenseAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Departement, DepartementAdmin)
admin.site.register(Arrondissement, ArrondissementAdmin)
