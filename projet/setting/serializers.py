from rest_framework import serializers
from .models import (
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
    Region,
    Departement,
    Arrondissement,
    EtapeExecution,
    Groupe,
    SUBGroupe,
)


class TypeRessourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeRessource
        fields = "__all__"


class NatureDepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureDepense
        fields = "__all__"


class ModeGestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeGestion
        fields = "__all__"


class ExerciceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercice
        fields = "__all__"


class EtapeExecutionGlobSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapeExecutionGlob
        fields = "__all__"


class ChapitreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapitre
        fields = "__all__"


class ProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programme
        fields = "__all__"


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = "__all__"


class ActiviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activite
        fields = "__all__"


class TacheSerializer(serializers.ModelSerializer):
    current_step = serializers.SerializerMethodField()
    has_maturation = serializers.SerializerMethodField()

    def get_has_maturation(self, obj):
        return hasattr(obj, "maturation") and obj.maturation is not None

    def get_current_step(self, obj):
        return (
            {"id": obj.current_step.id, "title": obj.current_step.etape.title}
            if obj.current_step
            else None
        )

    class Meta:
        model = Tache
        fields = "__all__"
        extra_fields = ["has_maturation"]

    @property
    def data(self):
        data = super().data
        for field in self.Meta.extra_fields:
            data[field] = getattr(self, f"get_{field}")(self.instance)
        return data


class GroupeDepenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupeDepense
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class DepartementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departement
        fields = "__all__"


class ArrondissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrondissement
        fields = "__all__"


class GroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe
        fields = "__all__"


class SUBGroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SUBGroupe
        fields = "__all__"


class EtapeExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapeExecution
        fields = "__all__"


class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()

    class Meta:
        fields = ["file_uploaded"]


# for auth
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("password",)
