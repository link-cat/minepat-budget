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


# import excel file
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage

from setting.utils import import_excel_file


class ExcelImportViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]
    serializer_class = UploadSerializer

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
            import_excel_file(file_path)
            return Response(
                {"message": "Fichier Excel importé avec succès"},
                status=status.HTTP_200_OK,
            )
        finally:
            # Supprimer le fichier après traitement
            default_storage.delete(file_path)
