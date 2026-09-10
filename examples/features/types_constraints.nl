# Feature: @type constraints and @invariant
# Constraints (min/max/positive/non-negative/required) and invariants are
# enforced at construction on every target; violations raise ValueError.

@module ex_types
@version 1.0.0
@target python

@type Account {
  owner: string, required
  balance: number, non-negative
  overdraft_limit: number, min: 0
}

@invariant Account {
  balance + overdraft_limit >= 0
}

[deposit]
PURPOSE: Add funds, returning the updated account
INPUTS:
  - account: Account
  - amount: number
GUARDS:
  - amount > 0 -> ValueError("deposit must be positive")
LOGIC:
  1. new_balance = account.balance + amount
RETURNS: Account(owner = account.owner, balance = new_balance, overdraft_limit = account.overdraft_limit)

[open]
PURPOSE: Open an account with a starting balance
INPUTS:
  - owner: string
  - initial: number, min: 0
RETURNS: Account(owner = owner, balance = initial, overdraft_limit = 100)

@main {
  PRINT open("ada", 50).balance
}

@test [open] {
  open("ada", 50).balance == 50
}
