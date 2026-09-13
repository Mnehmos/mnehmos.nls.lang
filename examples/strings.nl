# String Utilities Module
# Slicing and the character-level slug rewrite are outside the checked
# expression core, so they use the sanctioned @literal escape hatch rather
# than being smuggled in as a dense one-line expression.

@module strings
@version 1.0.0
@target python

@literal python {
def slugify(text: str) -> str:
    """Convert text to URL-friendly slug format."""
    cleaned = "".join(c if c.isalnum() else "-" for c in text.lower().strip())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-")


def ellipsised(text: str, max_length: float) -> str:
    """Cut text to max_length characters, the last three being an ellipsis."""
    return text[: int(max_length) - 3] + "..."
}

[is-empty]
PURPOSE: Check if a string is empty or whitespace only
INPUTS:
  • text: string
RETURNS: len(text.strip()) == 0

[truncate]
PURPOSE: Shorten text to a maximum length with ellipsis
INPUTS:
  • text: string
  • max_length: number
GUARDS:
  - max_length >= 4 -> ValueError("max_length must be >= 4")
LOGIC:
  1. IF len(text) <= max_length THEN text -> result ELSE ellipsised(text, max_length) -> result
RETURNS: result

[title-case]
PURPOSE: Convert text to title case
INPUTS:
  • text: string
RETURNS: text.title()

@test [is-empty] {
  is_empty("") == True
  is_empty("   ") == True
  is_empty("hello") == False
}

@test [truncate] {
  truncate("hello", 10) == "hello"
  truncate("hello", 5) == "hello"
  truncate("hello world", 8) == "hello..."
}

@test [title-case] {
  title_case("hello world") == "Hello World"
  title_case("") == ""
}
