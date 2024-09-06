from django.contrib import admin
from django.urls import path, include
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
    OperationViewSet,
    getProfile,
)

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

viewsets = [
    ("upload-bip", ExcelImportViewSet, "upload-bip"),
    ("tache", TacheViewSet, "tache"),
    ("type-ressource", TypeRessourceViewSet, "type-ressource"),
    ("nature-depense", NatureDepenseViewSet, "nature-depense"),
    ("mode-gestion", ModeGestionViewSet, "mode-gestion"),
    ("exercice", ExerciceViewSet, "exercice"),
    ("etape-execution", EtapeExecutionGlobViewSet, "etape-execution"),
    ("chapitre", ChapitreViewSet, "chapitre"),
    ("programme", ProgrammeViewSet, "programme"),
    ("action", ActionViewSet, "action"),
    ("activite", ActiviteViewSet, "activite"),
    ("groupe-depense", GroupeDepenseViewSet, "groupe-depense"),
    ("operation", OperationViewSet, "operation"),
]
router = routers.DefaultRouter()
for prefix, viewset, basename in viewsets:
    router.register(rf"{prefix}", viewset, basename=basename)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("setting/", include(router.urls)),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
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
