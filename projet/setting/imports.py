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
)
from execution.models import (
    EstExecuteeAction,
    EstExecuteeFCPDR,
    EstExecuteeGCAUTRES,
    EstExecuteeGCSUB,
)
from .utils import parse_date_or_default


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
    elif "Projet/Activite :" in text:
        return "Activite"
    else:
        return "Autre"


def import_excel_file(file_path):
    # Lire toutes les feuilles du fichier Excel
    excel_data = pd.read_excel(file_path, sheet_name=None)
    # Traiter chaque feuille
    for sheet_name, sheet_data in excel_data.items():
        match sheet_name:
            # case "TabOp_FCPDR":
            #     import_op_fcpdr(sheet_data)
            # case "TabExe-Prog":
            #     import_ExeProg(sheet_data)
            case "GC_FCPDR":
                import_GC_FCPDR(sheet_data)
            case "GC_AUTRES":
                import_GC_AUTRES(sheet_data)
            case "GC_SUBV-TRANSF":
                import_GC_SUB(sheet_data)
        # Vous pouvez ajouter le traitement des données ici


def import_bip_excel_file(file_path):
    # Lire toutes les feuilles du fichier Excel
    excel_data = pd.read_excel(file_path, sheet_name=None)
    # Traiter chaque feuille
    for sheet_name, sheet_data in excel_data.items():
        import_bip(sheet_data)


def import_op_fcpdr(sheet_data):
    for _, row in sheet_data.iterrows():
        print(row.iloc[1])


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
                    liquidation=int(row.iloc[7]) * 1000,
                    ordonancement=int(row.iloc[8]) * 1000,
                    pourcentage_ae_eng=row.iloc[9],
                    pourcentage_cp_eng=row.iloc[10],
                    pourcentage_liq=row.iloc[11],
                    pourcentage_ord=row.iloc[12],
                    pourcentage_RPHY_cp=row.iloc[13],
                )


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
                    tache = Tache.objects.filter(
                        activite=activite, title_fr__icontains=row.iloc[0]
                    ).first()
                    exercice = Exercice.objects.get(annee=2024)
                    execution = EstExecuteeFCPDR.objects.create(
                        tache=tache,
                        exercice=exercice,
                        montant_ae_init=float(row.iloc[1]) * 1000,
                        montant_cp_init=float(row.iloc[2]) * 1000,
                        montant_ae_rev=float(row.iloc[3]) * 1000,
                        montant_cp_rev=float(row.iloc[4]) * 1000,
                        contrat_situation_actuelle=row.iloc[5],
                        montant_contrat=float(row.iloc[6]) * 1000,
                        date_demarrage_travaux=parse_date_or_default(
                            row.iloc[7], "%d/%m/%Y", default_date=(2024, 1, 1)
                        ),
                        delai_execution_contrat=int(row.iloc[8]),
                        montant_ae_eng=float(row.iloc[9]) * 1000,
                        montant_cp_eng=float(row.iloc[10]) * 1000,
                        montant_liq=float(row.iloc[11]) * 1000,
                        liquidation=float(row.iloc[11]) * 1000,
                        ordonancement=float(row.iloc[12]) * 1000,
                        pourcentage_ae_eng=float(row.iloc[13]),
                        pourcentage_cp_eng=float(row.iloc[14]),
                        pourcentage_liq=float(row.iloc[15]),
                        pourcentage_ord=float(row.iloc[16]),
                        prise_en_charge_TTC=float(row.iloc[17]),
                        paiement_net_HT=float(row.iloc[18]),
                        pourcentage_execution_physique_au_demarrage=float(row.iloc[19]),
                        pourcentage_execution_physique_a_date=float(row.iloc[20]),
                        observations=row.iloc[21],
                    )
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
                    tache = Tache.objects.filter(
                        activite=activite, title_fr__icontains=row.iloc[0]
                    ).first()
                    exercice = Exercice.objects.get(annee=2024)
                    execution = EstExecuteeGCAUTRES.objects.create(
                        tache=tache,
                        exercice=exercice,
                        montant_ae_init=float(row.iloc[1]) * 1000,
                        montant_cp_init=float(row.iloc[2]) * 1000,
                        montant_ae_rev=float(row.iloc[3]) * 1000,
                        montant_cp_rev=float(row.iloc[4]) * 1000,
                        contrat_situation_actuelle=row.iloc[5],
                        montant_contrat=float(row.iloc[6]) * 1000,
                        date_demarrage_travaux=parse_date_or_default(
                            row.iloc[7], "%d/%m/%Y", default_date=(2024, 1, 1)
                        ),
                        delai_execution_contrat=int(row.iloc[8]),
                        montant_ae_eng=float(row.iloc[9]) * 1000,
                        montant_cp_eng=float(row.iloc[10]) * 1000,
                        montant_liq=float(row.iloc[11]) * 1000,
                        liquidation=float(row.iloc[11]) * 1000,
                        ordonancement=float(row.iloc[12]) * 1000,
                        pourcentage_ae_eng=float(row.iloc[13]),
                        pourcentage_cp_eng=float(row.iloc[14]),
                        pourcentage_liq=float(row.iloc[15]),
                        pourcentage_ord=float(row.iloc[16]),
                        prise_en_charge_TTC=float(row.iloc[17]),
                        paiement_net_HT=float(row.iloc[18]),
                        pourcentage_execution_physique_au_demarrage=float(row.iloc[19]),
                        pourcentage_execution_physique_a_date=float(row.iloc[20]),
                        observations=row.iloc[21],
                    )
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
                    tache = Tache.objects.filter(
                        activite=activite, title_fr__icontains=row.iloc[0]
                    ).first()
                    exercice = Exercice.objects.get(annee=2024)
                    execution = EstExecuteeGCSUB.objects.create(
                        tache=tache,
                        exercice=exercice,
                        montant_ae_init=float(row.iloc[1]) * 1000,
                        montant_cp_init=float(row.iloc[2]) * 1000,
                        montant_ae_rev=float(row.iloc[3]) * 1000,
                        montant_cp_rev=float(row.iloc[4]) * 1000,
                        contrat_situation_actuelle=row.iloc[5],
                        montant_contrat=float(row.iloc[6]) * 1000,
                        date_demarrage_travaux=parse_date_or_default(
                            row.iloc[7], "%d/%m/%Y", default_date=(2024, 1, 1)
                        ),
                        delai_execution_contrat=int(row.iloc[8]),
                        montant_ae_eng=float(row.iloc[9]) * 1000,
                        montant_cp_eng=float(row.iloc[10]) * 1000,
                        montant_liq=float(row.iloc[11]) * 1000,
                        liquidation=float(row.iloc[11]) * 1000,
                        ordonancement=float(row.iloc[12]) * 1000,
                        pourcentage_ae_eng=float(row.iloc[13]),
                        pourcentage_cp_eng=float(row.iloc[14]),
                        pourcentage_liq=float(row.iloc[15]),
                        pourcentage_ord=float(row.iloc[16]),
                        prise_en_charge_TTC=float(row.iloc[17]),
                        paiement_net_HT=float(row.iloc[18]),
                        pourcentage_execution_physique_au_demarrage=float(row.iloc[19]),
                        pourcentage_execution_physique_a_date=float(row.iloc[20]),
                        observations=row.iloc[21],
                    )
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
