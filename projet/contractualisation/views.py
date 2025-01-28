from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from setting.imports import importer_etapes

from .filters import EtapeContractualisationFilter, MaturationFilter
from projet.permissions import CustomDjangoModelPermissions

from .models import (
    EtapeContractualisation,
    Etape,
    PPM,
    Maturation,
    PieceJointe,
    PieceJointeContractualisation,
    PieceJointeMaturation
)
from .serializers import (
    EtapeContractualisationSerializer,
    EtapeSerializer,
    PPMSerializer,
    MaturationSerializer,
    PieceJointeContractSerializer,
    PieceJointeSerializer,
    PieceJointeMaturationSerializer
)

from django.utils.timezone import now


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Un ModelViewSet de base qui surcharge la méthode destroy pour
    retourner l'ID de l'élément supprimé dans la réponse.
    """

    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]

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

from django.db.models import F, ExpressionWrapper, IntegerField
from django.db.models.functions import Now
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response


class EtapeContractualisationViewSet(BaseModelViewSet):
    queryset = EtapeContractualisation.objects.all()
    serializer_class = EtapeContractualisationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EtapeContractualisationFilter

    def get_queryset(self):
        queryset = EtapeContractualisation.objects.all()

        is_finished = self.request.query_params.get("is_finished")
        if is_finished:
            queryset = queryset.filter(is_finished=bool(int(is_finished)))

        return queryset.order_by("-id")

    @action(detail=False, methods=["get"])
    def late(self, request):
        today = now().date()
        queryset = self.get_queryset().filter(date_prevue__lt=today, is_finished=False)

        filter_params = request.GET.dict()
        for key, value in filter_params.items():
            if hasattr(EtapeContractualisation, key):
                queryset = queryset.filter(**{key: value})

        # Sérialisation des résultats
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EtapeViewSet(BaseModelViewSet):
    queryset = Etape.objects.all()
    serializer_class = EtapeSerializer

    def get_queryset(self):
        # Surcharge de get_queryset pour trier par date de création
        return Etape.objects.all().order_by("-id")


class PPMViewSet(BaseModelViewSet):
    queryset = PPM.objects.all()
    serializer_class = PPMSerializer

    def get_queryset(self):
        # Surcharge de get_queryset pour trier par date de création
        return PPM.objects.all().order_by("-id")
class MaturationViewSet(BaseModelViewSet):
    queryset = Maturation.objects.all()
    serializer_class = MaturationSerializer
    filterset_class = MaturationFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-id")


from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from setting.serializers import UploadSerializer


# class ContractExcelImportViewSet(viewsets.ViewSet):
#     parser_classes = [MultiPartParser]
#     serializer_class = UploadSerializer
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         operation_summary="Importer un fichier Excel pour les contractualisations",
#         operation_description="Cette vue permet de téléverser un fichier Excel pour l'importation des données PPM et JPM.",
#         manual_parameters=[
#             openapi.Parameter(
#                 "file_uploaded",
#                 openapi.IN_FORM,
#                 description="Le fichier Excel à importer",
#                 type=openapi.TYPE_FILE,
#                 required=True,
#             )
#         ],
#         responses={
#             200: openapi.Response(
#                 description="Le fichier a été importé avec succès",
#                 examples={
#                     "application/json": {"message": "Fichier Excel importé avec succès"}
#                 },
#             ),
#             400: openapi.Response(
#                 description="Aucun fichier fourni",
#                 examples={"application/json": {"error": "Aucun fichier fourni"}},
#             ),
#         },
#     )
#     @action(detail=False, methods=["post"], url_path="contractualisation")
#     def import_excel(self, request):
#         if "file_uploaded" not in request.FILES:
#             return Response(
#                 {"error": "Aucun fichier fourni"}, status=status.HTTP_400_BAD_REQUEST
#             )

#         # Récupérer le fichier téléchargé
#         excel_file = request.FILES["file_uploaded"]
#         file_path = default_storage.save(f"/temp/{excel_file.name}", excel_file)

#         try:
#             # Appeler la fonction pour importer le fichier Excel
#             import_excel_contract_file(file_path)
#             return Response(
#                 {"message": "Fichier Excel importé avec succès"},
#                 status=status.HTTP_200_OK,
#             )
#         finally:
#             # Supprimer le fichier après traitement
#             print("import reussi")


class PieceJointeViewSet(BaseModelViewSet):
    queryset = PieceJointe.objects.all()
    serializer_class = PieceJointeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Filtrer par l'étape si nécessaire
        etape_id = self.request.query_params.get("etape_id")
        if etape_id:
            return self.queryset.filter(etape_id=etape_id)
        return self.queryset


class PieceJointeContractViewSet(BaseModelViewSet):
    queryset = PieceJointeContractualisation.objects.all()
    serializer_class = PieceJointeContractSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

class PieceJointeMaturationViewSet(BaseModelViewSet):
    queryset = PieceJointeMaturation.objects.all()
    serializer_class = PieceJointeMaturationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


class ExcelImportViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]
    serializer_class = UploadSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Importer un fichier Excel pour charger les etapes",
        operation_description="Cette vue permet de charger automatiquement des etapes pour la contractualisation.",
        responses={
            200: openapi.Response(
                description="Les etapes ont été crée avec succès",
            ),
            400: openapi.Response(
                description="Aucun fichier fourni",
                examples={"application/json": {"error": "Aucun fichier fourni"}},
            ),
        },
    )
    @action(detail=False, methods=["get"], url_path="BIP")
    def import_excel(self, request):
        file_path = "ressources/etapes.xlsx"

        try:
            # Importer le fichier Excel
            importer_etapes(f"media/{file_path}")
            return Response(
                {"message": "Fichier Excel importé avec succès"},
                status=status.HTTP_200_OK,
            )
        finally:
            # Supprimer le fichier après traitement
            print("creation reussi")
