# Feature: @property - property-based test specifications

@module ex_properties
@version 1.0.0
@target python

[add]
PURPOSE: Add two numbers
INPUTS:
  - a: number
  - b: number
RETURNS: a + b

@main {
  PRINT add(2, 3)
}

@test [add] {
  add(1, 2) == 3
  add(-1, 1) == 0
}

@property [add] {
  add(a, b) == add(b, a)
  add(a, 0) == a
}
