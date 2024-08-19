from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from execution.models import EstExecuteeAction

class EstExecuteeActionAdmin(SimpleHistoryAdmin):
    list_display = (
        "action",
        "montant_ae_init",
        "montant_cp_init",
        "montant_ae_rev",
        "montant_cp_rev",
        "montant_ae_eng",
        "montant_cp_eng",
        "liquidation",
        "ordonancement",
        "pourcentage_ae_eng",
        "pourcentage_cp_eng",
        "pourcentage_liq",
        "pourcentage_ord",
        "pourcentage_RPHY_cp",
        "dateimport",
    )
    search_fields = ("action",)


admin.site.register(EstExecuteeAction, EstExecuteeActionAdmin)
