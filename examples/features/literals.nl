# Feature: @literal python - the sanctioned escape hatch
# The literal body is emitted verbatim, still participates in the lockfile
# hash, and contributes an explicit unknown effect/failure marker. The
# checker registers literal-defined functions as declared escapes.

@module ex_literals
@version 1.0.0
@target python

@literal python {
def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    cleaned = "".join(c if c.isalnum() else "-" for c in text.lower().strip())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-")
}

[slug-and-check]
PURPOSE: Use the literal implementation from ordinary NLS logic
INPUTS:
  - text: string
LOGIC:
  1. slug = slugify(text)
  2. IF len(slug) > 0 THEN slug -> result ELSE "empty" -> result
RETURNS: result

@main {
  PRINT slug-and-check("Hello World")
}

@test [slug-and-check] {
  slug_and_check("Hello World") == "hello-world"
  slug_and_check("...") == "empty"
}
