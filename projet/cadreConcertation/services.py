from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from datetime import date
import calendar
from django.db.models import Sum, Avg, OuterRef, Subquery, FloatField
from setting.models import Tache
from execution.models import Operation, Consommation


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
        if code == "TABLEAU_SITUATION":
            new_content = generer_tableau_situation()
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