from datetime import datetime
from django.db.models import Sum, F, OuterRef, Subquery
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Avg, Count, F, Subquery, OuterRef, Max
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny


from execution.models import Consommation, Operation
from setting.models import Tache


@api_view(["GET"])
@permission_classes([AllowAny])
def BIPMetricsView(request):
    data = {}

    # Volume du BIP (Dotation totale)
    data["total_dotation"] = Tache.objects.aggregate(total=Sum('cout_tot'))['total'] or 0

    # Pourcentage d'exécution physique moyen basé sur la dernière consommation de chaque opération
    latest_consommations = (
            Consommation.objects.filter(id=Subquery(
                Consommation.objects.filter(operation=OuterRef('operation'))
                .order_by('-date_situation')
                .values('id')[:1]
            ))
        )
    data["pourcentage_exec_physique"] = latest_consommations.aggregate(moyenne=Avg('pourcentage_exec_physique'))['moyenne'] or 0

    # Pourcentage d'engagement (montant engagé vs montant prévisionnel)
    total_montant_previsionnel = Tache.objects.aggregate(total=Sum('montant_previsionnel'))['total'] or 1
    total_montant_engage = Operation.objects.aggregate(total=Sum('montant_engage'))['total'] or 0
    data["engagement_pourcentage"] = (total_montant_engage / total_montant_previsionnel) * 100

    # Évolution du %PHY sur l'année (groupé par mois, dernière consommation valable)
    data["evolution_phy"] = []
    current_year = datetime.now().year

    for month in range(1, 13):
        last_valid_consommations = Consommation.objects.filter(
                date_situation__year=current_year,
                date_situation__month=month
            ).order_by('-date_situation')

        if not last_valid_consommations.exists():
            last_valid_consommations = Consommation.objects.filter(
                    date_situation__year=current_year,
                    date_situation__month=month - 1 if month > 1 else 12
                ).order_by('-date_situation')

        avg_phy = last_valid_consommations.aggregate(moyenne=Avg('pourcentage_exec_physique'))['moyenne'] or 0
        data["evolution_phy"].append({'month': month, 'moyenne': avg_phy})

    # Répartition des tâches en fonction de leur état de forclusion
    data["forclusions"] = Tache.objects.values('etat_de_forclusion').annotate(count=Count('id'))

    # Informations générales
    data["total_ecarts"] = Tache.objects.aggregate(total=Sum(F('cout_tot') - F('montant_previsionnel')))['total'] or 0
    data["total_credits_forclos"] = Operation.objects.aggregate(total=Sum('montant'))['total'] or 0
    taches_par_region = (
        Tache.objects
        .filter(arrondissement__departement__region__isnull=False)
        .values(region_id=F('arrondissement__departement__region__id'),
                region_nom=F('arrondissement__departement__region__name_fr'))
        .annotate(nombre_taches=Count('id'))
    )
    data["taches_par_region"] = list(taches_par_region)

    return Response(data, status=status.HTTP_200_OK)
