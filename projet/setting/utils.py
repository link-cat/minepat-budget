from datetime import datetime
from django.utils import timezone
import math


def parse_date(date, default_date=None, date_format="%d/%m/%Y"):
    # Utiliser une date par défaut sous forme d'objet datetime
    if default_date is None:
        default_date = timezone.make_aware(datetime(2024, 1, 1))

    # Vérifier si la date est un NaN (ce qui nécessite que ce soit un float)
    if isinstance(date, float) and math.isnan(date):
        return default_date

    # Si la date est une chaîne de caractères, on tente de la parser
    if isinstance(date, str):
        try:
            parsed_date = datetime.strptime(date, date_format)
            return (
                timezone.make_aware(parsed_date)
                if timezone.is_naive(parsed_date)
                else parsed_date
            )
        except ValueError:
            print("Erreur : la chaîne n'est pas au bon format")
            return default_date

    # Si c'est déjà un objet datetime, on vérifie qu'il est "aware"
    elif isinstance(date, datetime):
        return timezone.make_aware(date) if timezone.is_naive(date) else date

    # Si ce n'est ni un float, ni une chaîne, ni une date, retourner la date par défaut
    else:
        print("Erreur : l'argument doit être une chaîne de caractères ou un datetime")
        return default_date
