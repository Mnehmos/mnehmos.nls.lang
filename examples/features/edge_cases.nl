# Feature: EDGE CASES - early exits before the main logic
# Python-evaluable edge cases become early returns; they run before LOGIC.

@module ex_edge_cases
@version 1.0.0
@target python

[safe-divide]
PURPOSE: Divide with explicit boundary handling
INPUTS:
  - numerator: number
  - divisor: number
EDGE CASES:
  - divisor == 0 -> return 0
LOGIC:
  1. quotient = numerator / divisor
RETURNS: quotient

[clamp]
PURPOSE: Clamp a value into a range
INPUTS:
  - value: number
  - low: number
  - high: number
EDGE CASES:
  - value < low -> return low
  - value > high -> return high
LOGIC:
  1. bounded = value
RETURNS: bounded

@main {
  PRINT safe-divide(7, 0)
  PRINT clamp(150, 0, 100)
}

@test [safe-divide] {
  safe_divide(7, 0) == 0
  safe_divide(8, 2) == 4
}

@test [clamp] {
  clamp(150, 0, 100) == 100
  clamp(-5, 0, 100) == 0
  clamp(50, 0, 100) == 50
}
