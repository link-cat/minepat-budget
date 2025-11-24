from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from datetime import date
import calendar
from django.db.models import Sum, Avg, OuterRef, Subquery, FloatField
from setting.models import Tache
from execution.models import Groupe, Operation, Consommation


def last_day_of_month(year: int, month: int) -> date:
    """Retourne la dernière date du mois."""
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, last_day)
  
def safe_percent(value):
    """Transforme un float en '12%' ou None si pas de valeur."""
    if value is None:
        return None
    return f"{round(value)}%"


def compute_perf(current, previous):
    """
    current / previous sont des floats (pourcentages, ex: 55.0)
    Retourne (valeur_str, trend) ex: ('11%', 'up')
    """
    if current is None or previous is None:
        return None, None

    delta = round(current - previous)
    if delta > 0:
        trend = "up"
    elif delta < 0:
        trend = "down"
    else:
        trend = "neutral"

    return f"{delta}%", trend

def format_montant(montant):
    """Formate un montant en séparant les milliers par des espaces"""
    if montant is None:
        return "-"
    return f"{montant:,.0f}".replace(",", " ")

def format_pourcentage(valeur):
    """Formate un pourcentage"""
    if valeur is None:
        return "-"
    return f"{valeur}%"

def calculer_variation(actuel, precedent):
    """
    Calcule la variation entre deux valeurs et détermine la tendance
    Retourne un tuple (valeur_formatée, tendance)
    """
    if actuel is None or precedent is None:
        return None, None
    
    variation = actuel - precedent
    
    if variation > 0:
        return f"{variation}%", "up"
    elif variation < 0:
        return f"{variation}%", "down"
    else:
        return "0%", "neutral"

def get_month_snapshot_for_type(type_execution: str, year: int, month: int):
    """
    Calcule pour un type_execution donné :
    - provision totale (somme des montants prévisionnels des taches)
    - % phy moyen sur le mois
    - % engagement sur le mois
    en utilisant la dernière consommation disponible de chaque opération
    dont la date_situation <= fin_du_mois.
    """
    end_of_month = last_day_of_month(year, month)

    # Tâches concernées
    taches_qs = Tache.objects.filter(type_execution=type_execution)

    # Provision = somme des montants prévisionnels de ces tâches
    provision_total = (
        taches_qs.aggregate(total=Sum("montant_previsionnel"))["total"] or 0
    )

    # Toutes les opérations liées à ces tâches
    operations_qs = Operation.objects.filter(tache__in=taches_qs)

    if not operations_qs.exists():
        return {
            "provision": provision_total,
            "phy_percent": None,
            "eng_percent": None,
        }

    # Sous-requête : dernière consommation (par opération) dont date_situation <= fin_de_mois
    latest_conso_subquery = Consommation.objects.filter(
        operation=OuterRef("pk"),
        date_situation__lte=end_of_month,
    ).order_by("-date_situation", "-pk")

    operations_with_snapshot = operations_qs.annotate(
        latest_phy=Subquery(
            latest_conso_subquery.values("pourcentage_exec_physique")[:1]
        ),
        latest_engage=Subquery(
            latest_conso_subquery.values("montant_engage")[:1]
        ),
    )

    # Agrégats
    agg = operations_with_snapshot.aggregate(
        avg_phy=Avg("latest_phy"),
        total_engage=Sum("latest_engage"),
        total_planned=Sum("montant"),  # montant prévu à l'échelle de l'opération
    )

    avg_phy = agg["avg_phy"]
    total_engage = agg["total_engage"] or 0
    total_planned = agg["total_planned"] or 0

    # % physique = moyenne des % physiques
    phy_percent = avg_phy  # float ou None

    # % engagement = montant engagé / montant prévu * 100
    if total_planned > 0:
        eng_percent = (total_engage / total_planned) * 100.0
    else:
        eng_percent = None

    return {
        "provision": provision_total,
        "phy_percent": phy_percent,
        "eng_percent": eng_percent,
    }
    
TYPE_EXECUTION_LABELS = {
    Tache.TypeExecutionChoices.FCPDR: "Fonds de Contrepartie en DR",
    Tache.TypeExecutionChoices.ETAPUB: "Établissements publics",
    Tache.TypeExecutionChoices.STRUCTRAT: "Structures rattachées",
    Tache.TypeExecutionChoices.PIISAH: "PIISAH",
    Tache.TypeExecutionChoices.PLANUT: "PLANUT",  # ou PLANUT si tu veux rester strict
    Tache.TypeExecutionChoices.PLURIANNUEL: "Projets Pluriannuels",
    # tu peux étendre selon tes besoins
}

def generer_tableau_synthese(annee_courante=2025):
    """
    Génère les données pour le tableau de synthèse du BIP à partir de la base.
    On calcule pour l'exercice `annee_courante` :
      - Juin annee_courante
      - Juillet annee_courante
      - Juillet annee_courante - 1
    """

    # Références temporelles
    year_current = annee_courante
    year_previous = annee_courante - 1

    # Fin de mois
    mois_juin = 6
    mois_juillet = 7

    lignes_data = []
    total_provision = 0
    # Pour calculer des totaux sur les pourcentages, on fait comme toi : on recalcule à la fin
    totals = {
        "phy_juin": [],
        "phy_juillet": [],
        "phy_juillet_prev": [],
        "eng_juin": [],
        "eng_juillet": [],
        "eng_juillet_prev": [],
    }

    for type_code, label in TYPE_EXECUTION_LABELS.items():
        # Snapshot par mois
        snap_juin = get_month_snapshot_for_type(type_code, year_current, mois_juin)
        snap_juillet = get_month_snapshot_for_type(type_code, year_current, mois_juillet)
        snap_juillet_prev = get_month_snapshot_for_type(
            type_code, year_previous, mois_juillet
        )

        provision = snap_juin["provision"] or 0  # même provision pour l'exercice
        total_provision += provision

        phy_juin = snap_juin["phy_percent"]
        phy_juillet = snap_juillet["phy_percent"]
        phy_juillet_prev = snap_juillet_prev["phy_percent"]

        eng_juin = snap_juin["eng_percent"]
        eng_juillet = snap_juillet["eng_percent"]
        eng_juillet_prev = snap_juillet_prev["eng_percent"]

        # Perf physiques
        perf_phy_vs_juin_str, perf_phy_vs_juin_trend = compute_perf(
            phy_juillet, phy_juin
        )
        perf_phy_vs_2024_str, perf_phy_vs_2024_trend = compute_perf(
            phy_juillet, phy_juillet_prev
        )

        # Perf engagement
        perf_eng_vs_juin_str, perf_eng_vs_juin_trend = compute_perf(
            eng_juillet, eng_juin
        )
        perf_eng_vs_2024_str, perf_eng_vs_2024_trend = compute_perf(
            eng_juillet, eng_juillet_prev
        )

        # Alimente les listes de totaux (pour faire un total "moyenne" ensuite)
        if phy_juin is not None:
            totals["phy_juin"].append(phy_juin)
        if phy_juillet is not None:
            totals["phy_juillet"].append(phy_juillet)
        if phy_juillet_prev is not None:
            totals["phy_juillet_prev"].append(phy_juillet_prev)

        if eng_juin is not None:
            totals["eng_juin"].append(eng_juin)
        if eng_juillet is not None:
            totals["eng_juillet"].append(eng_juillet)
        if eng_juillet_prev is not None:
            totals["eng_juillet_prev"].append(eng_juillet_prev)

        lignes_data.append(
            {
                "nom": label,
                "provision": provision,
                "phy_juin_2025": safe_percent(phy_juin),
                "phy_juillet_2025": safe_percent(phy_juillet),
                "perf_phy_vs_juin": perf_phy_vs_juin_str,
                "perf_phy_vs_juin_trend": perf_phy_vs_juin_trend,
                "phy_juillet_2024": safe_percent(phy_juillet_prev),
                "perf_phy_vs_2024": perf_phy_vs_2024_str,
                "perf_phy_vs_2024_trend": perf_phy_vs_2024_trend,
                "eng_juin_2025": safe_percent(eng_juin),
                "eng_juillet_2025": safe_percent(eng_juillet),
                "perf_eng_vs_juin": perf_eng_vs_juin_str,
                "perf_eng_vs_juin_trend": perf_eng_vs_juin_trend,
                "eng_juillet_2024": safe_percent(eng_juillet_prev),
                "perf_eng_vs_2024": perf_eng_vs_2024_str,
                "perf_eng_vs_2024_trend": perf_eng_vs_2024_trend,
                "is_total": False,
            }
        )

    # Ligne TOTAL
    def avg_or_none(values):
        return sum(values) / len(values) if values else None

    total_phy_juin = avg_or_none(totals["phy_juin"])
    total_phy_juillet = avg_or_none(totals["phy_juillet"])
    total_phy_juillet_prev = avg_or_none(totals["phy_juillet_prev"])

    total_eng_juin = avg_or_none(totals["eng_juin"])
    total_eng_juillet = avg_or_none(totals["eng_juillet"])
    total_eng_juillet_prev = avg_or_none(totals["eng_juillet_prev"])

    total_perf_phy_vs_juin_str, total_perf_phy_vs_juin_trend = compute_perf(
        total_phy_juillet, total_phy_juin
    )
    total_perf_phy_vs_2024_str, total_perf_phy_vs_2024_trend = compute_perf(
        total_phy_juillet, total_phy_juillet_prev
    )
    total_perf_eng_vs_juin_str, total_perf_eng_vs_juin_trend = compute_perf(
        total_eng_juillet, total_eng_juin
    )
    total_perf_eng_vs_2024_str, total_perf_eng_vs_2024_trend = compute_perf(
        total_eng_juillet, total_eng_juillet_prev
    )

    lignes_data.append(
        {
            "nom": f"BIP {annee_courante} (TOTAL)",
            "provision": total_provision,
            "phy_juin_2025": safe_percent(total_phy_juin),
            "phy_juillet_2025": safe_percent(total_phy_juillet),
            "perf_phy_vs_juin": total_perf_phy_vs_juin_str,
            "perf_phy_vs_juin_trend": total_perf_phy_vs_juin_trend,
            "phy_juillet_2024": safe_percent(total_phy_juillet_prev),
            "perf_phy_vs_2024": total_perf_phy_vs_2024_str,
            "perf_phy_vs_2024_trend": total_perf_phy_vs_2024_trend,
            "eng_juin_2025": safe_percent(total_eng_juin),
            "eng_juillet_2025": safe_percent(total_eng_juillet),
            "perf_eng_vs_juin": total_perf_eng_vs_juin_str,
            "perf_eng_vs_juin_trend": total_perf_eng_vs_juin_trend,
            "eng_juillet_2024": safe_percent(total_eng_juillet_prev),
            "perf_eng_vs_2024": total_perf_eng_vs_2024_str,
            "perf_eng_vs_2024_trend": total_perf_eng_vs_2024_trend,
            "is_total": True,
        }
    )

    # Formater les provisions (séparateur de milliers) comme tu le faisais
    for ligne in lignes_data:
        if ligne["provision"]:
            ligne["provision"] = format_montant(ligne["provision"])

    context = {
        "data": {
            "lignes": lignes_data
        },
        "force_landscape": True,
    }

    return render_to_string("rapports/tables/table_synthese.html", context)
def generer_tableau_situation(annee_courante=2025):
    """
    Génère les données pour le tableau de synthèse du BIP à partir de la base.
    On calcule pour l'exercice `annee_courante` :
      - Juin annee_courante
      - Juillet annee_courante
      - Juillet annee_courante - 1
    """

    # Références temporelles
    year_current = annee_courante
    year_previous = annee_courante - 1

    # Fin de mois
    mois_juin = 6
    mois_juillet = 7

    lignes_data = []
    total_provision = 0
    # Pour calculer des totaux sur les pourcentages, on fait comme toi : on recalcule à la fin
    totals = {
        "phy_juin": [],
        "phy_juillet": [],
        "phy_juillet_prev": [],
        "eng_juin": [],
        "eng_juillet": [],
        "eng_juillet_prev": [],
    }

    for type_code, label in TYPE_EXECUTION_LABELS.items():
        # Snapshot par mois
        snap_juin = get_month_snapshot_for_type(type_code, year_current, mois_juin)
        snap_juillet = get_month_snapshot_for_type(type_code, year_current, mois_juillet)
        snap_juillet_prev = get_month_snapshot_for_type(
            type_code, year_previous, mois_juillet
        )

        provision = snap_juin["provision"] or 0  # même provision pour l'exercice
        total_provision += provision

        phy_juin = snap_juin["phy_percent"]
        phy_juillet = snap_juillet["phy_percent"]
        phy_juillet_prev = snap_juillet_prev["phy_percent"]

        eng_juin = snap_juin["eng_percent"]
        eng_juillet = snap_juillet["eng_percent"]
        eng_juillet_prev = snap_juillet_prev["eng_percent"]

        # Perf physiques
        perf_phy_vs_juin_str, perf_phy_vs_juin_trend = compute_perf(
            phy_juillet, phy_juin
        )

        # Perf engagement
        perf_eng_vs_juin_str, perf_eng_vs_juin_trend = compute_perf(
            eng_juillet, eng_juin
        )

        # Alimente les listes de totaux (pour faire un total "moyenne" ensuite)
        if phy_juin is not None:
            totals["phy_juin"].append(phy_juin)
        if phy_juillet is not None:
            totals["phy_juillet"].append(phy_juillet)
        if phy_juillet_prev is not None:
            totals["phy_juillet_prev"].append(phy_juillet_prev)

        if eng_juin is not None:
            totals["eng_juin"].append(eng_juin)
        if eng_juillet is not None:
            totals["eng_juillet"].append(eng_juillet)
        if eng_juillet_prev is not None:
            totals["eng_juillet_prev"].append(eng_juillet_prev)

        lignes_data.append(
            {
                "nom": label,
                "provision": provision,
                "phy_juin_2025": safe_percent(phy_juin),
                "phy_juillet_2025": safe_percent(phy_juillet),
                "perf_phy_vs_juin": perf_phy_vs_juin_str,
                "perf_phy_vs_juin_trend": perf_phy_vs_juin_trend,
                "phy_juillet_2024": safe_percent(phy_juillet_prev),
                "eng_juin_2025": safe_percent(eng_juin),
                "eng_juillet_2025": safe_percent(eng_juillet),
                "perf_eng_vs_juin": perf_eng_vs_juin_str,
                "perf_eng_vs_juin_trend": perf_eng_vs_juin_trend,
                "eng_juillet_2024": safe_percent(eng_juillet_prev),
                "is_total": False,
            }
        )

    # Ligne TOTAL
    def avg_or_none(values):
        return sum(values) / len(values) if values else None

    total_phy_juin = avg_or_none(totals["phy_juin"])
    total_phy_juillet = avg_or_none(totals["phy_juillet"])
    total_phy_juillet_prev = avg_or_none(totals["phy_juillet_prev"])

    total_eng_juin = avg_or_none(totals["eng_juin"])
    total_eng_juillet = avg_or_none(totals["eng_juillet"])
    total_eng_juillet_prev = avg_or_none(totals["eng_juillet_prev"])

    total_perf_phy_vs_juin_str, total_perf_phy_vs_juin_trend = compute_perf(
        total_phy_juillet, total_phy_juin
    )
    total_perf_eng_vs_juin_str, total_perf_eng_vs_juin_trend = compute_perf(
        total_eng_juillet, total_eng_juin
    )

    lignes_data.append(
        {
            "nom": f"BIP {annee_courante} (TOTAL)",
            "provision": total_provision,
            "phy_juin_2025": safe_percent(total_phy_juin),
            "phy_juillet_2025": safe_percent(total_phy_juillet),
            "perf_phy_vs_juin": total_perf_phy_vs_juin_str,
            "perf_phy_vs_juin_trend": total_perf_phy_vs_juin_trend,
            "phy_juillet_2024": safe_percent(total_phy_juillet_prev),
            "eng_juin_2025": safe_percent(total_eng_juin),
            "eng_juillet_2025": safe_percent(total_eng_juillet),
            "perf_eng_vs_juin": total_perf_eng_vs_juin_str,
            "perf_eng_vs_juin_trend": total_perf_eng_vs_juin_trend,
            "eng_juillet_2024": safe_percent(total_eng_juillet_prev),
            "is_total": True,
        }
    )

    # Formater les provisions (séparateur de milliers) comme tu le faisais
    for ligne in lignes_data:
        if ligne["provision"]:
            ligne["provision"] = format_montant(ligne["provision"])

    context = {
        "data": {
            "lignes": lignes_data
        },
        "force_landscape": True,
    }

    return render_to_string("rapports/tables/table_situation.html", context)

def generer_tableau_matrice_operation(annee_courante=2025, mois_courant=7):
    """
    Génère la matrice des opérations du Groupe 3 (FCPDR) pour un mois donné.
    - Colonnes : Projet/Programme, Opérations, Dotation, %Phy, %Eng, Observations
    - %Phy et %Eng calculés sur la dernière consommation de chaque opération
      dont date_situation <= fin du mois.
    """

    end_of_month = last_day_of_month(annee_courante, mois_courant)

    # On cible uniquement le groupe "groupe 3" et les tâches FCPDR
    ops_qs = (
        Operation.objects
        .filter(
            tache__type_execution=Tache.TypeExecutionChoices.FCPDR,
            groupe__title_fr__iexact="groupe 3",
        )
        .select_related("tache", "groupe", "tache__activite")
    )

    if not ops_qs.exists():
        # Rien à afficher, on renvoie un tableau vide "propre"
        context = {
            "data": {
                "annee": annee_courante,
                "groupes": [],
                "total": {
                    "dotation": format_montant(0),
                    "phy": None,
                    "eng": None,
                },
            },
            "force_landscape": True,
        }
        return render_to_string(
            "rapports/tables/table_matrice_operations.html", context
        )

    # Sous-requête : dernière consommation de chaque opération
    latest_conso_subquery = (
        Consommation.objects
        .filter(
            operation=OuterRef("pk"),
            date_situation__lte=end_of_month,
        )
        .order_by("-date_situation", "-pk")
    )

    ops_qs = ops_qs.annotate(
        last_phy=Subquery(
            latest_conso_subquery.values("pourcentage_exec_physique")[:1]
        ),
        last_engage=Subquery(
            latest_conso_subquery.values("montant_engage")[:1]
        ),
        last_obs=Subquery(
            latest_conso_subquery.values("observations")[:1]
        ),
    )

    # Regroupement par "Projet / Programme"
    grouped = {}
    total_dotation = 0
    phy_values = []  # pour moyenne globale
    total_engage_global = 0
    total_montant_global = 0

    for op in ops_qs:
        # Libellé du projet / programme
        projet_label = getattr(getattr(op.tache, "activite", None), "title_fr", None)
        if not projet_label:
            projet_label = op.tache.title_fr

        dotation = op.montant or 0
        total_dotation += dotation
        total_montant_global += dotation

        # %Phy
        phy = op.last_phy  # float ou None
        if phy is not None:
            phy_values.append(phy)

        # %Eng
        if dotation > 0 and op.last_engage is not None:
            eng_percent = (op.last_engage / dotation) * 100.0
            total_engage_global += op.last_engage or 0
        else:
            eng_percent = None

        row = {
            "operation": op.title_fr,
            "dotation": format_montant(dotation),
            "phy": safe_percent(phy),
            "eng": safe_percent(eng_percent),
            "observation": op.last_obs,
        }

        grouped.setdefault(projet_label, []).append(row)

    # Construction de la liste ordonnée pour le template
    groupes_list = []
    for projet, rows in grouped.items():
        groupes_list.append(
            {
                "projet": projet,
                "rows": rows,
            }
        )

    # On peut trier les projets par ordre alpha si tu veux un rendu stable
    groupes_list.sort(key=lambda g: g["projet"])

    # Totaux
    if phy_values:
        avg_phy_global = sum(phy_values) / len(phy_values)
    else:
        avg_phy_global = None

    if total_montant_global > 0 and total_engage_global > 0:
        eng_global = (total_engage_global / total_montant_global) * 100.0
    else:
        eng_global = None

    context = {
        "data": {
            "annee": annee_courante,
            "groupes": groupes_list,
            "total": {
                "dotation": format_montant(total_dotation),
                "phy": safe_percent(avg_phy_global),
                "eng": safe_percent(eng_global),
            },
        },
        "force_landscape": True,
    }

    return render_to_string(
        "rapports/tables/table_matrice_operations.html", context
    )
    
def generate_tableau_synthese_fcpdr(annee_courante=2025):
    """
    Génère la matrice du tableau FCPDR par groupe :
        - Provisonnel : Groupe 1
        - Normale : Groupe 2 + Groupe 3
    """
    from execution.models import Operation, Groupe
    from setting.models import Tache
    from django.db.models import Sum, Avg

    # --- Étape 1 : récupérer les groupes utiles ---
    groupes = {
        "Groupe 1": None,
        "Groupe 2": None,
        "Groupe 3": None,
    }

    all_groupes = Groupe.objects.filter(type="FCPDR")
    for g in all_groupes:
        if g.title_fr.lower() in ["groupe 1", "groupe 2", "groupe 3"]:
            groupes[g.title_fr] = g.id

    # --- Étape 2 : filtrer les opérations liées aux tâches FCPDR ---
    taches_fcpdr = Tache.objects.filter(type_execution=Tache.TypeExecutionChoices.FCPDR)

    operations = Operation.objects.filter(tache__in=taches_fcpdr)

    # --- Étape 3 : agrégation par groupe ---
    def compute_for_group(group_id):
        qs = operations.filter(groupe_id=group_id)
        if not qs.exists():
            return {
                "dotation": 0,
                "phy": None,
                "eng": None,
            }

        # Dernière consommation par opération
        latest_conso = Consommation.objects.filter(
            operation=OuterRef("pk")
        ).order_by("-date_situation", "-pk")

        qs = qs.annotate(
            last_phy=Subquery(latest_conso.values("pourcentage_exec_physique")[:1]),
            last_eng=Subquery(latest_conso.values("montant_engage")[:1]),
        )

        agg = qs.aggregate(
            dotation=Sum("montant"),
            phy=Avg("last_phy"),
            total_eng=Sum("last_eng"),
            total_planned=Sum("montant"),
        )

        # Défensive: convertir les agrégats None en 0 pour éviter les divisions par None
        total_eng = agg.get("total_eng") or 0
        total_planned = agg.get("total_planned") or 0
        avg_phy = agg.get("phy")

        eng_percent = None
        if total_planned > 0:
            eng_percent = (total_eng / total_planned) * 100.0

        # Ne pas forcer 0 pour phy/eng si la valeur est réellement inconnue (None)
        phy_value = round(avg_phy) if avg_phy is not None else None
        eng_value = round(eng_percent) if eng_percent is not None else None

        return {
            "dotation": agg.get("dotation") or 0,
            "phy": phy_value,
            "eng": eng_value,
        }

    g1 = compute_for_group(groupes["Groupe 1"])
    g2 = compute_for_group(groupes["Groupe 2"])
    g3 = compute_for_group(groupes["Groupe 3"])

    # --- Étape 4 : Totaux ---
    total1 = {
        "dotation": g1["dotation"],
        "phy": g1["phy"],
        "eng": g1["eng"],
    }

    total2 = {
        "dotation": g2["dotation"] + g3["dotation"],
        "phy": round(((g2["phy"] or 0) + (g3["phy"] or 0)) / 2) if (g2["phy"] is not None or g3["phy"] is not None) else None,
        "eng": round(((g2["eng"] or 0) + (g3["eng"] or 0)) / 2) if (g2["eng"] is not None or g3["eng"] is not None) else None,
    }

    total_final = {
        "dotation": total1["dotation"] + total2["dotation"],
        "phy": round(((total1["phy"] or 0) + (total2["phy"] or 0)) / 2),
        "eng": round(((total1["eng"] or 0) + (total2["eng"] or 0)) / 2),
    }
    
    year_current = annee_courante
    year_previous = annee_courante - 1
    mois_juin = 6
    mois_juillet = 7

    snap_juin = get_month_snapshot_for_type(
        Tache.TypeExecutionChoices.FCPDR, year_current, mois_juin
    )
    snap_juillet = get_month_snapshot_for_type(
        Tache.TypeExecutionChoices.FCPDR, year_current, mois_juillet
    )
    snap_juillet_prev = get_month_snapshot_for_type(
        Tache.TypeExecutionChoices.FCPDR, year_previous, mois_juillet
    )

    provision = snap_juin["provision"] or 0

    phy_juin = snap_juin["phy_percent"]
    phy_juillet = snap_juillet["phy_percent"]
    phy_juillet_prev = snap_juillet_prev["phy_percent"]

    eng_juin = snap_juin["eng_percent"]
    eng_juillet = snap_juillet["eng_percent"]
    eng_juillet_prev = snap_juillet_prev["eng_percent"]

    # Perf physiques
    perf_phy_vs_juin_str, perf_phy_vs_juin_trend = compute_perf(
        phy_juillet, phy_juin
    )
    perf_phy_vs_2024_str, perf_phy_vs_2024_trend = compute_perf(
        phy_juillet, phy_juillet_prev
    )

    # Perf engagement
    perf_eng_vs_juin_str, perf_eng_vs_juin_trend = compute_perf(
        eng_juillet, eng_juin
    )
    perf_eng_vs_2024_str, perf_eng_vs_2024_trend = compute_perf(
        eng_juillet, eng_juillet_prev
    )

    fcpdr_data = {
        "nom": "Fonds de Contrepartie en DR",
        "provision": format_montant(provision),

        "phy_juin_2025": safe_percent(phy_juin),
        "phy_juillet_2025": safe_percent(phy_juillet),
        "perf_phy_vs_juin": perf_phy_vs_juin_str,
        "perf_phy_vs_juin_trend": perf_phy_vs_juin_trend,
        "phy_juillet_2024": safe_percent(phy_juillet_prev),
        "perf_phy_vs_2024": perf_phy_vs_2024_str,
        "perf_phy_vs_2024_trend": perf_phy_vs_2024_trend,

        "eng_juin_2025": safe_percent(eng_juin),
        "eng_juillet_2025": safe_percent(eng_juillet),
        "perf_eng_vs_juin": perf_eng_vs_juin_str,
        "perf_eng_vs_juin_trend": perf_eng_vs_juin_trend,
        "eng_juillet_2024": safe_percent(eng_juillet_prev),
        "perf_eng_vs_2024": perf_eng_vs_2024_str,
        "perf_eng_vs_2024_trend": perf_eng_vs_2024_trend,
    }

    # ------------- CONTEXTE GLOBAL POUR LE TEMPLATE -------------

    context = {
        "matrice": {
            "g1": g1,
            "g2": g2,
            "g3": g3,
            "t1": total1,
            "t2": total2,
            "tf": total_final,
        },
        "fcpdr": fcpdr_data,
        "annee": annee_courante,
    }

    return render_to_string("rapports/tables/table_synthese_fcpdr.html", context)
  
  
def get_month_snapshot_for_transferts(year: int, month: int):
    """
    Snapshot mensuel pour les TRANSFERTS :
    - on prend toutes les opérations dont le groupe est de type SUBV (Transferts/Subventions)
    - provision = somme des montants prévisionnels des tâches liées
    - phy_percent = moyenne des % physiques de la dernière conso par opération
    - eng_percent = total montants engagés / total montants opérations
    """
    end_of_month = last_day_of_month(year, month)

    ops_qs = Operation.objects.filter(
        groupe__type=Groupe.TypeChoices.SUBV
    )

    if not ops_qs.exists():
        return {
            "provision": 0,
            "phy_percent": None,
            "eng_percent": None,
        }

    # Provision = somme des montants prévisionnels des tâches impliquées
    tache_ids = ops_qs.values_list("tache_id", flat=True).distinct()
    provision_total = (
        Tache.objects.filter(id__in=tache_ids)
        .aggregate(total=Sum("montant_previsionnel"))["total"]
        or 0
    )

    latest_conso = Consommation.objects.filter(
        operation=OuterRef("pk"),
        date_situation__lte=end_of_month,
    ).order_by("-date_situation", "-pk")

    ops_annotated = ops_qs.annotate(
        last_phy=Subquery(latest_conso.values("pourcentage_exec_physique")[:1]),
        last_eng=Subquery(latest_conso.values("montant_engage")[:1]),
    )

    agg = ops_annotated.aggregate(
        avg_phy=Avg("last_phy"),
        total_eng=Sum("last_eng"),
        total_planned=Sum("montant"),
    )

    avg_phy = agg["avg_phy"]
    total_eng = agg["total_eng"] or 0
    total_planned = agg["total_planned"] or 0

    phy_percent = avg_phy if avg_phy is not None else None
    eng_percent = (total_eng / total_planned) * 100.0 if total_planned > 0 else None

    return {
        "provision": provision_total,
        "phy_percent": phy_percent,
        "eng_percent": eng_percent,
    }


def generate_tableau_synthese_transferts(annee_courante=2025):
    """
    Génère le double tableau 'Transferts' :

    1) Tableau du haut :
        - Procédure ordinaire
        - Procédure dérogatoire
        + Total

       Basé sur les opérations dont groupe.type = SUBV.

    2) Tableau du bas :
        - Ligne 'Transferts' équivalente au tableau de synthèse
          (comme la ligne FCPDR, mais ici pour les transferts).
    """

    # --------- TABLEAU DU HAUT : PROCÉDURE ORDINAIRE / DÉROGATOIRE ---------

    # On récupère les groupes SUBV utiles
    groupes_ids = {
        "Procédure ordinaire": None,
        "Procédure dérogatoire": None,
    }

    for g in Groupe.objects.filter(type=Groupe.TypeChoices.SUBV):
        title = g.title_fr.strip().lower()
        if title == "procédure ordinaire":
            groupes_ids["Procédure ordinaire"] = g.id
        elif title == "procédure dérogatoire":
            groupes_ids["Procédure dérogatoire"] = g.id

    ops_qs = Operation.objects.filter(
        groupe__type=Groupe.TypeChoices.SUBV
    )

    def compute_for_group(group_id):
        qs = ops_qs.filter(groupe_id=group_id)
        if not qs.exists():
            return {
                "dotation": 0,
                "attribue": 0,
                "phy": None,
                "eng": None,
            }

        latest_conso = Consommation.objects.filter(
            operation=OuterRef("pk")
        ).order_by("-date_situation", "-pk")

        qs = qs.annotate(
            last_phy=Subquery(
                latest_conso.values("pourcentage_exec_physique")[:1]
            ),
            last_eng=Subquery(
                latest_conso.values("montant_engage")[:1]
            ),
            last_contrat=Subquery(
                latest_conso.values("montant_contrat")[:1]
            ),
        )

        agg = qs.aggregate(
            dotation=Sum("montant"),
            attribue=Sum("last_contrat"),
            avg_phy=Avg("last_phy"),
            total_eng=Sum("last_eng"),
            total_planned=Sum("montant"),
        )

        dotation = agg["dotation"] or 0
        attribue = agg["attribue"] or 0
        phy = agg["avg_phy"]
        total_eng = agg["total_eng"] or 0
        total_planned = agg["total_planned"] or 0

        eng_percent = (total_eng / total_planned) * 100.0 if total_planned > 0 else None

        return {
            "dotation": dotation,
            "attribue": attribue,
            "phy": round(phy) if phy is not None else None,
            "eng": round(eng_percent) if eng_percent is not None else None,
        }

    ord_data = compute_for_group(groupes_ids["Procédure ordinaire"])
    dero_data = compute_for_group(groupes_ids["Procédure dérogatoire"])

    def add_or_zero(a, b):
        return (a or 0) + (b or 0)

    def avg_or_none(*vals):
        vals = [v for v in vals if v is not None]
        return round(sum(vals) / len(vals)) if vals else None

    total_data = {
        "dotation": add_or_zero(ord_data["dotation"], dero_data["dotation"]),
        "attribue": add_or_zero(ord_data["attribue"], dero_data["attribue"]),
        "phy": avg_or_none(ord_data["phy"], dero_data["phy"]),
        "eng": avg_or_none(ord_data["eng"], dero_data["eng"]),
    }

    # Formatage montants pour le template
    for d in (ord_data, dero_data, total_data):
        d["dotation_fmt"] = format_montant(d["dotation"])
        d["attribue_fmt"] = format_montant(d["attribue"])

    year_current = annee_courante
    year_previous = annee_courante - 1
    mois_juin = 6
    mois_juillet = 7

    snap_juin = get_month_snapshot_for_transferts(year_current, mois_juin)
    snap_juillet = get_month_snapshot_for_transferts(year_current, mois_juillet)
    snap_juillet_prev = get_month_snapshot_for_transferts(year_previous, mois_juillet)

    provision = snap_juin["provision"] or 0
    phy_juin = snap_juin["phy_percent"]
    phy_juillet = snap_juillet["phy_percent"]
    phy_juillet_prev = snap_juillet_prev["phy_percent"]

    eng_juin = snap_juin["eng_percent"]
    eng_juillet = snap_juillet["eng_percent"]
    eng_juillet_prev = snap_juillet_prev["eng_percent"]

    # Perf physiques
    perf_phy_vs_juin_str, perf_phy_vs_juin_trend = compute_perf(
        phy_juillet, phy_juin
    )
    perf_phy_vs_2024_str, perf_phy_vs_2024_trend = compute_perf(
        phy_juillet, phy_juillet_prev
    )

    # Perf engagement
    perf_eng_vs_juin_str, perf_eng_vs_juin_trend = compute_perf(
        eng_juillet, eng_juin
    )
    perf_eng_vs_2024_str, perf_eng_vs_2024_trend = compute_perf(
        eng_juillet, eng_juillet_prev
    )

    transferts_data = {
        "nom": "Transferts",
        "provision": format_montant(provision),
        "phy_juin_2025": safe_percent(phy_juin),
        "phy_juillet_2025": safe_percent(phy_juillet),
        "perf_phy_vs_juin": perf_phy_vs_juin_str,
        "perf_phy_vs_juin_trend": perf_phy_vs_juin_trend,
        "phy_juillet_2024": safe_percent(phy_juillet_prev),
        "perf_phy_vs_2024": perf_phy_vs_2024_str,
        "perf_phy_vs_2024_trend": perf_phy_vs_2024_trend,
        "eng_juin_2025": safe_percent(eng_juin),
        "eng_juillet_2025": safe_percent(eng_juillet),
        "perf_eng_vs_juin": perf_eng_vs_juin_str,
        "perf_eng_vs_juin_trend": perf_eng_vs_juin_trend,
        "eng_juillet_2024": safe_percent(eng_juillet_prev),
        "perf_eng_vs_2024": perf_eng_vs_2024_str,
        "perf_eng_vs_2024_trend": perf_eng_vs_2024_trend,
    }

    context = {
        "top": {
            "ordinaire": ord_data,
            "derogatoire": dero_data,
            "total": total_data,
        },
        "bottom": transferts_data,
        "annee": annee_courante,
    }

    return render_to_string(
        "rapports/tables/table_synthese_transferts.html", context
    )
  
def generer_tableau_avancement():
    """Génère le tableau d'avancement - À implémenter"""
    # TODO: Implémenter selon vos besoins
    return render_to_string('rapports/tables/table_avancement.html', {})


def process_dynamic_html(html_content):
    """
    Parse le HTML de TinyMCE et remplace les placeholders par les vrais tableaux
    """
    if not html_content:
        return ""
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Trouver tous les placeholders grâce à la classe définie dans le React
    placeholders = soup.find_all("div", class_="dynamic-placeholder")
    
    for div in placeholders:
        code = div.get("data-code")
        new_content = None
        
        if code == "TABLEAU_SYNTHESE":
            new_content = generer_tableau_synthese()
        elif code == "TABLEAU_SITUATION":
            new_content = generer_tableau_situation()
        elif code == "TABLEAU_MATRICE_OPERATIONS":
            new_content = generer_tableau_matrice_operation()
        elif code == "TABLEAU_SYNTHESE_FCPDR":
            new_content = generate_tableau_synthese_fcpdr()
        elif code == "TABLEAU_TRANSFERTS":
          new_content = generate_tableau_synthese_transferts()
        elif code == "TABLEAU_AVANCEMENT":
            new_content = generer_tableau_avancement()
        elif code == "LISTE_RETARDS":
            # new_content = generer_liste_retards()
            pass
        
        # Si on a généré du contenu, on remplace le DIV placeholder
        if new_content:
            # On crée un nouvel objet BeautifulSoup à partir du HTML généré
            table_soup = BeautifulSoup(new_content, 'html.parser')
            # On remplace le div placeholder par le nouveau contenu
            div.replace_with(table_soup)
        else:
            # Si pas de contenu trouvé, on supprime le placeholder proprement
            div.decompose()
    
    return str(soup)