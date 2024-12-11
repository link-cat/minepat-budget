from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from django.db.models import Count, Q

from contractualisation.models import (
    EtapeContractualisation,
    PieceJointeContractualisation,
)


class ContractualisationViewSet(ViewSet):
    """
    ViewSet pour gérer les fonctionnalités liées aux pièces jointes et aux étapes de contractualisation.
    """

    @action(detail=False, methods=["get"], url_path="documents-uploades")
    def documents_uploades(self, request):
        """
        Retourne le nombre de documents uploadés pour chaque pièce jointe.
        """
        pieces = (
            PieceJointeContractualisation.objects.values("label")
            .annotate(nombre_documents=Count("id", filter=~Q(document=None)))
            .order_by("-nombre_documents")
        )
        return Response(list(pieces))

    @action(
        detail=False,
        methods=["get"],
        url_path="ecart-entre-etapes/(?P<etape_1_id>[^/.]+)/(?P<etape_2_id>[^/.]+)",
    )
    def ecart_entre_etapes(self, request, etape_1_id, etape_2_id):
        """
        Calcule l'écart en jours entre deux étapes.
        """
        try:
            etape_1 = EtapeContractualisation.objects.get(pk=etape_1_id)
            etape_2 = EtapeContractualisation.objects.get(pk=etape_2_id)

            # Vérifier si les dates sont valides
            if not etape_1.date_fin or not etape_2.date_demarrage:
                raise ValidationError(
                    {
                        "error": "Les dates nécessaires ne sont pas définies pour l'une ou les deux étapes."
                    }
                )

            # Calcul de l'écart
            ecart = (etape_2.date_demarrage - etape_1.date_fin).days
            return Response(
                {
                    "etape_1": etape_1.etape.title,
                    "etape_2": etape_2.etape.title,
                    "ecart_jours": ecart,
                }
            )

        except EtapeContractualisation.DoesNotExist:
            raise NotFound({"error": "L'une des étapes spécifiées n'existe pas."})
