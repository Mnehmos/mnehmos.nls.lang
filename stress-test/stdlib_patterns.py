
"""Test patterns from common Python utilities."""
from typing import Optional, Union, List, Dict, Any
from dataclasses import dataclass
import json

def parse_json_safe(text: str) -> Optional[dict]:
    """Parse JSON string safely, returning None on error."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None

def flatten_list(nested: List[List[Any]]) -> List[Any]:
    """Flatten a nested list by one level."""
    result = []
    for sublist in nested:
        result.extend(sublist)
    return result

def dict_merge(base: dict, update: dict) -> dict:
    """Merge two dictionaries, with update taking precedence."""
    merged = dict(base)
    merged.update(update)
    return merged

def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Divide a by b, returning default if b is zero."""
    if b == 0:
        return default
    return a / b

def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp a value between minimum and maximum."""
    return max(minimum, min(maximum, value))

def pluralize(word: str, count: int) -> str:
    """Return singular or plural form based on count."""
    if count == 1:
        return word
    return word + 's'
