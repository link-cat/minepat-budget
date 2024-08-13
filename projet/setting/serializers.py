from rest_framework import serializers
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
    class Meta:
        model = Tache
        fields = "__all__"


class GroupeDepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupeDepense
        fields = "__all__"


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = "__all__"


class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()

    class Meta:
        fields = ["file_uploaded"]
