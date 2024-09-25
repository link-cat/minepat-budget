import django_filters
from .models import EstExecuteeGCSUB, EstExecuteeGCAUTRES


class EstExecuteeGCSUBFilter(django_filters.FilterSet):
    # Filtrer par titre d'une action
    action = django_filters.CharFilter(
        field_name="tache__activite__action__title_fr", lookup_expr="icontains"
    )

    # Filtrer par titre d'un programme
    programme = django_filters.CharFilter(
        field_name="tache__activite__action__programme__title_fr",
        lookup_expr="icontains",
    )

    # Filtrer par titre d'une activité
    activite = django_filters.CharFilter(
        field_name="tache__activite__title_fr", lookup_expr="icontains"
    )

    # Filtrer par titre d'un chapitre
    chapitre = django_filters.CharFilter(
        field_name="tache__activite__action__programme__chapitre__title_fr",
        lookup_expr="icontains",
    )

    class Meta:
        model = EstExecuteeGCSUB
        fields = ["action", "programme", "activite", "chapitre"]


class EstExecuteeGCAutresFilter(django_filters.FilterSet):
    # Filtrer par titre d'une action
    action = django_filters.CharFilter(
        field_name="tache__activite__action__title_fr", lookup_expr="icontains"
    )

    # Filtrer par titre d'un programme
    programme = django_filters.CharFilter(
        field_name="tache__activite__action__programme__title_fr",
        lookup_expr="icontains",
    )

    # Filtrer par titre d'une activité
    activite = django_filters.CharFilter(
        field_name="tache__activite__title_fr", lookup_expr="icontains"
    )

    # Filtrer par titre d'un chapitre
    chapitre = django_filters.CharFilter(
        field_name="tache__activite__action__programme__chapitre__title_fr",
        lookup_expr="icontains",
    )

    class Meta:
        model = EstExecuteeGCAUTRES
        fields = ["action", "programme", "activite", "chapitre"]
