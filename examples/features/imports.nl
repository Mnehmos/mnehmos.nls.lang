# Feature: @imports - calling host-language modules
# Module names brought in via @imports are usable as explicit unknowns;
# declaring the import is what makes the call checked.

@module ex_imports
@version 1.0.0
@target python
@imports math

[hypotenuse]
PURPOSE: Length of the hypotenuse
INPUTS:
  - a: number
  - b: number
RETURNS: math.sqrt(a * a + b * b)

@main {
  PRINT hypotenuse(3, 4)
}

@test [hypotenuse] {
  hypotenuse(3, 4) == 5
}
