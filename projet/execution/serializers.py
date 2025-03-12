from rest_framework import serializers
import math
import logging

logger = logging.getLogger(__name__)


from .models import (
    EstExecuteeAction,
    EstExecuteeFCPDR,
    EstExecuteeFCPTDD,
    EstExecuteeGCAUTRES,
    EstExecuteeGCSUB,
    EstExecuteeModeGestion,
    EstExecuteeOperationFDCDR,
    EstExecuteeSur,
    EstProgramme,
    Groupe,
    Operation,
    Consommation,
    PieceJointeConsommation,
)

from setting.models import Tache


class EstExecuteeActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstExecuteeAction
        fields = "__all__"
        read_only_fields = [
            "montant_ae_init",
            "montant_cp_init",
            "montant_ae_rev",
            "montant_cp_rev",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Remplace les valeurs NaN ou inf par 0 (ou une autre valeur)
        for key, value in data.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                data[key] = 0  # Remplacer par 0 ou une autre valeur par défaut

        return data


class EstExecuteeFCPDRSerializer(serializers.ModelSerializer):
    tache = serializers.SerializerMethodField()

    def get_tache(self, obj):
        return obj.tache.title_fr

    class Meta:
        model = EstExecuteeFCPDR
        fields = "__all__"
        read_only_fields = [
            "montant_ae_init",
            "montant_cp_init",
            "montant_ae_rev",
            "montant_cp_rev",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Remplace les valeurs NaN ou inf par 0 (ou une autre valeur)
        for key, value in data.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                data[key] = 0  # Remplacer par 0 ou une autre valeur par défaut

        return data


class EstExecuteeFCPTDDSerializer(serializers.ModelSerializer):
    tache = serializers.SerializerMethodField()

    def get_tache(self, obj):
        return obj.tache.title_fr

    class Meta:
        model = EstExecuteeFCPTDD
        fields = "__all__"
        read_only_fields = [
            "montant_ae_init",
            "montant_cp_init",
            "montant_ae_rev",
            "montant_cp_rev",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Remplace les valeurs NaN ou inf par 0 (ou une autre valeur)
        for key, value in data.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                data[key] = 0  # Remplacer par 0 ou une autre valeur par défaut

        return data


class EstExecuteeGCAUTRESSerializer(serializers.ModelSerializer):
    tache = serializers.SerializerMethodField()

    def get_tache(self, obj):
        return obj.tache.title_fr

    class Meta:
        model = EstExecuteeGCAUTRES
        fields = "__all__"
        read_only_fields = [
            "montant_ae_init",
            "montant_cp_init",
            "montant_ae_rev",
            "montant_cp_rev",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Remplace les valeurs NaN ou inf par 0 (ou une autre valeur)
        for key, value in data.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                data[key] = 0  # Remplacer par 0 ou une autre valeur par défaut

        return data


class EstExecuteeGCSUBSerializer(serializers.ModelSerializer):
    tache = serializers.SerializerMethodField()

    def get_tache(self, obj):
        return obj.tache.title_fr

    class Meta:
        model = EstExecuteeGCSUB
        fields = "__all__"
        read_only_fields = [
            "montant_ae_init",
            "montant_cp_init",
            "montant_ae_rev",
            "montant_cp_rev",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        logger.debug(f"Data before sanitization: {data}")

        # Remplace les valeurs NaN ou inf par 0 (ou une autre valeur)
        for key, value in data.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                data[key] = 0  # Remplacer par 0 ou une autre valeur par défaut

        logger.debug(f"Data after sanitization: {data}")
        return data


class EstExecuteeModeGestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstExecuteeModeGestion
        fields = "__all__"
        read_only_fields = [
            "montant_ae_init",
            "montant_cp_init",
            "montant_ae_rev",
            "montant_cp_rev",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Remplace les valeurs NaN ou inf par 0 (ou une autre valeur)
        for key, value in data.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                data[key] = 0  # Remplacer par 0 ou une autre valeur par défaut

        return data


class EstExecuteeOperationFDCDRSerializer(serializers.ModelSerializer):
    groupe = serializers.SerializerMethodField()

    def get_groupe(self, obj):
        return obj.groupe.title_fr

    class Meta:
        model = EstExecuteeOperationFDCDR
        fields = "__all__"
        read_only_fields = [
            "montant_ae_init",
            "montant_cp_init",
            "montant_ae_rev",
            "montant_cp_rev",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Remplace les valeurs NaN ou inf par 0 (ou une autre valeur)
        for key, value in data.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                data[key] = 0  # Remplacer par 0 ou une autre valeur par défaut

        return data


class EstExecuteeSurSerializer(serializers.ModelSerializer):
    tache = serializers.SerializerMethodField()

    def get_tache(self, obj):
        return obj.tache.title_fr

    class Meta:
        model = EstExecuteeSur
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Remplace les valeurs NaN ou inf par 0 (ou une autre valeur)
        for key, value in data.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                data[key] = 0  # Remplacer par 0 ou une autre valeur par défaut

        return data


class EstProgrammeSerializer(serializers.ModelSerializer):
    tache = serializers.SerializerMethodField()

    def get_tache(self, obj):
        return obj.tache.title_fr

    class Meta:
        model = EstProgramme
        fields = "__all__"
        read_only_fields = [
            "montant_ae_init",
            "montant_cp_init",
            "montant_ae_rev",
            "montant_cp_rev",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Remplace les valeurs NaN ou inf par 0 (ou une autre valeur)
        for key, value in data.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                data[key] = 0  # Remplacer par 0 ou une autre valeur par défaut

        return data


from django.utils import timezone


class PieceJointeConsommationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceJointeConsommation
        fields = "__all__"
        read_only_fields = ["id", "date_upload"]

    def update(self, instance, validated_data):
        if "document" in validated_data:
            instance.date_upload = timezone.now()
        return super().update(instance, validated_data)


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = "__all__"
        read_only_fields = [
            "montant_engage",
        ]


class ConsommationSerializer(serializers.ModelSerializer):
    pieces_jointes = PieceJointeConsommationSerializer(many=True, read_only=True)

    class Meta:
        model = Consommation
        fields = "__all__"


class GroupeExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe
        fields = "__all__"
