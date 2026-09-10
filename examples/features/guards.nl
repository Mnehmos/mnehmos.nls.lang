# Feature: GUARDS — typed, ordered failure contracts
# The first failing guard wins; error identity, code, and message are
# preserved on every target (see tests/semantic/test_guard_ordering.py).

@module ex_guards
@version 1.0.0
@target python

@type InsufficientFunds {
  message: string
}

[withdraw]
PURPOSE: Withdraw from an account balance with full validation
INPUTS:
  - balance: number
  - amount: number
GUARDS:
  - amount > 0 -> ValueError("amount must be positive")
  - amount <= balance -> InsufficientFunds(OVERDRAW, "amount exceeds balance")
RETURNS: balance - amount

@main {
  PRINT withdraw(100, 30)
}

@test [withdraw] {
  withdraw(100, 30) == 70
}
