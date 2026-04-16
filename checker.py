# checker.py
import re
from typing import Dict, List, Tuple

COMMON_PATTERNS = [
    "123", "1234", "12345", "password", "qwerty", "admin", "letmein", "0000", "abcd"
]

def analyze_password(pw: str) -> Dict[str, object]:
    length = len(pw)
    has_upper = bool(re.search(r'[A-Z]', pw))
    has_lower = bool(re.search(r'[a-z]', pw))
    has_digit = bool(re.search(r'\d', pw))
    has_special = bool(re.search(r'[^A-Za-z0-9]', pw))
    classes = sum([has_upper, has_lower, has_digit, has_special])

    found_patterns: List[str] = []
    low_pw = pw.lower()
    for pat in COMMON_PATTERNS:
        if pat in low_pw:
            found_patterns.append(pat)

    entropy_estimate = estimate_entropy(length, classes)

    score, label = score_password(length, classes, found_patterns, entropy_estimate)

    feedback = build_feedback(length, classes, found_patterns, entropy_estimate, label)

    return {
        "password": pw,
        "length": length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "classes": classes,
        "found_patterns": found_patterns,
        "entropy_estimate": entropy_estimate,
        "score": score,
        "label": label,
        "feedback": feedback
    }

def estimate_entropy(length: int, classes: int) -> float:
    # Very simple estimate: log2(charset_size^length) = length * log2(charset_size)
    # charset_size approximated by classes: 26 for upper/lower, 10 digits, 32 specials
    size = 0
    if classes == 0:
        return 0.0
    # approximate mapping
    if classes == 1:
        size = 26
    elif classes == 2:
        size = 52
    elif classes == 3:
        size = 62
    elif classes >= 4:
        size = 94
    import math
    return round(length * math.log2(size), 2)

def score_password(length: int, classes: int, found_patterns: List[str], entropy: float) -> Tuple[int, str]:
    # Score 0..100
    score = 0
    # length contribution
    if length >= 12:
        score += 30
    elif length >= 10:
        score += 20
    elif length >= 8:
        score += 10
    else:
        score += 0
    # classes contribution
    score += classes * 15  # up to 60
    # entropy bonus
    if entropy >= 60:
        score += 10
    elif entropy >= 40:
        score += 5
    # penalty for patterns
    if found_patterns:
        score -= 30
    # clamp
    score = max(0, min(100, score))
    if score < 40:
        label = "Faible"
    elif score < 70:
        label = "Moyen"
    else:
        label = "Fort"
    return score, label

def build_feedback(length: int, classes: int, found_patterns: List[str], entropy: float, label: str) -> List[str]:
    fb = []
    if length < 12:
        fb.append("Allonger le mot de passe à au moins 12 caractères.")
    else:
        fb.append("Longueur suffisante.")
    if classes < 3:
        fb.append("Ajouter au moins trois types de caractères : majuscules, minuscules, chiffres, caractères spéciaux.")
    else:
        fb.append("Bonne diversité de caractères.")
    if found_patterns:
        fb.append(f"Éviter les motifs faibles détectés: {', '.join(found_patterns)}.")
    if entropy < 40:
        fb.append("Entropie estimée faible — utilisez une phrase de passe ou augmentez la longueur.")
    fb.append(f"Score final: {label} ({entropy} bits estimés).")
    return fb