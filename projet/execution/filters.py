import django_filters
from .models import (
    Consommation,
    EstExecuteeGCSUB,
    EstExecuteeGCAUTRES,
    EstExecuteeOperationFDCDR,
    Groupe,
    Operation,
)


class EstExecuteeGCSUBFilter(django_filters.FilterSet):
    # Filtrer par titre d'une action
    action = django_filters.CharFilter(
        field_name="tache__activite__action__id", lookup_expr="exact"
    )

    # Filtrer par titre d'un programme
    programme = django_filters.CharFilter(
        field_name="tache__activite__action__programme__id",
        lookup_expr="exact",
    )

    # Filtrer par titre d'une activité
    activite = django_filters.CharFilter(
        field_name="tache__activite__id", lookup_expr="exact"
    )

    # Filtrer par titre d'un chapitre
    chapitre = django_filters.CharFilter(
        field_name="tache__activite__action__programme__chapitre__id",
        lookup_expr="exact",
    )

    class Meta:
        model = EstExecuteeGCSUB
        fields = ["action", "programme", "activite", "chapitre"]


class EstExecuteeGCAutresFilter(django_filters.FilterSet):
    # Filtrer par titre d'une action
    action = django_filters.CharFilter(
        field_name="tache__activite__action__id", lookup_expr="exact"
    )

    # Filtrer par titre d'un programme
    programme = django_filters.CharFilter(
        field_name="tache__activite__action__programme__id",
        lookup_expr="exact",
    )

    # Filtrer par titre d'une activité
    activite = django_filters.CharFilter(
        field_name="tache__activite__id", lookup_expr="exact"
    )

    # Filtrer par titre d'un chapitre
    chapitre = django_filters.CharFilter(
        field_name="tache__activite__action__programme__chapitre__id",
        lookup_expr="exact",
    )

    class Meta:
        model = EstExecuteeGCAUTRES
        fields = ["action", "programme", "activite", "chapitre"]


class EstExecuteeOperationFCPFilter(django_filters.FilterSet):
    # Filtrer par titre d'une action
    groupe = django_filters.CharFilter(
        field_name="groupe__groupe__id", lookup_expr="exact"
    )

    # Filtrer par titre d'un programme
    activite = django_filters.CharFilter(
        field_name="groupe__activite__id",
        lookup_expr="exact",
    )

    # Filtrer par titre d'un chapitre
    chapitre = django_filters.CharFilter(
        field_name="groupe__activite__action__programme__chapitre__id",
        lookup_expr="exact",
    )

    class Meta:
        model = EstExecuteeOperationFDCDR
        fields = ["groupe", "activite", "chapitre"]


class OperationFilter(django_filters.FilterSet):
    tache = django_filters.CharFilter(field_name="tache__id", lookup_expr="exact")
    groupe = django_filters.CharFilter(field_name="groupe", lookup_expr="exact")

    class Meta:
        model = Operation
        fields = ["tache", "groupe"]
class ConsommationFilter(django_filters.FilterSet):
    operation = django_filters.CharFilter(field_name="operation__id", lookup_expr="exact")

    class Meta:
        model = Consommation
        fields = [
            "operation",
        ]
class GroupeFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name="type", lookup_expr="exact")

    class Meta:
        model = Groupe
        fields = [
            "type",
        ]
