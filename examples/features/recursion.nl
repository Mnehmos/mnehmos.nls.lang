# Feature: self-recursion
# Recursive operations need no self-entry in DEPENDS; totality comes from
# the ELSE arm so the result is defined on every path.

@module ex_recursion
@version 1.0.0
@target python

[factorial]
PURPOSE: Factorial via self-recursion
INPUTS:
  - n: number
GUARDS:
  - n >= 0 -> ValueError("n must be non-negative")
LOGIC:
  1. IF n <= 1 THEN 1 -> result ELSE n * [factorial](n - 1) -> result
RETURNS: result

[sum-to]
PURPOSE: Triangular sum via self-recursion
INPUTS:
  - n: number
LOGIC:
  1. IF n <= 0 THEN 0 -> total ELSE n + [sum-to](n - 1) -> total
RETURNS: total

@main {
  PRINT factorial(5)
  PRINT sum-to(4)
}

@test [factorial] {
  factorial(0) == 1
  factorial(5) == 120
}

@test [sum-to] {
  sum_to(0) == 0
  sum_to(4) == 10
}
