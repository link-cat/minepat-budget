import pandas as pd


def import_excel_file(file_path):
    # Lire toutes les feuilles du fichier Excel
    excel_data = pd.read_excel(file_path, sheet_name=None)
    # Traiter chaque feuille
    for sheet_name, sheet_data in excel_data.items():
        print(f"Traitement de la feuille : {sheet_name}")
        # Exemple : afficher les premières lignes de la feuille
        print(sheet_data.head())
        # Vous pouvez ajouter le traitement des données ici
