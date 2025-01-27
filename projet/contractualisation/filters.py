import django_filters

from contractualisation.models import EtapeContractualisation,Maturation
from setting.filters import ExerciceFilter


class EtapeContractualisationFilter(django_filters.FilterSet):
    tache = django_filters.CharFilter(
        field_name="tache_id", lookup_expr="exact"
    )
    exercice = ExerciceFilter(label="Année d'exercice")

    class Meta:
        model = EtapeContractualisation
        fields = ["tache","exercice"]

class MaturationFilter(django_filters.FilterSet):
    tache = django_filters.CharFilter(
        field_name="tache_id", lookup_expr="exact"
    )

    class Meta:
        model = Maturation
        fields = ["tache"]
