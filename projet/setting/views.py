from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from projet.permissions import CustomDjangoModelPermissions

from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q


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
    Region,
    Departement,
    Arrondissement,
    Groupe,
    SUBGroupe,
    EtapeExecution,
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
    EtapeExecutionSerializer,
    UploadSerializer,
    GroupeSerializer,
    SUBGroupeSerializer,
)


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Un ModelViewSet de base qui surcharge la méthode destroy pour
    retourner l'ID de l'élément supprimé dans la réponse.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        resource_id = instance.id
        self.perform_destroy(instance)
        return Response(
            data={"message": "Deleted successfully", "deleted_id": resource_id},
        )

    def perform_destroy(self, instance):
        """
        Cette méthode exécute la suppression de l'instance.
        Elle est appelée dans `destroy()`.
        """
        instance.delete()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-id")


class TypeRessourceViewSet(BaseModelViewSet):
    queryset = TypeRessource.objects.all()
    serializer_class = TypeRessourceSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class NatureDepenseViewSet(BaseModelViewSet):
    queryset = NatureDepense.objects.all()
    serializer_class = NatureDepenseSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class ModeGestionViewSet(BaseModelViewSet):
    queryset = ModeGestion.objects.all()
    serializer_class = ModeGestionSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class ExerciceViewSet(BaseModelViewSet):
    queryset = Exercice.objects.all()
    serializer_class = ExerciceSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class EtapeExecutionGlobViewSet(BaseModelViewSet):
    queryset = EtapeExecutionGlob.objects.all()
    serializer_class = EtapeExecutionGlobSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class ChapitreViewSet(BaseModelViewSet):
    queryset = Chapitre.objects.all()
    serializer_class = ChapitreSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class ProgrammeViewSet(BaseModelViewSet):
    queryset = Programme.objects.all()
    serializer_class = ProgrammeSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class ActionViewSet(BaseModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class ActiviteViewSet(BaseModelViewSet):
    queryset = Activite.objects.all()
    serializer_class = ActiviteSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class TacheViewSet(BaseModelViewSet):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "q",
                openapi.IN_QUERY,
                description="Mot-clé pour rechercher dans les champs title_fr et title_en.",
                type=openapi.TYPE_STRING,
            )
        ],
        responses={200: TacheSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def search(self, request):
        """
        Recherche les tâches par title_fr ou title_en correspondant à un mot-clé.
        """
        keyword = request.query_params.get("q", "").strip()
        if not keyword:
            return Response(
                {"error": "Le paramètre 'q' est requis pour effectuer une recherche."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tasks = self.queryset.filter(
            Q(title_fr__icontains=keyword) | Q(title_en__icontains=keyword)
        )
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupeDepenseViewSet(BaseModelViewSet):
    queryset = GroupeDepense.objects.all()
    serializer_class = GroupeDepenseSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class OperationViewSet(BaseModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class RegionViewSet(BaseModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class DepartementViewSet(BaseModelViewSet):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class ArrondissementViewSet(BaseModelViewSet):
    queryset = Arrondissement.objects.all()
    serializer_class = ArrondissementSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class GroupeViewSet(BaseModelViewSet):
    queryset = Groupe.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class SUBGroupeViewSet(BaseModelViewSet):
    queryset = SUBGroupe.objects.all()
    serializer_class = SUBGroupeSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


class EtapeExecutionViewSet(BaseModelViewSet):
    queryset = EtapeExecution.objects.all()
    serializer_class = EtapeExecutionSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]


# import excel file
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage

from setting.imports import import_bip_excel_file


class ExcelImportViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]
    serializer_class = UploadSerializer
    permission_classes = [IsAuthenticated]

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
            import_bip_excel_file(f"media/{file_path}")
            return Response(
                {"message": "Fichier Excel importé avec succès"},
                status=status.HTTP_200_OK,
            )
        finally:
            # Supprimer le fichier après traitement
            print("import reussi")


# for auth
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes

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
@permission_classes([IsAuthenticated])
def getProfile(request):

    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)


from django.contrib.auth.models import Permission


@api_view(["GET"])
@swagger_auto_schema(
    operation_description="Liste des permissions disponibles avec ID et codename",
    responses={200: "Liste des permissions sous forme {id: codename}"},
)
@permission_classes([AllowAny])
def PermissionListView(request):
    permissions = Permission.objects.all().values("id", "codename")
    return Response({"permissions": list(permissions)}, status=status.HTTP_200_OK)
