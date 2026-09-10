# Feature: optional inputs
# Inputs marked optional may be omitted at call sites; callers are checked
# against the declared arity window.

@module ex_optionals
@version 1.0.0
@target python

[greet]
PURPOSE: Greeting with an optional honorific
INPUTS:
  - name: string
  - title: string, optional
LOGIC:
  1. IF title is not None THEN title + " " + name -> full ELSE name -> full
RETURNS: full

[paginate]
PURPOSE: Page size with an optional cap
INPUTS:
  - total: number
  - page_size: number, optional
LOGIC:
  1. IF page_size is not None THEN page_size -> size ELSE 25 -> size
  2. pages = total / size
RETURNS: pages

@main {
  PRINT greet("Ada")
  PRINT paginate(100)
}

@test [greet] {
  greet("Ada") == "Ada"
  greet("Ada", "Dr.") == "Dr. Ada"
}

@test [paginate] {
  paginate(100) == 4
  paginate(100, 10) == 10
}
