import re
from typing import Dict


def render_template(template: str, variables: Dict[str, str]) -> str:
    """
    Simple template variable substitution
    Replaces {{variable}} with actual values
    """
    result = template
    for key, value in variables.items():
        pattern = r'\{\{\s*' + re.escape(key) + r'\s*\}\}'
        result = re.sub(pattern, str(value), result)
    return result
