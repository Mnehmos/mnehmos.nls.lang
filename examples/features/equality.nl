# Feature: structural equality
# Lists and records compare by value on every target (like Python), not by
# reference (unlike raw JavaScript).

@module ex_equality
@version 1.0.0
@target python

@type Point {
  x: number
  y: number
}

[same-shape]
PURPOSE: Do two points describe the same location?
INPUTS:
  - a: Point
  - b: Point
RETURNS: a == b

[same-items]
PURPOSE: Do two lists hold equal contents?
INPUTS:
  - left: list of number
  - right: list of number
RETURNS: left == right

@main {
  PRINT same-shape(Point(x = 1, y = 2), Point(x = 1, y = 2))
  PRINT same-items([1, 2], [1, 2])
}

@test [same-shape] {
  same_shape(Point(x = 1, y = 2), Point(x = 1, y = 2)) == True
  same_shape(Point(x = 1, y = 2), Point(x = 3, y = 2)) == False
}

@test [same-items] {
  same_items([1, 2], [1, 2]) == True
  same_items([1, 2], [2, 1]) == False
}
