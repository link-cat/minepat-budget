from rest_framework import serializers
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


class EstExecuteeFCPDRSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstExecuteeFCPDR
        fields = "__all__"
        read_only_fields = [
            "montant_ae_init",
            "montant_cp_init",
            "montant_ae_rev",
            "montant_cp_rev",
        ]


class EstExecuteeFCPTDDSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstExecuteeFCPTDD
        fields = "__all__"
        read_only_fields = [
            "montant_ae_init",
            "montant_cp_init",
            "montant_ae_rev",
            "montant_cp_rev",
        ]


class EstExecuteeGCAUTRESSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstExecuteeGCAUTRES
        fields = "__all__"
        read_only_fields = [
            "montant_ae_init",
            "montant_cp_init",
            "montant_ae_rev",
            "montant_cp_rev",
        ]


class EstExecuteeGCSUBSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstExecuteeGCSUB
        fields = "__all__"
        read_only_fields = [
            "montant_ae_init",
            "montant_cp_init",
            "montant_ae_rev",
            "montant_cp_rev",
        ]


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


class EstExecuteeSurSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstExecuteeSur
        fields = "__all__"


class EstProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstProgramme
        fields = "__all__"
        read_only_fields = [
            "montant_ae_init",
            "montant_cp_init",
            "montant_ae_rev",
            "montant_cp_rev",
        ]
