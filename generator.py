# generator.py
import string
import secrets
from typing import List

DEFAULT_SPECIALS = "!@#$%^&*()-_=+[]{}|;:,.<>?/"

def build_charset(use_upper: bool, use_lower: bool, use_digits: bool, use_specials: bool, specials: str = DEFAULT_SPECIALS) -> str:
    charset = ""
    if use_upper:
        charset += string.ascii_uppercase
    if use_lower:
        charset += string.ascii_lowercase
    if use_digits:
        charset += string.digits
    if use_specials:
        charset += specials
    if not charset:
        raise ValueError("Au moins une catégorie de caractères doit être sélectionnée.")
    return charset

def generate_password(length: int = 12, use_upper: bool = True, use_lower: bool = True,
                      use_digits: bool = True, use_specials: bool = True, specials: str = DEFAULT_SPECIALS) -> str:
    if length < 1:
        raise ValueError("La longueur doit être >= 1.")
    charset = build_charset(use_upper, use_lower, use_digits, use_specials, specials)
    # Ensure at least one char from each selected class is present
    required_chars: List[str] = []
    if use_upper:
        required_chars.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        required_chars.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        required_chars.append(secrets.choice(string.digits))
    if use_specials:
        required_chars.append(secrets.choice(specials))
    if len(required_chars) > length:
        raise ValueError("La longueur est trop courte pour inclure toutes les classes de caractères demandées.")
    # Fill the rest
    remaining = [secrets.choice(charset) for _ in range(length - len(required_chars))]
    password_list = required_chars + remaining
    # Shuffle securely
    secrets.SystemRandom().shuffle(password_list)
    return ''.join(password_list)