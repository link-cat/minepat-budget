from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from setting.imports import importer_etapes

from .filters import EtapeContractualisationFilter
from projet.permissions import CustomDjangoModelPermissions

from .models import (
    EtapeContractualisation,
    Etape,
    PPM,
    PieceJointe,
    PieceJointeContractualisation,
)
from .serializers import (
    EtapeContractualisationSerializer,
    EtapeSerializer,
    PPMSerializer,
    PieceJointeContractSerializer,
    PieceJointeSerializer,
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


class EtapeContractualisationViewSet(BaseModelViewSet):
    queryset = EtapeContractualisation.objects.all()
    serializer_class = EtapeContractualisationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EtapeContractualisationFilter

    def perform_save(self, serializer):
        etape_contractualisation = serializer.save()
        tache = etape_contractualisation.tache

        if tache:
            # Récupérer l'étape prioritaire
            prioritaire = (
                EtapeContractualisation.objects.filter(tache=tache, is_finished=False)
                .order_by("etape__rang")
                .first()
            )
            # Mettre à jour les attributs de la tâche
            tache.type = etape_contractualisation.etape.type
            tache.current_step = prioritaire if prioritaire else None

            print(
                EtapeContractualisation.objects.filter(
                    tache=tache, is_finished=False
                ).first()
            )

            # Sauvegarder la tâche
            tache.save()
        else:
            print("Aucune tâche associée à cette étape.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_save(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_save(serializer)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        today = now().date()
        is_finished = self.request.query_params.get("is_finished")
        late = self.request.query_params.get("late")
        for instance in queryset:
            if instance.date_prevue and not instance.is_finished:
                delay_days = (today - instance.date_prevue).days - (
                    instance.etape.delai or 0
                )
                if delay_days > 0:
                    instance.retard_message = (
                        f"Vous êtes en retard de {delay_days} jours."
                    )
                else:
                    instance.retard_message = None
                instance.save(update_fields=["retard_message"])
            elif instance.date_prevue and instance.is_finished:
                delay_days = (instance.date_fin - instance.date_prevue).days - (
                    instance.etape.delai or 0
                )
                if delay_days > 0:
                    instance.retard_message = (
                        f"Vous êtes en retard de {delay_days} jours."
                    )
                else:
                    instance.retard_message = None
                instance.save(update_fields=["retard_message"])
        if late:
            return self.queryset.filter(retard_message__isnull=False)
        if is_finished:
            return self.queryset.filter(is_finished=is_finished)
        return self.queryset.order_by("-id")


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


# class JPMViewSet(BaseModelViewSet):
#     queryset = JPM.objects.all()
#     serializer_class = JPMSerializer

#     def get_queryset(self):
#         # Surcharge de get_queryset pour trier par date de création
#         return JPM.objects.all().order_by("-id")


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

    def get_queryset(self):
        # Filtrer par l'étape si nécessaire
        etape_id = self.request.query_params.get("etape_id")
        if etape_id:
            return self.queryset.filter(etape_id=etape_id)
        return self.queryset


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
