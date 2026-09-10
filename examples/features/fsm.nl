# Feature: FSM state markers on LOGIC steps
# [state-name] prefixes label steps for state diagrams (nlsc graph) while
# remaining ordinary executable logic.

@module ex_fsm
@version 1.0.0
@target python

[order-flow]
PURPOSE: Walk an order through draft, confirmed, and shipped states
INPUTS:
  - total: number
GUARDS:
  - total > 0 -> ValueError("order needs a positive total")
LOGIC:
  1. [draft] draft_total = total
  2. [confirmed] confirmed_total = draft_total * 1.08
  3. [shipped] shipped_total = confirmed_total
RETURNS: shipped_total

@main {
  PRINT order-flow(100)
}

@test [order-flow] {
  order_flow(100) == 108
}
