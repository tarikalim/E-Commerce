import re


def validate_password(password):
    if len(password) >= 8 and re.search(r"[A-Z]", password) and re.search(r"[0-9]", password):
        return True
    return False
