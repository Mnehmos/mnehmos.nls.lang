"""
Semantic tests for NLS Core Semantics (Issue #88).

This package contains tests that validate semantic BEHAVIOR rather than
syntax output. These tests are target-agnostic and verify the 5 semantic
invariants documented in docs/core-semantics.md:

1. Guard Ordering - Guards evaluated in specification order
2. Logic Step Dataflow - Variables flow correctly between steps
3. Type Constraints - Enforced at construction time
4. Test Isolation - Each test case is independent
5. Property Semantics - Properties hold for all valid inputs
"""
