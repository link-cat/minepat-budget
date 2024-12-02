import pandas as pd
import re
from datetime import datetime


from setting.models import (
    Region,
    Departement,
    Arrondissement,
    Chapitre,
    Programme,
    Action,
    Activite,
    Tache,
    Operation,
    TypeRessource,
    ModeGestion,
    NatureDepense,
    GroupeDepense,
    Exercice,
    Groupe,
    SUBGroupe,
)
from execution.models import (
    EstExecuteeAction,
    EstExecuteeFCPDR,
    EstExecuteeGCAUTRES,
    EstExecuteeGCSUB,
    EstExecuteeOperationFDCDR,
)
from contractualisation.models import PPM, JPM
from .utils import parse_date


# Variables pour stocker le nombre d'instances créées
logs = {
    "Region": 0,
    "Departement": 0,
    "Arrondissement": 0,
    "TypeRessource": 0,
    "ModeGestion": 0,
    "NatureDepense": 0,
    "Exercice": 0,
    "Chapitre": 0,
    "Programme": 0,
    "Action": 0,
    "Activite": 0,
    "Tache": 0,
    "Operation": 0,
    "GroupeDepense": 0,
}


def determine_line_type(row):
    text = row.iloc[0]
    if pd.isna(text):
        return None
    elif "Total" in text:
        return "Total"
    elif "Chapitre :" in text:
        return "Chapitre"
    elif "Programme :" in text:
        return "Programme"
    elif "Action :" in text:
        return "Action"
    elif "Projet/Activite :" in text or "Programme / Projet :" in text:
        return "Activite"
    elif "Groupe :" in text:
        return "Groupe"
    else:
        return "Autre"


def import_excel_file(file_path):
    # Lire toutes les feuilles du fichier Excel
    excel_data = pd.read_excel(file_path, sheet_name=None)
    # Traiter chaque feuille
    for sheet_name, sheet_data in excel_data.items():
        match sheet_name:
            case "TabExe-Prog":
                import_ExeProg(sheet_data)
            case "GC_FCPDR":
                import_GC_FCPDR(sheet_data)
            case "GC_AUTRES":
                import_GC_AUTRES(sheet_data)
            case "GC_SUBV-TRANSF":
                import_GC_SUB(sheet_data)
            case "TabOp_FCPDR":
                import_TabOp_FCPDR(sheet_data)
        # Vous pouvez ajouter le traitement des données ici


def import_bip_excel_file(file_path):
    # Lire toutes les feuilles du fichier Excel
    excel_data = pd.read_excel(file_path, sheet_name=None)
    # Traiter chaque feuille
    for sheet_name, sheet_data in excel_data.items():
        import_bip(sheet_data)


def import_excel_contract_file(file_path):
    # Lire toutes les feuilles du fichier Excel
    excel_data = pd.read_excel(file_path, sheet_name=None)
    # Traiter chaque feuille
    for sheet_name, sheet_data in excel_data.items():
        match sheet_name:
            case "PPM MINEPAT":
                import_ppm_minepat(sheet_data)
            case "JPM MINEPAT":
                import_jpm_minepat(sheet_data)
        # Vous pouvez ajouter le traitement des données ici


def import_ppm_minepat(sheet_data):
    for _, row in sheet_data.iterrows():
        if (
            _ < 3
        ):  # Ignorer les premières lignes si elles ne contiennent pas de données utiles
            continue

        # Rechercher une tâche correspondante en base de données via 'Désignation'
        tache = Tache.objects.filter(title_fr__icontains=row.iloc[1]).first()
        if tache is None:
            print(f"Tâche non trouvée pour la désignation: {row.iloc[1]}")
            continue

        # Vérifier si un PPM existe déjà pour cette tâche
        ppm = PPM.objects.filter(tache=tache).first()

        if ppm:
            # Mettre à jour les champs existants
            ppm.nature_prestations = row.iloc[2]
            ppm.montant_previsionnel = row.iloc[3]
            ppm.source_financement = row.iloc[4]
            ppm.autorite_contractante = row.iloc[5]
            ppm.mode_consultation_solicite = row.iloc[6]
            ppm.procedure = row.iloc[7]
            ppm.saisine_ac = parse_date(row.iloc[8])
            ppm.saisine_cpm = parse_date(row.iloc[9])
            ppm.examen_dao_cpm = parse_date(row.iloc[10])
            ppm.saisine_cccm_dao = parse_date(row.iloc[11])
            ppm.avis_cccm_dao = row.iloc[12]
            ppm.non_objection_bf_1 = row.iloc[13]
            ppm.date_publication_ao = parse_date(row.iloc[14])
            ppm.depouillement_offres = parse_date(row.iloc[15])
            ppm.analyse_offres_techniques = parse_date(row.iloc[16])
            ppm.examen_rapport_offres_techniques = parse_date(row.iloc[17])
            ppm.non_objection_bf_2 = row.iloc[18]
            ppm.ouverture_offres_financieres = parse_date(row.iloc[19])
            ppm.analyse_offres_financieres_synthese = parse_date(row.iloc[20])
            ppm.proposition_attribution_cpm = parse_date(row.iloc[21])
            ppm.saisine_cccm_attribution = parse_date(row.iloc[22])
            ppm.avis_cccm_attribution = row.iloc[23]
            ppm.non_objection_bf_3 = row.iloc[24]
            ppm.publication_resultats = parse_date(row.iloc[25])
            ppm.notification_decision_attribution = parse_date(row.iloc[26])
            ppm.preparation_projet_marche = parse_date(row.iloc[27])
            ppm.saisine_cpm_marche = parse_date(row.iloc[28])
            ppm.examen_projet_marche = parse_date(row.iloc[29])
            ppm.saisine_cccm_marche = parse_date(row.iloc[30])
            ppm.avis_cccm_projet_marche_gg = row.iloc[31]
            ppm.non_objection_bf_4 = row.iloc[32]
            ppm.date_signature_marche = parse_date(row.iloc[33])
            ppm.notification_marche = parse_date(row.iloc[34])
            ppm.demarrage_prestations = parse_date(row.iloc[35])
            ppm.reception_provisoire = parse_date(row.iloc[36])
            ppm.reception_definitive = parse_date(row.iloc[37])
            ppm.save()
            print(f"PPM mis à jour pour la tâche : {tache.title_fr}")
        else:
            # Créer un nouvel objet PPM
            PPM.objects.create(
                tache=tache,
                nature_prestations=row.iloc[2],
                montant_previsionnel=row.iloc[3],
                source_financement=row.iloc[4],
                autorite_contractante=row.iloc[5],
                mode_consultation_solicite=row.iloc[6],
                procedure=row.iloc[7],
                saisine_ac=parse_date(row.iloc[8]),
                saisine_cpm=parse_date(row.iloc[9]),
                examen_dao_cpm=parse_date(row.iloc[10]),
                saisine_cccm_dao=parse_date(row.iloc[11]),
                avis_cccm_dao=row.iloc[12],
                non_objection_bf_1=row.iloc[13],
                date_publication_ao=parse_date(row.iloc[14]),
                depouillement_offres=parse_date(row.iloc[15]),
                analyse_offres_techniques=parse_date(row.iloc[16]),
                examen_rapport_offres_techniques=parse_date(row.iloc[17]),
                non_objection_bf_2=row.iloc[18],
                ouverture_offres_financieres=parse_date(row.iloc[19]),
                analyse_offres_financieres_synthese=parse_date(row.iloc[20]),
                proposition_attribution_cpm=parse_date(row.iloc[21]),
                saisine_cccm_attribution=parse_date(row.iloc[22]),
                avis_cccm_attribution=row.iloc[23],
                non_objection_bf_3=row.iloc[24],
                publication_resultats=parse_date(row.iloc[25]),
                notification_decision_attribution=parse_date(row.iloc[26]),
                preparation_projet_marche=parse_date(row.iloc[27]),
                saisine_cpm_marche=parse_date(row.iloc[28]),
                examen_projet_marche=parse_date(row.iloc[29]),
                saisine_cccm_marche=parse_date(row.iloc[30]),
                avis_cccm_projet_marche_gg=row.iloc[31],
                non_objection_bf_4=row.iloc[32],
                date_signature_marche=parse_date(row.iloc[33]),
                notification_marche=parse_date(row.iloc[34]),
                demarrage_prestations=parse_date(row.iloc[35]),
                reception_provisoire=parse_date(row.iloc[36]),
                reception_definitive=parse_date(row.iloc[37]),
            )
            print(f"PPM créé pour la tâche : {tache.title_fr}")

    print("Importation terminée.")


def import_jpm_minepat(sheet_data):
    for _, row in sheet_data.iterrows():
        if _ < 3:
            continue

        tache = Tache.objects.filter(title_fr__icontains=row.iloc[1]).first()
        if tache is None:
            print(f"Tâche non trouvée pour la désignation: {row.iloc[1]}")
            continue

        # Vérifier si un JPM existe déjà pour cette tâche
        jpm = JPM.objects.filter(tache=tache).first()

        if jpm:
            # Mettre à jour les champs existants
            jpm.nature_prestations = row.iloc[2]
            jpm.montant_previsionnel = row.iloc[3]
            jpm.source_financement = row.iloc[4]
            jpm.autorite_contractante = row.iloc[5]
            jpm.mode_consultation = row.iloc[6]
            jpm.date_lancement_consultation = parse_date(row.iloc[7])
            jpm.date_attribution_marche = parse_date(row.iloc[8])
            jpm.date_signature_marche = parse_date(row.iloc[9])
            jpm.date_demarrage_prestations = parse_date(row.iloc[10])
            jpm.date_reception_prestations = parse_date(row.iloc[11])
            jpm.save()
            print(f"JPM mis à jour pour la tâche : {tache.title_fr}")
        else:
            # Créer un nouvel objet JPM
            JPM.objects.create(
                tache=tache,
                nature_prestations=row.iloc[2],
                montant_previsionnel=row.iloc[3],
                source_financement=row.iloc[4],
                autorite_contractante=row.iloc[5],
                mode_consultation=row.iloc[6],
                date_lancement_consultation=parse_date(row.iloc[7]),
                date_attribution_marche=parse_date(row.iloc[8]),
                date_signature_marche=parse_date(row.iloc[9]),
                date_demarrage_prestations=parse_date(row.iloc[10]),
                date_reception_prestations=parse_date(row.iloc[11]),
            )
            print(f"JPM créé pour la tâche : {tache.title_fr}")

    print("Importation terminée.")


def import_ExeProg(sheet_data):
    for _, row in sheet_data.iterrows():
        match determine_line_type(row):
            case "Chapitre":
                numero_chapitre = int(
                    re.search(r"Chapitre\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                chapitre = Chapitre.objects.get(code=numero_chapitre)
            case "Programme":
                numero_programme = int(
                    re.search(r"Programme\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                programme = Programme.objects.get(
                    chapitre=chapitre,
                    code=numero_programme,
                )
            case "Action":
                numero_action = int(
                    re.search(r"Action\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                action = Action.objects.get(
                    programme=programme,
                    code=numero_action,
                )
                exercice = Exercice.objects.get(annee=2024)
                execution = EstExecuteeAction.objects.create(
                    action=action,
                    exercice=exercice,
                    montant_ae_init=int(row.iloc[1]) * 1000,
                    montant_cp_init=int(row.iloc[2]) * 1000,
                    montant_ae_rev=int(row.iloc[3]) * 1000,
                    montant_cp_rev=int(row.iloc[4]) * 1000,
                    montant_ae_eng=int(row.iloc[5]) * 1000,
                    montant_cp_eng=int(row.iloc[6]) * 1000,
                    montant_liq=int(row.iloc[7]) * 1000,
                    ordonancement=int(row.iloc[8]) * 1000,
                    pourcentage_ae_eng=row.iloc[9],
                    pourcentage_cp_eng=row.iloc[10],
                    pourcentage_liq=row.iloc[11],
                    pourcentage_ord=row.iloc[12],
                    pourcentage_RPHY_cp=row.iloc[13],
                )


def import_TabOp_FCPDR(sheet_data):
    sheet_data.iloc[:, 6] = sheet_data.iloc[:, 6].fillna("0").astype(str)
    can_save = False
    for _, row in sheet_data.iterrows():
        match determine_line_type(row):
            case "Chapitre":
                numero_chapitre = int(
                    re.search(r"Chapitre\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                chapitre = Chapitre.objects.get(code=numero_chapitre)
            case "Activite":
                nom_activite = row.iloc[0].replace("Programme / Projet : ", "")
                activite = Activite.objects.filter(
                    title_fr__icontains=nom_activite,
                ).first()
            case "Groupe":
                numero_groupe = int(
                    re.search(r"Groupe\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                groupe, created = Groupe.objects.get_or_create(
                    code=numero_groupe,
                    defaults={
                        "title_fr": row.iloc[0].replace("Groupe :", ""),
                    },
                )
                can_save = True
            case "Autre":
                if can_save:
                    try:
                        if activite is None:
                            print(f"activite : {nom_activite} n'existe pas.")
                            continue
                        subgroupe, created = SUBGroupe.objects.get_or_create(
                            groupe=groupe,
                            activite=activite,
                            title_fr=row.iloc[0],
                        )
                        exercice = Exercice.objects.get(annee=2024)
                        execution = EstExecuteeOperationFDCDR.objects.create(
                            groupe=subgroupe,
                            exercice=exercice,
                            montant_ae=float(row.iloc[1]) * 1000,
                            montant_cp=float(row.iloc[2]) * 1000,
                            contrat_situation_actuelle=row.iloc[3],
                            montant_contrat=float(row.iloc[4]) * 1000,
                            date_demarrage_travaux=parse_date(row.iloc[5]),
                            delai_execution_contrat=int(row.iloc[6]),
                            montant_engage=float(row.iloc[7]) * 1000,
                            pourcentage_execution_physique_au_demarrage=float(
                                row.iloc[8]
                            ),
                            pourcentage_execution_physique_a_date=float(row.iloc[9]),
                            observation=row.iloc[10],
                        )
                    except Exception as e:
                        # Imprimer le type d'erreur et son message
                        print(f"Erreur : {e}")  # Message d'erreur
                        print(f"Type d'erreur : {type(e).__name__}")  # Type de l'erreur
            case "Total":
                can_save = False


def import_GC_FCPDR(sheet_data):
    sheet_data.iloc[:, 7] = sheet_data.iloc[:, 7].fillna("1/01/2024").astype(str)
    sheet_data.iloc[:, 8] = sheet_data.iloc[:, 8].fillna("0").astype(str)
    can_save = False
    for _, row in sheet_data.iterrows():
        match determine_line_type(row):
            case "Chapitre":
                numero_chapitre = int(
                    re.search(r"Chapitre\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                chapitre = Chapitre.objects.get(code=numero_chapitre)
            case "Programme":
                numero_programme = int(
                    re.search(r"Programme\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                programme = Programme.objects.get(
                    chapitre=chapitre,
                    code=numero_programme,
                )
            case "Action":
                numero_action = int(
                    re.search(r"Action\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                action = Action.objects.get(
                    programme=programme,
                    code=numero_action,
                )
            case "Activite":
                nom_activite = (
                    re.search(r"Projet/Activite\s*:\s*(.*)", row.iloc[0])
                    .group(1)
                    .replace('"-U', '" -U')
                )
                activite = Activite.objects.filter(
                    action=action,
                    title_fr__icontains=nom_activite,
                ).first()
                can_save = True
            case "Autre":
                if can_save:
                    try:
                        tache = Tache.objects.filter(
                            activite=activite, title_fr__icontains=row.iloc[0]
                        ).first()
                        exercice = Exercice.objects.get(annee=2024)
                        if tache is None:
                            print(f"la tache : {row.iloc[0]} n'existe pas")
                            continue
                        execution = EstExecuteeFCPDR.objects.create(
                            tache=tache,
                            exercice=exercice,
                            montant_ae_init=float(row.iloc[1]) * 1000,
                            montant_cp_init=float(row.iloc[2]) * 1000,
                            montant_ae_rev=float(row.iloc[3]) * 1000,
                            montant_cp_rev=float(row.iloc[4]) * 1000,
                            contrat_situation_actuelle=row.iloc[5],
                            montant_contrat=float(row.iloc[6]) * 1000,
                            date_demarrage_travaux=parse_date(row.iloc[7]),
                            delai_execution_contrat=int(row.iloc[8]),
                            montant_ae_eng=float(row.iloc[9]) * 1000,
                            montant_cp_eng=float(row.iloc[10]) * 1000,
                            montant_liq=float(row.iloc[11]) * 1000,
                            ordonancement=float(row.iloc[12]) * 1000,
                            pourcentage_ae_eng=float(row.iloc[13]),
                            pourcentage_cp_eng=float(row.iloc[14]),
                            pourcentage_liq=float(row.iloc[15]),
                            pourcentage_ord=float(row.iloc[16]),
                            prise_en_charge_TTC=float(row.iloc[17]),
                            paiement_net_HT=float(row.iloc[18]),
                            pourcentage_execution_physique_au_demarrage=float(
                                row.iloc[19]
                            ),
                            pourcentage_execution_physique_a_date=float(row.iloc[20]),
                            observations=row.iloc[21],
                        )
                    except Exception as e:
                        # Imprimer le type d'erreur et son message
                        print(f"Erreur : {e}")  # Message d'erreur
                        print(f"Type d'erreur : {type(e).__name__}")  # Type de l'erreur
            case "Total":
                can_save = False


def import_GC_AUTRES(sheet_data):
    sheet_data.iloc[:, 7] = sheet_data.iloc[:, 7].fillna("1/01/2024").astype(str)
    sheet_data.iloc[:, 8] = sheet_data.iloc[:, 8].fillna("0").astype(str)
    can_save = False
    for _, row in sheet_data.iterrows():
        match determine_line_type(row):
            case "Chapitre":
                numero_chapitre = int(
                    re.search(r"Chapitre\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                chapitre = Chapitre.objects.get(code=numero_chapitre)
            case "Programme":
                numero_programme = int(
                    re.search(r"Programme\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                programme = Programme.objects.get(
                    chapitre=chapitre,
                    code=numero_programme,
                )
            case "Action":
                numero_action = int(
                    re.search(r"Action\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                action = Action.objects.get(
                    programme=programme,
                    code=numero_action,
                )
            case "Activite":
                nom_activite = (
                    re.search(r"Projet/Activite\s*:\s*(.*)", row.iloc[0])
                    .group(1)
                    .replace('"-U', '" -U')
                )
                activite = Activite.objects.filter(
                    action=action,
                    title_fr__icontains=nom_activite,
                ).first()
                can_save = True
            case "Autre":
                if can_save:
                    try:
                        tache = Tache.objects.filter(
                            activite=activite, title_fr__icontains=row.iloc[0]
                        ).first()
                        exercice = Exercice.objects.get(annee=2024)
                        if tache is None:
                            print(f"la tache : {row.iloc[0]} n'existe pas")
                            continue
                        execution = EstExecuteeGCAUTRES.objects.create(
                            tache=tache,
                            exercice=exercice,
                            montant_ae_init=float(row.iloc[1]) * 1000,
                            montant_cp_init=float(row.iloc[2]) * 1000,
                            montant_ae_rev=float(row.iloc[3]) * 1000,
                            montant_cp_rev=float(row.iloc[4]) * 1000,
                            contrat_situation_actuelle=row.iloc[5],
                            montant_contrat=float(row.iloc[6]) * 1000,
                            date_demarrage_travaux=parse_date(row.iloc[7]),
                            delai_execution_contrat=int(row.iloc[8]),
                            montant_ae_eng=float(row.iloc[9]) * 1000,
                            montant_cp_eng=float(row.iloc[10]) * 1000,
                            montant_liq=float(row.iloc[11]) * 1000,
                            ordonancement=float(row.iloc[12]) * 1000,
                            pourcentage_ae_eng=float(row.iloc[13]),
                            pourcentage_cp_eng=float(row.iloc[14]),
                            pourcentage_liq=float(row.iloc[15]),
                            pourcentage_ord=float(row.iloc[16]),
                            prise_en_charge_TTC=float(row.iloc[17]),
                            paiement_net_HT=float(row.iloc[18]),
                            pourcentage_execution_physique_au_demarrage=float(
                                row.iloc[19]
                            ),
                            pourcentage_execution_physique_a_date=float(row.iloc[20]),
                            observations=row.iloc[21],
                        )
                    except Exception as e:
                        # Imprimer le type d'erreur et son message
                        print(f"Erreur : {e}")  # Message d'erreur
                        print(f"Type d'erreur : {type(e).__name__}")  # Type de l'erreur
            case "Total":
                can_save = False


def import_GC_SUB(sheet_data):
    sheet_data.iloc[:, 7] = sheet_data.iloc[:, 7].fillna("1/01/2024").astype(str)
    sheet_data.iloc[:, 8] = sheet_data.iloc[:, 8].fillna("0").astype(str)
    can_save = False
    for _, row in sheet_data.iterrows():
        match determine_line_type(row):
            case "Chapitre":
                numero_chapitre = int(
                    re.search(r"Chapitre\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                chapitre = Chapitre.objects.get(code=numero_chapitre)
            case "Programme":
                numero_programme = int(
                    re.search(r"Programme\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                programme = Programme.objects.get(
                    chapitre=chapitre,
                    code=numero_programme,
                )
            case "Action":
                numero_action = int(
                    re.search(r"Action\s*:\s*(\d+)", row.iloc[0]).group(1)
                )
                action = Action.objects.get(
                    programme=programme,
                    code=numero_action,
                )
            case "Activite":
                nom_activite = (
                    re.search(r"Projet/Activite\s*:\s*(.*)", row.iloc[0])
                    .group(1)
                    .replace('"-U', '" -U')
                )
                activite = Activite.objects.filter(
                    action=action,
                    title_fr__icontains=nom_activite,
                ).first()
                can_save = True
            case "Autre":
                if can_save:
                    try:
                        tache = Tache.objects.filter(
                            activite=activite, title_fr__icontains=row.iloc[0]
                        ).first()
                        exercice = Exercice.objects.get(annee=2024)
                        if tache is None:
                            print(f"la tache : {row.iloc[0]} n'existe pas")
                            continue
                        execution = EstExecuteeGCSUB.objects.create(
                            tache=tache,
                            exercice=exercice,
                            montant_ae_init=float(row.iloc[1]) * 1000,
                            montant_cp_init=float(row.iloc[2]) * 1000,
                            montant_ae_rev=float(row.iloc[3]) * 1000,
                            montant_cp_rev=float(row.iloc[4]) * 1000,
                            contrat_situation_actuelle=row.iloc[5],
                            montant_contrat=float(row.iloc[6]) * 1000,
                            date_demarrage_travaux=parse_date(row.iloc[7]),
                            delai_execution_contrat=int(row.iloc[8]),
                            montant_ae_eng=float(row.iloc[9]) * 1000,
                            montant_cp_eng=float(row.iloc[10]) * 1000,
                            montant_liq=float(row.iloc[11]) * 1000,
                            ordonancement=float(row.iloc[12]) * 1000,
                            pourcentage_ae_eng=float(row.iloc[13]),
                            pourcentage_cp_eng=float(row.iloc[14]),
                            pourcentage_liq=float(row.iloc[15]),
                            pourcentage_ord=float(row.iloc[16]),
                            prise_en_charge_TTC=float(row.iloc[17]),
                            paiement_net_HT=float(row.iloc[18]),
                            pourcentage_execution_physique_au_demarrage=float(
                                row.iloc[19]
                            ),
                            pourcentage_execution_physique_a_date=float(row.iloc[20]),
                            observations=row.iloc[21],
                        )
                    except Exception as e:
                        # Imprimer le type d'erreur et son message
                        print(f"Erreur : {e}")  # Message d'erreur
                        print(f"Type d'erreur : {type(e).__name__}")  # Type de l'erreur
            case "Total":
                can_save = False


def import_bip(sheet_data):
    for _, row in sheet_data.iterrows():
        regionFr = row["Région"].split("/")[0]
        regionEn = (
            row["Région"].split("/")[1]
            if len(row["Région"].split("/")) > 1
            else row["Région"].split("/")[0]
        )
        region, created = Region.objects.get_or_create(
            name_fr=regionFr,
            name_en=regionEn,
        )
        if created:
            logs["Region"] += 1

        departement, created = Departement.objects.get_or_create(
            name=row["Département"],
            region=region,
        )
        if created:
            logs["Departement"] += 1

        arrondissement, created = Arrondissement.objects.get_or_create(
            name=row["Arrondissement"],
            departement=departement,
        )
        if created:
            logs["Arrondissement"] += 1

        chapitre, created = Chapitre.objects.get_or_create(
            code=row["Code Chap."],
            defaults={
                "title_fr": row["LibFr. Chap."],
                "title_en": row["LibUk. Chap."],
            },
        )
        if created:
            logs["Chapitre"] += 1

        programme, created = Programme.objects.get_or_create(
            code=row["Code Prog."],
            chapitre=chapitre,
            defaults={
                "title_fr": row["LibFr. Progr."],
                "title_en": row["LibUk. Progr."],
            },
        )
        if created:
            logs["Programme"] += 1

        action, created = Action.objects.get_or_create(
            code=row["Code Action"],
            programme=programme,
            defaults={
                "title_fr": row["LibFr. Action"],
                "title_en": row["LibUk. Action"],
            },
        )
        if created:
            logs["Action"] += 1

        activite, created = Activite.objects.get_or_create(
            code=row["Code Projet"],
            action=action,
            defaults={
                "title_fr": row["LibFr. Projet"],
                "title_en": row["LibUk. Projet"],
            },
        )
        if created:
            logs["Activite"] += 1

        tache, created = Tache.objects.get_or_create(
            code=row["Code Tâche"],
            activite=activite,
            defaults={
                "title_fr": row["LibFr. Tâche"],
                "title_en": row["LibUk. Tâche"],
                "cout_tot": row["Dotation AE"],
                "montant_previsionnel": row["Dotation CP"],
                "montant_reel": row["Dotation CP"],
                "adjudicataire": row["Bénéficiaire"],
                "numero_notification": row["Num Carton"],
            },
        )
        if created:
            logs["Tache"] += 1

        operation, created = Operation.objects.get_or_create(
            tache=tache,
            defaults={
                "title_fr": row["LibFr. Tâche"],
                "title_en": row["LibUk. Tâche"],
            },
        )
        if created:
            logs["Operation"] += 1

        typeRessource, created = TypeRessource.objects.get_or_create(
            code=row["Lib. Source Fin."].split(" - ")[0],
            defaults={
                "title": row["Lib. Source Fin."].split(" - ")[1],
            },
        )
        if created:
            logs["TypeRessource"] += 1

        mode, created = ModeGestion.objects.get_or_create(
            code=row["Mode Gestion"],
            title=row["Lib. Mode de gestion"].split(" - ")[1],
            source=row["Source Fin."],
            type_ressource=typeRessource,
        )
        if created:
            logs["ModeGestion"] += 1

        groupe, created = GroupeDepense.objects.get_or_create(
            title=row["Titre"],
        )
        if created:
            logs["GroupeDepense"] += 1

        nature, created = NatureDepense.objects.get_or_create(
            code=row["Paragraphe"], title=row["Lib. Nature depense"], groupe=groupe
        )
        if created:
            logs["NatureDepense"] += 1

        exercice, created = Exercice.objects.get_or_create(
            annee=row["Année Dem."],
        )
        if created:
            logs["Exercice"] += 1

    print(logs)
