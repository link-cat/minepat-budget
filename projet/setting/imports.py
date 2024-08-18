import pandas as pd


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


def import_excel_file(file_path):
    # Lire toutes les feuilles du fichier Excel
    excel_data = pd.read_excel(file_path, sheet_name=None)
    # Traiter chaque feuille
    for sheet_name, sheet_data in excel_data.items():
        match sheet_name:
            case "22":
                import_bip(sheet_data)
            case "TabOp_FCPDR":
                import_op_fcpdr(sheet_data)
        # Vous pouvez ajouter le traitement des données ici


def import_op_fcpdr(sheet_data):
    for _, row in sheet_data.iterrows():
        print(row.iloc[1])

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
            title=row["Source Fin."],
        )
        if created:
            logs["TypeRessource"] += 1

        mode, created = ModeGestion.objects.get_or_create(
            title=row["Mode Gestion"],
            type_ressource=typeRessource,
        )
        if created:
            logs["ModeGestion"] += 1

        nature, created = NatureDepense.objects.get_or_create(
            title=row["Grandes Masses"],
            mode=mode,
        )
        if created:
            logs["NatureDepense"] += 1

        groupe, created = GroupeDepense.objects.get_or_create(
            title=row["TITRE"],
        )
        if created:
            logs["GroupeDepense"] += 1

        exercice, created = Exercice.objects.get_or_create(
            annee=row["Année Dem."],
        )
        if created:
            logs["Exercice"] += 1

    print(logs)
