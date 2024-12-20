from django.utils import timezone
from rest_framework import serializers

from .models import EtapeContractualisation, Etape, PPM, PieceJointe, PieceJointeContractualisation


class EtapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etape
        fields = "__all__"


class PPMSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPM
        fields = "__all__"


# class JPMSerializer(serializers.ModelSerializer):
#     tache = serializers.SerializerMethodField()

#     def get_tache(self, obj):
#         return {"id":obj.tache.id,"nom":obj.tache.title_fr, "code":obj.tache.code}

#     class Meta:
#         model = JPM
#         fields = "__all__"


class PieceJointeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceJointe
        fields = "__all__"
        read_only_fields = ["id", "date_upload"]

    def update(self, instance, validated_data):
        if "document" in validated_data:
            instance.date_upload = timezone.now()
        return super().update(instance, validated_data)
class PieceJointeContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceJointeContractualisation
        fields = "__all__"
        read_only_fields = ["id", "date_upload"]

    def update(self, instance, validated_data):
        if "document" in validated_data:
            instance.date_upload = timezone.now()
        return super().update(instance, validated_data)


class EtapeContractualisationSerializer(serializers.ModelSerializer):
    pieces_jointes = PieceJointeContractSerializer(many=True, read_only=True)
    etape = serializers.SerializerMethodField()
    etape_id = serializers.PrimaryKeyRelatedField(
        queryset=Etape.objects.all(), write_only=True, source="etape"
    )

    def validate(self, attrs):
        if EtapeContractualisation.objects.filter(
            tache=attrs["tache"], etape_id=attrs["etape_id"]
        ).exists():
            raise serializers.ValidationError(
                "Une étape contractualisation avec cette tâche et cette étape existe déjà."
            )
        return attrs

    def get_etape(self, obj):
        return {
            "id": obj.etape.id,
            "title": obj.etape.title,
            "type": obj.etape.type,
            "dated": obj.etape.dated,
            "acteurs": obj.etape.acteurs
        }

    class Meta:
        model = EtapeContractualisation
        fields = [
            "id",
            "etape_id",
            "etape",
            "tache",
            "date_prevue",
            "date_effective",
            "montant_prevu",
            "montant_reel",
            "taux_consomation",
            "observations",
            "is_finished",
            "pieces_jointes",
        ]
