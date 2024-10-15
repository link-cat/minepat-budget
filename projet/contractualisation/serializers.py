from rest_framework import serializers

from .models import EtapeContractualisation,Etape


class EtapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etape
        fields = "__all__"

class EtapeContractualisationSerializer(serializers.ModelSerializer):
    title_display = serializers.CharField(source="get_title_display", read_only=True)

    class Meta:
        model = EtapeContractualisation
        fields = "__all__"
        read_only_fields = ["ecart_jours", "title_display"]
