from rest_framework import serializers

from .models import EtapeContractualisation, Etape, PPM, JPM


class EtapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etape
        fields = "__all__"


class PPMSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPM
        fields = "__all__"


class JPMSerializer(serializers.ModelSerializer):
    class Meta:
        model = JPM
        fields = "__all__"


class EtapeContractualisationSerializer(serializers.ModelSerializer):
    title_display = serializers.CharField(source="get_title_display", read_only=True)

    class Meta:
        model = EtapeContractualisation
        fields = "__all__"
        read_only_fields = ["ecart_jours", "title_display"]


