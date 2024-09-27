import django_filters
from .models import EstExecuteeGCSUB, EstExecuteeGCAUTRES


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