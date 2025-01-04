from django.contrib import messages
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path

from .imports import import_bip_excel_file
from .forms import ExcelUploadForm
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    TypeRessource,
    NatureDepense,
    ModeGestion,
    Exercice,
    GroupeDepense,
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
    filter_horizontal = ("exercices",)

    change_list_template = "admin/tache_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-excel/",
                self.admin_site.admin_view(self.import_excel),
                name="import_excel",
            ),
        ]
        return custom_urls + urls

    def import_excel(self, request):
        from django.core.files.storage import default_storage

        if request.method == "POST":
            form = ExcelUploadForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = form.cleaned_data["file_uploaded"]
                file_path = default_storage.save(f"temp/{excel_file.name}", excel_file)
                try:
                    import_bip_excel_file(f"media/{file_path}")
                    self.message_user(
                        request,
                        "Fichier Excel importé avec succès",
                        level=messages.SUCCESS,
                    )
                except Exception as e:
                    self.message_user(
                        request, f"Erreur lors de l'import : {e}", level=messages.ERROR
                    )
                return HttpResponseRedirect("../")
        else:
            form = ExcelUploadForm()

        context = {
            "form": form,
            "opts": self.model._meta,
            "title": "Importer un fichier Excel",
        }
        return render(request, "admin/excel_import.html", context)


class GroupeAdmin(SimpleHistoryAdmin):
    list_display = ("code", "title_fr", "title_en")
    search_fields = ("title_fr", "title_en")
class SUBGroupeAdmin(SimpleHistoryAdmin):
    list_display = ("groupe", "title_fr", "title_en")
    search_fields = ("title_fr", "title_en")


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
admin.site.register(Region, RegionAdmin)
admin.site.register(Departement, DepartementAdmin)
admin.site.register(Arrondissement, ArrondissementAdmin)
