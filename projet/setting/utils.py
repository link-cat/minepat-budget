from datetime import datetime


def parse_date_or_default(date_str, date_format="%d/%m/%Y", default_date=None):
    if isinstance(date_str, str):
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            print("Erreur : la chaîne n'est pas au bon format ISO")
            return None
    else:
        print("Erreur : l'argument doit être une chaîne de caractères")
        return default_date

