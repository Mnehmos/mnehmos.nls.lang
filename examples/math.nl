# Math Module
# Example from PRD Appendix B

@module math
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  • a: number
  • b: number
RETURNS: a + b

[multiply]
PURPOSE: Multiply two numbers
INPUTS:
  • a: number
  • b: number
RETURNS: a × b

@test [add] {
  add(2, 3) == 5
  add(-1, 1) == 0
  add(0, 0) == 0
}
