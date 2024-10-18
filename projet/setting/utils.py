from datetime import datetime
from django.utils import timezone
import math


def parse_date(date, default_date=None, date_format="%d/%m/%Y"):
    if default_date is None:
        default_date = timezone.make_aware(datetime(2024, 1, 1))

    if isinstance(date, str) and (not date.strip() or date in ["“ ”", ""]):
        return default_date

    if isinstance(date, float) and math.isnan(date):
        return default_date

    if isinstance(date, str):
        try:
            parsed_date = datetime.strptime(date.strip(), date_format)
            return (
                timezone.make_aware(parsed_date)
                if timezone.is_naive(parsed_date)
                else parsed_date
            )
        except ValueError as e:
            print(f"Erreur de parsing de la date {date}: {e}")
            return default_date

    elif isinstance(date, datetime):
        return timezone.make_aware(date) if timezone.is_naive(date) else date
    else:
        print("Erreur : l'argument doit être une chaîne de caractères ou un datetime")
        return default_date
