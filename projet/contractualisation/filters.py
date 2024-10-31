import django_filters

from contractualisation.models import EtapeContractualisation


class EtapeContractualisationFilter(django_filters.FilterSet):
    tache = django_filters.CharFilter(
        field_name="tache_id", lookup_expr="exact"
    )

    class Meta:
        model = EtapeContractualisation
        fields = ["tache"]
