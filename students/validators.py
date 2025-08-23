from django.core.exceptions import ValidationError


def validate_score(value):
    if not 0 <= value <= 100:
        raise ValidationError("Score must be between 0 and 100.")
