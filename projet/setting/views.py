from rest_framework import viewsets
from setting.models import (
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
)
from setting.serializers import (
    TypeRessourceSerializer,
    NatureDepenseSerializer,
    ModeGestionSerializer,
    ExerciceSerializer,
    EtapeExecutionGlobSerializer,
    ChapitreSerializer,
    ProgrammeSerializer,
    ActionSerializer,
    ActiviteSerializer,
    TacheSerializer,
    GroupeDepenseSerializer,
    OperationSerializer,
    RegionSerializer,
    DepartementSerializer,
    ArrondissementSerializer,
    EtapeContractualisationSerializer,
    EtapeExecutionSerializer,
    UploadSerializer,
)


class TypeRessourceViewSet(viewsets.ModelViewSet):
    queryset = TypeRessource.objects.all()
    serializer_class = TypeRessourceSerializer


class NatureDepenseViewSet(viewsets.ModelViewSet):
    queryset = NatureDepense.objects.all()
    serializer_class = NatureDepenseSerializer


class ModeGestionViewSet(viewsets.ModelViewSet):
    queryset = ModeGestion.objects.all()
    serializer_class = ModeGestionSerializer


class ExerciceViewSet(viewsets.ModelViewSet):
    queryset = Exercice.objects.all()
    serializer_class = ExerciceSerializer


class EtapeExecutionGlobViewSet(viewsets.ModelViewSet):
    queryset = EtapeExecutionGlob.objects.all()
    serializer_class = EtapeExecutionGlobSerializer


class ChapitreViewSet(viewsets.ModelViewSet):
    queryset = Chapitre.objects.all()
    serializer_class = ChapitreSerializer


class ProgrammeViewSet(viewsets.ModelViewSet):
    queryset = Programme.objects.all()
    serializer_class = ProgrammeSerializer


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class ActiviteViewSet(viewsets.ModelViewSet):
    queryset = Activite.objects.all()
    serializer_class = ActiviteSerializer


class TacheViewSet(viewsets.ModelViewSet):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer


class GroupeDepenseViewSet(viewsets.ModelViewSet):
    queryset = GroupeDepense.objects.all()
    serializer_class = GroupeDepenseSerializer


class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = RegionSerializer


class DepartementViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = DepartementSerializer


class ArrondissementViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = ArrondissementSerializer


class EtapeContractualisationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = EtapeContractualisationSerializer


class EtapeExecutionViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = EtapeExecutionSerializer


# import excel file
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from setting.imports import import_bip_excel_file


class ExcelImportViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]
    serializer_class = UploadSerializer

    @swagger_auto_schema(
        operation_summary="Importer un fichier Excel pour le BIP",
        operation_description="Cette vue permet de téléverser un fichier Excel pour l'importation des données BIP. Le fichier doit être au format Excel.",
        manual_parameters=[
            openapi.Parameter(
                "file_uploaded",
                openapi.IN_FORM,
                description="Le fichier Excel à importer",
                type=openapi.TYPE_FILE,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Le fichier a été importé avec succès",
                examples={
                    "application/json": {"message": "Fichier Excel importé avec succès"}
                },
            ),
            400: openapi.Response(
                description="Aucun fichier fourni",
                examples={"application/json": {"error": "Aucun fichier fourni"}},
            ),
        },
    )
    @action(detail=False, methods=["post"], url_path="BIP")
    def import_excel(self, request):
        if "file_uploaded" not in request.FILES:
            return Response(
                {"error": "Aucun fichier fourni"}, status=status.HTTP_400_BAD_REQUEST
            )
        excel_file = request.FILES["file_uploaded"]
        file_path = default_storage.save(f"temp/{excel_file.name}", excel_file)

        try:
            # Importer le fichier Excel
            import_bip_excel_file(file_path)
            return Response(
                {"message": "Fichier Excel importé avec succès"},
                status=status.HTTP_200_OK,
            )
        finally:
            # Supprimer le fichier après traitement
            default_storage.delete(file_path)


# for auth
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import generics

from setting.serializers import ProfileSerializer


@swagger_auto_schema(
    method="get",
    operation_summary="Récupérer le profil de l'utilisateur",
    operation_description="Ce endpoint retourne le profil de l'utilisateur authentifié. Un access token valide doit être fourni.",
    responses={
        200: openapi.Response(
            description="Profil de l'utilisateur récupéré avec succès",
            examples={
                "application/json": {
                    "id": 1,
                    "username": "user123",
                    "email": "user@example.com",
                }
            },
        ),
        401: openapi.Response(
            description="Non autorisé. Le token d'accès est invalide ou manquant.",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided."
                }
            },
        ),
    },
    security=[{"Bearer": []}],
)
@api_view(["GET"])
def getProfile(request):

    permission_classes = [IsAuthenticated]

    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)
