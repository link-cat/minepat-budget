from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    TypeRessource,
    NatureDepense,
    ModeGestion,
    Exercice,
    EtapeExecutionGlob,
    Chapitre,
    Programme,
    Action,
    Activite,
    Tache,
    GroupeDepense,
    Operation,
    Region,
    Departement,
    Arrondissement,
    Commune,
)


class TypeRessourceAdmin(SimpleHistoryAdmin):
    list_display = ("title",)


class NatureDepenseAdmin(SimpleHistoryAdmin):
    list_display = ("title",)
    filter_horizontal = ("type_ressources",)


class ModeGestionAdmin(SimpleHistoryAdmin):
    list_display = ("title",)


class ExerciceAdmin(SimpleHistoryAdmin):
    list_display = ("annee", "dateimport")


class EtapeExecutionGlobAdmin(SimpleHistoryAdmin):
    list_display = ("title",)


class ChapitreAdmin(SimpleHistoryAdmin):
    list_display = ("code", "title")


class ProgrammeAdmin(SimpleHistoryAdmin):
    list_display = ("code", "title", "chapitre")


class ActionAdmin(SimpleHistoryAdmin):
    list_display = ("code", "title", "programme")


class ActiviteAdmin(SimpleHistoryAdmin):
    list_display = ("code", "title", "action")


class TacheAdmin(SimpleHistoryAdmin):
    list_display = ("code", "title", "activite", "cout_tot")


class GroupeDepenseAdmin(SimpleHistoryAdmin):
    list_display = ("title",)


class OperationAdmin(SimpleHistoryAdmin):
    list_display = ("title",)


class RegionAdmin(SimpleHistoryAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class DepartementAdmin(SimpleHistoryAdmin):
    list_display = ("name", "region")
    search_fields = ("name",)
    list_filter = ("region",)


class ArrondissementAdmin(SimpleHistoryAdmin):
    list_display = ("name", "departement")
    search_fields = ("name",)
    list_filter = ("departement",)


class CommuneAdmin(SimpleHistoryAdmin):
    list_display = ("name", "arrondissement")
    search_fields = ("name",)
    list_filter = ("arrondissement",)


admin.site.register(TypeRessource, TypeRessourceAdmin)
admin.site.register(NatureDepense, NatureDepenseAdmin)
admin.site.register(ModeGestion, ModeGestionAdmin)
admin.site.register(Exercice, ExerciceAdmin)
admin.site.register(EtapeExecutionGlob, EtapeExecutionGlobAdmin)
admin.site.register(Chapitre, ChapitreAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Activite, ActiviteAdmin)
admin.site.register(Tache, TacheAdmin)
admin.site.register(GroupeDepense, GroupeDepenseAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Departement, DepartementAdmin)
admin.site.register(Arrondissement, ArrondissementAdmin)
admin.site.register(Commune, CommuneAdmin)
