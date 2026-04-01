@module sorting
@target python

[quick-sort]
PURPOSE: Sort a list of numbers using the quicksort algorithm
INPUTS:
  - items: list of number
EDGE CASES:
  - len(items) < 2 -> return items
LOGIC:
  1. items[0] -> pivot
  2. [x for x in items if x < pivot] -> lesser
  3. [x for x in items if x == pivot] -> equal
  4. [x for x in items if x > pivot] -> greater
  5. [quick-sort](lesser) -> sorted_lesser
  6. [quick-sort](greater) -> sorted_greater
RETURNS: sorted_lesser + equal + sorted_greater

@test [quick-sort] {
  quick_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]
  quick_sort([]) == []
  quick_sort([1]) == [1]
  quick_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
}
