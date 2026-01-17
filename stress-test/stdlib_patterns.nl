@module stdlib-patterns
@target python

[parse-json-safe]
PURPOSE: Parse JSON string safely, returning None on error.
INPUTS:
  - text: string
RETURNS: json.loads(text)

[flatten-list]
PURPOSE: Flatten a nested list by one level.
INPUTS:
  - nested: list of list of any
LOGIC:
  1. result = []
RETURNS: result

[dict-merge]
PURPOSE: Merge two dictionaries, with update taking precedence.
INPUTS:
  - base: dictionary
  - update: dictionary
LOGIC:
  1. merged = dict(base)
RETURNS: merged

[safe-divide]
PURPOSE: Divide a by b, returning default if b is zero.
INPUTS:
  - a: number
  - b: number
  - default: number
RETURNS: a / b

[clamp]
PURPOSE: Clamp a value between minimum and maximum.
INPUTS:
  - value: number
  - minimum: number
  - maximum: number
RETURNS: max(minimum, min(maximum, value))

[pluralize]
PURPOSE: Return singular or plural form based on count.
INPUTS:
  - word: string
  - count: number
RETURNS: word + 's'
