from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from setting.views import (
    ExcelImportViewSet,
    TacheViewSet,
    TypeRessourceViewSet,
    NatureDepenseViewSet,
    ModeGestionViewSet,
    ExerciceViewSet,
    EtapeExecutionGlobViewSet,
    ChapitreViewSet,
    ProgrammeViewSet,
    ActionViewSet,
    ActiviteViewSet,
    GroupeDepenseViewSet,
    EtapeExecutionViewSet,
    RegionViewSet,
    DepartementViewSet,
    ArrondissementViewSet,
    GroupeViewSet,
    SUBGroupeViewSet,
    getProfile,
    PermissionListView,
)

from execution.views import (
    Annexe2View,
    Annexe3View,
    ExcelImportViewSet as ImportExecution,
    EstExecuteeActionViewSet,
    EstExecuteeFCPDRViewSet,
    EstExecuteeFCPTDDViewSet,
    EstExecuteeGCAUTRESViewSet,
    EstExecuteeGCSUBViewSet,
    EstExecuteeModeGestionViewSet,
    EstExecuteeOperationFDCDRViewSet,
    EstExecuteeSurViewSet,
    EstProgrammeViewSet,
    OperationViewSet,
    ConsommationViewSet,
    GroupeViewSet as ExecutionGroupe,
    PieceJointeConsommationViewSet,
)

from contractualisation.views import (
    EtapeContractualisationViewSet,
    EtapeViewSet,
    PieceJointeViewSet,
    MaturationViewSet,
    PieceJointeContractViewSet,
    PieceJointeMaturationViewSet,
    ExcelImportViewSet as ImportEtape,
)

from statistiques.views import BIPMetricsView
from execution.views import Annexe1View

schema_view = get_schema_view(
    openapi.Info(
        title="Projet API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Routes pour le module 'setting'
setting_viewsets = [
    ("upload-bip", ExcelImportViewSet, "upload-bip"),
    ("tache", TacheViewSet, "tache"),
    ("type-ressource", TypeRessourceViewSet, "type-ressource"),
    ("nature-depense", NatureDepenseViewSet, "nature-depense"),
    ("mode-gestion", ModeGestionViewSet, "mode-gestion"),
    ("exercice", ExerciceViewSet, "exercice"),
    ("etape-execution-gobale", EtapeExecutionGlobViewSet, "etape-execution-globale"),
    ("chapitre", ChapitreViewSet, "chapitre"),
    ("programme", ProgrammeViewSet, "programme"),
    ("action", ActionViewSet, "action"),
    ("activite", ActiviteViewSet, "activite"),
    ("groupe-depense", GroupeDepenseViewSet, "groupe-depense"),
    ("region", RegionViewSet, "region"),
    ("departement", DepartementViewSet, "departement"),
    ("arrondissement", ArrondissementViewSet, "arrondissement"),
    ("groupe", GroupeViewSet, "groupe"),
    ("sub-groupe", SUBGroupeViewSet, "sub-groupe"),
    ("etape-execution", EtapeExecutionViewSet, "etape-execution"),
]
router_setting = routers.DefaultRouter()
for prefix, viewset, basename in setting_viewsets:
    router_setting.register(rf"{prefix}", viewset, basename=basename)

# Routes pour le module 'execution'
execution_viewsets = [
    ("upload-execution", ImportExecution, "upload-execution"),
    ("est-executee-action", EstExecuteeActionViewSet, "est-executee-action"),
    ("est-executee-fcpdr", EstExecuteeFCPDRViewSet, "est-executee-fcpdr"),
    ("est-executee-fcptdd", EstExecuteeFCPTDDViewSet, "est-executee-fcptdd"),
    ("est-executee-gcautres", EstExecuteeGCAUTRESViewSet, "est-executee-gcautres"),
    ("est-executee-gcsub", EstExecuteeGCSUBViewSet, "est-executee-gcsub"),
    (
        "est-executee-mode-gestion",
        EstExecuteeModeGestionViewSet,
        "est-executee-mode-gestion",
    ),
    (
        "est-executee-operation-fdcdr",
        EstExecuteeOperationFDCDRViewSet,
        "est-executee-operation-fdcdr",
    ),
    ("est-executee-sur", EstExecuteeSurViewSet, "est-executee-sur"),
    ("est-programme", EstProgrammeViewSet, "est-programme"),
    (
        "pieces-jointe-consommation",
        PieceJointeConsommationViewSet,
        "pieces-jointe-consommation",
    ),
    ("operation", OperationViewSet, "operation"),
    ("consommation", ConsommationViewSet, "consommation"),
    ("groupe", ExecutionGroupe, "groupe"),
]
router_execution = routers.DefaultRouter()
for prefix, viewset, basename in execution_viewsets:
    router_execution.register(rf"{prefix}", viewset, basename=basename)

# Routes pour le module 'contractualisation'
contractualisation_viewsets = [
    (
        "etape-contractualisation",
        EtapeContractualisationViewSet,
        "etape-contractualisation",
    ),
    ("etape", EtapeViewSet, "etape"),
    ("pieces-jointe", PieceJointeViewSet, "pieces-jointe"),
    ("pieces-jointe-contract", PieceJointeContractViewSet, "pieces-jointe-contract"),
    (
        "pieces-jointe-maturation",
        PieceJointeMaturationViewSet,
        "pieces-jointe-maturation",
    ),
    ("load-etape", ImportEtape, "load-etape"),
    ("maturation", MaturationViewSet, "maturation"),
]
router_contractualisation = routers.DefaultRouter()
for prefix, viewset, basename in contractualisation_viewsets:
    router_contractualisation.register(rf"{prefix}", viewset, basename=basename)

# URLs globales
urlpatterns = [
    path("admin/", admin.site.urls),
    path("setting/", include(router_setting.urls)),
    path("execution/", include(router_execution.urls)),
    path("contractualisation/", include(router_contractualisation.urls)),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/permissions/", PermissionListView, name="permissions-list"),
    path("api/metrics/", BIPMetricsView, name="metrics"),
    path("api/annexe1/", Annexe1View, name="annexe_1"),
    path("api/annexe2/", Annexe2View, name="annexe_2"),
    path("api/annexe3/", Annexe3View, name="annexe_3"),
    path("profile/", getProfile, name="profile"),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
