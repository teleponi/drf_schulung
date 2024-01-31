from django.core.exceptions import ValidationError


def contains_xy(current_value) -> None:
    if "xy" not in current_value:
        raise ValidationError("Der Text muss die Zeichenfolge xy enthalten")