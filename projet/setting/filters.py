import django_filters
from django.db.models import Q
from functools import reduce
from operator import or_

from .models import Tache
from execution.models import Groupe


class TacheFilter(django_filters.FilterSet):
    groupe = django_filters.ModelChoiceFilter(
        field_name="operations__groupe",
        queryset=Groupe.objects.all(),
        label="Groupe",
        distinct=True,
    )

    class Meta:
        model = Tache
        fields = ["groupe"]


class ExerciceFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        # Obtenir tous les champs relationnels explicites du modèle
        related_fields = [
            field
            for field in qs.model._meta.get_fields()
            if field.is_relation
            and not field.auto_created  # Relations explicites uniquement
        ]

        # Vérifier si le champ est directement ou indirectement lié à Tache
        def is_related_to_tache(field):
            related_model = field.related_model
            if not related_model:
                return False
            return related_model == Tache or any(  # Directement lié à Tache
                f.related_model == Tache
                for f in related_model._meta.get_fields()
                if f.is_relation
            )  # Indirectement lié

        # Construire les lookup queries pour les relations valides
        lookup_queries = [
            Q(**{f"{field.name}__exercices__annee": value})
            for field in related_fields
            if is_related_to_tache(field)  # Inclure uniquement les champs liés à Tache
        ]

        # Appliquer le filtre si des relations valides sont trouvées
        if lookup_queries:
            return qs.filter(reduce(or_, lookup_queries))

        # Si aucune relation trouvée, renvoyer le queryset inchangé
        return qs
