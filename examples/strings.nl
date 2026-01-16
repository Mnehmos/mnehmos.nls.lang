# String Utilities Module
# Complex logic uses @literal blocks for exact code

@module strings
@target python

[is-empty]
PURPOSE: Check if a string is empty or whitespace only
INPUTS:
  • text: string
RETURNS: not text or text.isspace()

[truncate]
PURPOSE: Shorten text to a maximum length with ellipsis
INPUTS:
  • text: string
  • max_length: number

@literal python {
def truncate(text: str, max_length: int) -> str:
    """Shorten text to a maximum length with ellipsis."""
    if max_length < 4:
        raise ValueError("max_length must be >= 4")
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
}

[slugify]
PURPOSE: Convert text to URL-friendly slug format
INPUTS:
  • text: string

@literal python {
import re

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug format."""
    text = text.lower().strip()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^a-z0-9-]', '', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')
}

[title-case]
PURPOSE: Convert text to title case
INPUTS:
  • text: string
RETURNS: text.title()
