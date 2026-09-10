# Feature: IF / THEN / ELSE - total branches and nested joins
# Both arms bind the joined name, so every path defines it. A one-armed
# branch that binds a value would be rejected with ESEM010.

@module ex_branches
@version 1.0.0
@target python

[grade]
PURPOSE: Letter grade for a passing-or-distinction score
INPUTS:
  - score: number
GUARDS:
  - score >= 0 -> ValueError("score cannot be negative")
LOGIC:
  1. IF score >= 90 THEN "A" -> letter ELSE "B" -> letter
RETURNS: letter

[pass-fail]
PURPOSE: Pass or fail on every path
INPUTS:
  - score: number
LOGIC:
  1. IF score >= 50 THEN "pass" -> band ELSE "fail" -> band
RETURNS: band

[bucket]
PURPOSE: Nested joins across two booleans
INPUTS:
  - high: boolean
  - fast: boolean
LOGIC:
  1. IF high THEN 2 -> weight ELSE 1 -> weight
  2. IF fast THEN weight + 10 -> total ELSE weight - 1 -> total
RETURNS: total

@main {
  PRINT grade(95)
  PRINT bucket(True, True)
}

@test [grade] {
  grade(95) == "A"
  grade(80) == "B"
}

@test [pass-fail] {
  pass_fail(80) == "pass"
  pass_fail(10) == "fail"
}

@test [bucket] {
  bucket(True, True) == 12
  bucket(False, False) == 0
}
