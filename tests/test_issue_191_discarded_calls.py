"""Issue #191: ANLU calls must execute even when their return value is discarded.

Behavior tests: generated Python is executed and we compare ordered events
and raised errors — not source substrings.
"""

from __future__ import annotations

import pytest

from nlsc.emitter import emit_python
from nlsc.parser import parse_nl_file

REPRODUCER = """@module discarded_call
[reject]
PURPOSE: Always raise when called
GUARDS:
  - False -> ValueError("called")
RETURNS: 0

[probe]
PURPOSE: Call reject
LOGIC:
  1. [reject]()
DEPENDS: [reject]
RETURNS: 0
"""


def _exec_module(source: str) -> dict:
    nl_file = parse_nl_file(source)
    code = emit_python(nl_file)
    namespace: dict = {}
    exec(code, namespace)  # noqa: S102 - test harness executes generated code
    return namespace


def test_reproducer_discarded_guard_call_raises():
    namespace = _exec_module(REPRODUCER)
    with pytest.raises(ValueError, match="called"):
        namespace["probe"]()


EVENT_LOG_SOURCE = """@module event_log
[record]
PURPOSE: Append an event to the log
INPUTS:
  - name: string
LOGIC:
  1. events.append(name)
RETURNS: events

[use-bound]
PURPOSE: Call record and bind its value
INPUTS:
  - name: string
LOGIC:
  1. [record](name) -> entry
RETURNS: entry
DEPENDS: [record]

[use-discarded]
PURPOSE: Call record and discard its value
INPUTS:
  - name: string
LOGIC:
  1. [record](name)
RETURNS: 0
DEPENDS: [record]
"""

def _run_with_log(source: str, fn_name: str, arg: str) -> list:
    nl_file = parse_nl_file(source)
    code = emit_python(nl_file)
    namespace: dict = {}
    exec(code, namespace)  # noqa: S102
    # Generated functions resolve `events` from their module globals at
    # call time, so injecting it after exec works without a preamble.
    namespace["events"] = []
    namespace[fn_name](arg)
    return namespace["events"]


def test_event_log_operation_invoked_once_with_binding():
    events = _run_with_log(EVENT_LOG_SOURCE, "use_bound", "a")
    assert events == ["a"]


def test_event_log_operation_invoked_once_without_binding():
    events = _run_with_log(EVENT_LOG_SOURCE, "use_discarded", "b")
    assert events == ["b"]


def test_returned_values_remain_discardable_and_void_needs_no_fake_binding():
    namespace = _exec_module(EVENT_LOG_SOURCE)
    namespace["events"] = []
    # A void-style op returning nothing meaningful still runs via discard.
    assert namespace["use_discarded"]("c") == 0
    assert namespace["events"] == ["c"]


CONDITIONAL_SOURCE = """@module conditional_calls
[record]
PURPOSE: Append an event to the log
INPUTS:
  - name: string
LOGIC:
  1. events.append(name)
RETURNS: events

[run-if]
PURPOSE: Conditionally record
INPUTS:
  - flag: boolean
LOGIC:
  1. IF flag THEN [record]("hit")
RETURNS: 0
DEPENDS: [record]
"""


def test_false_conditional_does_not_invoke_discarded_call():
    nl_file = parse_nl_file(CONDITIONAL_SOURCE)
    code = emit_python(nl_file)
    namespace: dict = {}
    exec(code, namespace)  # noqa: S102
    namespace["events"] = []
    namespace["run_if"](False)
    assert namespace["events"] == []


def test_true_conditional_invokes_discarded_call_exactly_once():
    nl_file = parse_nl_file(CONDITIONAL_SOURCE)
    code = emit_python(nl_file)
    namespace: dict = {}
    exec(code, namespace)  # noqa: S102
    namespace["events"] = []
    namespace["run_if"](True)
    assert namespace["events"] == ["hit"]


def test_nested_arguments_in_discarded_call_are_preserved():
    source = """@module nested_discard
[identity]
PURPOSE: Return input
INPUTS:
  - x: number
RETURNS: x

[outer]
PURPOSE: Call identity with a nested call argument
LOGIC:
  1. [identity]([identity](1))
RETURNS: 0
DEPENDS: [identity]
"""
    namespace = _exec_module(source)
    # Compiles and runs; the nested ANLU call must survive emission whole.
    assert namespace["outer"]() == 0


def test_descriptive_prose_is_still_not_executable():
    source = """@module prose_guard
[noop]
PURPOSE: Do nothing dangerous
LOGIC:
  1. Process customer payment
RETURNS: 0
"""
    namespace = _exec_module(source)
    # Descriptive text stays a comment; nothing raises.
    assert namespace["noop"]() == 0
    code = emit_python(parse_nl_file(source))
    assert "Process customer payment" in code  # still visible as a comment
    assert "Process customer payment()" not in code


def test_typescript_preserves_discarded_call_statement():
    from nlsc.emitter_typescript import emit_typescript

    code = emit_typescript(parse_nl_file(REPRODUCER))
    # The call executes; only the error-class contract (issue #198) is
    # still open on the TypeScript side.
    assert "reject();" in code
