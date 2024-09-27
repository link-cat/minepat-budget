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
)

from setting.models import Tache


class TacheTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache
        fields = ["title_fr", "title_en"]


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
