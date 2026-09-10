# Feature: string handling
# Method calls lower structurally; NLS truthiness treats "" as falsy.

@module ex_text
@version 1.0.0
@target python

[normalize]
PURPOSE: Trim and uppercase a label
INPUTS:
  - text: string
RETURNS: text.strip().upper()

[is-blank]
PURPOSE: Is the text empty or whitespace only?
INPUTS:
  - text: string
RETURNS: len(text.strip()) == 0

@main {
  PRINT normalize("  ada  ")
  PRINT is-blank("   ")
}

@test [normalize] {
  normalize("  ada  ") == "ADA"
}

@test [is-blank] {
  is_blank("   ") == True
  is_blank("x") == False
}
