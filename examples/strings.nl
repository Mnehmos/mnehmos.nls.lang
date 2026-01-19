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
GUARDS:
  - max_length >= 4 -> ValueError("max_length must be >= 4")
RETURNS: text if len(text) <= max_length else text[:int(max_length) - 3] + "..."

[slugify]
PURPOSE: Convert text to URL-friendly slug format
INPUTS:
  • text: string
RETURNS: '-'.join(filter(None, ''.join(c if c.isalnum() else '-' for c in text.lower().strip()).split('-')))

[title-case]
PURPOSE: Convert text to title case
INPUTS:
  • text: string
RETURNS: text.title()
