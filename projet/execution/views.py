from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


from .models import (
    EstExecuteeAction,
    EstExecuteeFCPDR,
    EstExecuteeFCPTDD,
    EstExecuteeGCAUTRES,
    EstExecuteeGCSUB,
    EstExecuteeModeGestion,
    EstExecuteeOperationFDCDR,
    EstExecuteeSur,
    EstProgramme,
)
from .serializers import (
    EstExecuteeActionSerializer,
    EstExecuteeFCPDRSerializer,
    EstExecuteeFCPTDDSerializer,
    EstExecuteeGCAUTRESSerializer,
    EstExecuteeGCSUBSerializer,
    EstExecuteeModeGestionSerializer,
    EstExecuteeOperationFDCDRSerializer,
    EstExecuteeSurSerializer,
    EstProgrammeSerializer,
)
from .filters import EstExecuteeGCSUBFilter,EstExecuteeGCAutresFilter


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Un ModelViewSet de base qui surcharge la méthode destroy pour
    retourner l'ID de l'élément supprimé dans la réponse.
    """
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

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


class EstExecuteeActionViewSet(BaseModelViewSet):
    queryset = EstExecuteeAction.objects.all()
    serializer_class = EstExecuteeActionSerializer


class EstExecuteeFCPDRViewSet(BaseModelViewSet):
    queryset = EstExecuteeFCPDR.objects.all()
    serializer_class = EstExecuteeFCPDRSerializer


class EstExecuteeFCPTDDViewSet(BaseModelViewSet):
    queryset = EstExecuteeFCPTDD.objects.all()
    serializer_class = EstExecuteeFCPTDDSerializer


class EstExecuteeGCAUTRESViewSet(BaseModelViewSet):
    queryset = EstExecuteeGCAUTRES.objects.all()
    serializer_class = EstExecuteeGCAUTRESSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstExecuteeGCAutresFilter


class EstExecuteeGCSUBViewSet(BaseModelViewSet):
    queryset = EstExecuteeGCSUB.objects.all()
    serializer_class = EstExecuteeGCSUBSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstExecuteeGCSUBFilter


class EstExecuteeModeGestionViewSet(BaseModelViewSet):
    queryset = EstExecuteeModeGestion.objects.all()
    serializer_class = EstExecuteeModeGestionSerializer


class EstExecuteeOperationFDCDRViewSet(BaseModelViewSet):
    queryset = EstExecuteeOperationFDCDR.objects.all()
    serializer_class = EstExecuteeOperationFDCDRSerializer


class EstExecuteeSurViewSet(BaseModelViewSet):
    queryset = EstExecuteeSur.objects.all()
    serializer_class = EstExecuteeSurSerializer


class EstProgrammeViewSet(BaseModelViewSet):
    queryset = EstProgramme.objects.all()
    serializer_class = EstProgrammeSerializer

from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from setting.serializers import UploadSerializer

from setting.imports import import_excel_file

class ExcelImportViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]
    serializer_class = UploadSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Importer un fichier Excel pour la gestion du suivi de l'execution",
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
    @action(detail=False, methods=["post"], url_path="execution")
    def import_excel(self, request):
        if "file_uploaded" not in request.FILES:
            return Response(
                {"error": "Aucun fichier fourni"}, status=status.HTTP_400_BAD_REQUEST
            )
        excel_file = request.FILES["file_uploaded"]
        file_path = default_storage.save(f"temp/{excel_file.name}", excel_file)

        try:
            # Importer le fichier Excel
            import_excel_file(file_path)
            return Response(
                {"message": "Fichier Excel importé avec succès"},
                status=status.HTTP_200_OK,
            )
        finally:
            # Supprimer le fichier après traitement
            default_storage.delete(file_path)
