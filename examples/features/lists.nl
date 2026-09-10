# Feature: list construction and collection builtins
# len / sum / max / min and indexing lower structurally.

@module ex_lists
@version 1.0.0
@target python

@type Basket {
  prices: list of number
}

[stats]
PURPOSE: Count, total, and largest price as a list
INPUTS:
  - prices: list of number
LOGIC:
  1. count = len(prices)
  2. total = sum(prices)
  3. largest = max(prices)
RETURNS: [count, total, largest]

[first-price]
PURPOSE: First price, or 0 when empty
INPUTS:
  - prices: list of number
LOGIC:
  1. IF len(prices) > 0 THEN prices[0] -> head ELSE 0 -> head
RETURNS: head

@main {
  PRINT stats([10, 25, 5])
  PRINT first-price([])
}

@test [stats] {
  stats([10, 25, 5]) == [3, 40, 25]
}

@test [first-price] {
  first_price([10, 25]) == 10
  first_price([]) == 0
}
