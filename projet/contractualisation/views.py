from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from projet.permissions import CustomDjangoModelPermissions

from .models import EtapeContractualisation,Etape
from .serializers import EtapeContractualisationSerializer,EtapeSerializer

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

    def get_queryset(self):
        # Surcharge de get_queryset pour trier par date de création
        return EtapeContractualisation.objects.all().order_by("-id")


class EtapeViewSet(BaseModelViewSet):
    queryset = Etape.objects.all()
    serializer_class = EtapeSerializer
    def get_queryset(self):
        # Surcharge de get_queryset pour trier par date de création
        return Etape.objects.all().order_by("-id")
