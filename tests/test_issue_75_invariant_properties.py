"""Issue #75: property-based coverage for type invariants.

Hypothesis generates values; construction of the generated module must
be accepted exactly when the declared constraints and invariants hold.
This turns "invariants are enforced" from an example-based claim into a
property over the value domain.
"""

from __future__ import annotations

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from nlsc.parser import parse_nl_file
from nlsc.emitter import emit_python


def _construct(source: str) -> tuple[type, str]:
    """Compile a module and return (type, error message) for calling."""
    code = emit_python(parse_nl_file(source))
    namespace: dict = {}
    exec(code, namespace)  # noqa: S102 - test harness executes generated code
    type_name = source.split("@type ", 1)[1].split(" ", 1)[0].split("{", 1)[0].strip()
    return namespace[type_name]


@settings(max_examples=40, suppress_health_check=[HealthCheck.too_slow])
@given(value=st.integers(min_value=-50, max_value=50), bound=st.integers(min_value=-20, max_value=20))
def test_min_constraint_acceptance_matches_predicate(value, bound):
    a_type = _construct(
        f"""@module m
@version 1.0.0
@type Amount {{
  value: number, min: {bound}
}}
"""
    )
    if value >= bound:
        assert a_type(value=value).value == value
    else:
        try:
            a_type(value=value)
            raise AssertionError("value below min was accepted")
        except ValueError:
            pass


@settings(max_examples=40, suppress_health_check=[HealthCheck.too_slow])
@given(value=st.integers(min_value=-50, max_value=50), bound=st.integers(min_value=-20, max_value=20))
def test_max_constraint_acceptance_matches_predicate(value, bound):
    a_type = _construct(
        f"""@module m
@version 1.0.0
@type Amount {{
  value: number, max: {bound}
}}
"""
    )
    if value <= bound:
        assert a_type(value=value).value == value
    else:
        try:
            a_type(value=value)
            raise AssertionError("value above max was accepted")
        except ValueError:
            pass


@settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
@given(value=st.integers(min_value=-30, max_value=30))
def test_positive_and_non_negative_predicates(value):
    positive = _construct(
        """@module m
@version 1.0.0
@type P {
  n: number, positive
}
"""
    )
    non_negative = _construct(
        """@module m
@version 1.0.0
@type N {
  n: number, non-negative
}
"""
    )
    if value > 0:
        assert positive(n=value).n == value
    else:
        try:
            positive(n=value)
            raise AssertionError("non-positive accepted by 'positive'")
        except ValueError:
            pass
    if value >= 0:
        assert non_negative(n=value).n == value
    else:
        try:
            non_negative(n=value)
            raise AssertionError("negative accepted by 'non-negative'")
        except ValueError:
            pass


@settings(max_examples=40, suppress_health_check=[HealthCheck.too_slow])
@given(
    low=st.integers(min_value=-20, max_value=20),
    high=st.integers(min_value=-20, max_value=20),
)
def test_invariant_over_two_fields_matches_predicate(low, high):
    range_type = _construct(
        """@module m
@version 1.0.0
@type Range {
  low: number
  high: number
}

@invariant Range {
  low <= high
}
"""
    )
    if low <= high:
        instance = range_type(low=low, high=high)
        assert (instance.low, instance.high) == (low, high)
    else:
        try:
            range_type(low=low, high=high)
            raise AssertionError("inverted range accepted")
        except ValueError as exc:
            assert "Invariant violated" in str(exc)


@settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
@given(
    quantity=st.integers(min_value=-5, max_value=15),
    price=st.integers(min_value=-5, max_value=15),
)
def test_multiple_field_predicates_combine(quantity, price):
    item_type = _construct(
        """@module m
@version 1.0.0
@type LineItem {
  quantity: number, min: 1
  price: number, min: 0
}
"""
    )
    should_accept = quantity >= 1 and price >= 0
    if should_accept:
        instance = item_type(quantity=quantity, price=price)
        assert (instance.quantity, instance.price) == (quantity, price)
    else:
        try:
            item_type(quantity=quantity, price=price)
            raise AssertionError(f"accepted invalid combination {quantity}, {price}")
        except ValueError:
            pass
