import re

def sanitize_email(email: str) -> str:

    return email.strip().lower()

def sanitize_string(s: str) -> str:

    return s.strip()

def validate_password(password: str) -> str:

    if len(password) < 8:
        raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Le mot de passe doit contenir au moins une lettre majuscule.")
    if not re.search(r"[a-z]", password):
        raise ValueError("Le mot de passe doit contenir au moins une lettre minuscule.")
    if not re.search(r"[0-9]", password):
        raise ValueError("Le mot de passe doit contenir au moins un chiffre.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Le mot de passe doit contenir au moins un caractère spécial.")
    return password
