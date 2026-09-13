# NLS Examples

This directory contains working examples of `.nl` files demonstrating various NLS features.

## Quick Start

```bash
# Compile any example
nlsc compile arithmetic.nl

# Or compile the same example to TypeScript
nlsc compile arithmetic.nl -t typescript

# Run tests
nlsc test shop_demo.nl

# Visualize dependencies
nlsc graph billing.nl
```

## Complete examples vs. drafts

Only some files here are complete specifications. The rest still have prose
LOGIC steps or use constructs outside the checked core, which makes them
**scaffolds**: `nlsc compile` writes them to `<name>.draft.py` and `nlsc run`
and `nlsc test` refuse to execute them (`ESCAF001`), because their unresolved
steps compile to `None` placeholders rather than to the logic described.

| Example | Status |
| --- | --- |
| `showcase/mission_control.nl` | Complete — passes `--strict` |
| `arithmetic.nl` | Complete — passes `--strict` |
| `shop_demo.nl` | Complete — passes `--strict` |
| `billing.nl` | Complete — passes `--strict` |
| `strings.nl` | Complete — passes `--strict` |
| `sorting.nl`, `sorting_ja.nl`, `sorting_ts.nl` | Complete — passes `--strict` |
| `workflow_engine.nl` | Draft — largely prose LOGIC |

Bringing the corpus to strict-clean is tracked in
[#264](https://github.com/Mnehmos/mnehmos.nls.lang/issues/264).

## Examples

### showcase/mission_control.nl - Aster Mission Control
An interactive rover expedition planner with a local browser interface. Select
survey sites, balance energy and sample capacity, and launch a simulated round
trip. The domain logic is compiled from 19 NLS operations with typed records,
invariants, launch guards, recursive routes, and embedded examples and properties.

```bash
python -m nlsc run examples/showcase/mission_control.nl --strict
# Open http://127.0.0.1:8765
```

See the [showcase guide](showcase/README.md) for a walkthrough and verification.

### arithmetic.nl - Basic Arithmetic
The simplest possible example. Two functions: `add` and `multiply`.

**Features demonstrated:**
- Basic ANLU structure
- Simple inputs and returns
- Test blocks

### sorting_ts.nl - TypeScript Quicksort
The quicksort example compiled to the TypeScript target.

**Features demonstrated:**
- `@target typescript`
- Deterministic LOGIC emission to TypeScript
- Generated Node assert tests

### strings.nl - String Operations
Text manipulation utilities.

**Features demonstrated:**
- String type handling
- Multiple functions

### shop_demo.nl - E-commerce Basics
Division and discount calculations with guard clauses.

**Features demonstrated:**
- Guard clauses with error messages
- `@test` blocks with multiple assertions
- Input validation

### billing.nl - Invoice Processing
Comprehensive billing system with types, invariants, and property tests.

**Features demonstrated:**
- Custom `@type` definitions
- Type constraints (`min:`, `required`)
- `@invariant` blocks for type validation
- Multi-step `LOGIC` sections
- `DEPENDS` declarations
- `@property` blocks for property-based testing
- Complex function composition

## Running Examples

```bash
# Compile to Python
nlsc compile billing.nl

# Compile to TypeScript
nlsc compile billing.nl -t typescript

# Verify syntax without generating
nlsc verify billing.nl

# Run @test blocks
nlsc test billing.nl

# Generate dependency graph
nlsc graph billing.nl -f mermaid
nlsc graph billing.nl -f ascii

# Watch for changes
nlsc watch .
```

## Example: Billing Module

```nl
@type LineItem {
  description: string, required
  quantity: number, min: 1
  unit_price: number, min: 0
}

[calculate-line-total]
PURPOSE: Calculate the total for a single line item.
INPUTS:
  - item: LineItem
RETURNS: item.quantity * item.unit_price

@test [calculate-line-total] {
  calculate_line_total(LineItem(...)) == 50
}
```

Compiles to:

```python
@dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float

    def __post_init__(self):
        if self.quantity < 1:
            raise ValueError('quantity must be at least 1')
        if self.unit_price < 0:
            raise ValueError('unit_price must be at least 0')

def calculate_line_total(item: LineItem) -> float:
    """Calculate the total for a single line item."""
    return item.quantity * item.unit_price
```

## Adding New Examples

1. Create a new `.nl` file in this directory
2. Run `nlsc compile <file>.nl` to generate Python
3. Run `nlsc test <file>.nl` to verify tests pass
4. Commit both the `.nl` and generated `.py` files
