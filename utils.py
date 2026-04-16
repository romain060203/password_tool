# utils.py
from typing import List

DEFAULT_COMMON_PATTERNS = [
    "123", "1234", "12345", "password", "qwerty", "admin", "letmein", "0000", "abcd"
]

def load_common_patterns(extra: List[str] = None) -> List[str]:
    patterns = DEFAULT_COMMON_PATTERNS.copy()
    if extra:
        patterns.extend(extra)
    return patterns