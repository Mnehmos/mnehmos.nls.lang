"""Property-based tests for resolver dependency ordering."""

from hypothesis import given, strategies as st

from nlsc.schema import ANLU, Module, NLFile
from nlsc.resolver import resolve_dependencies


def _make_nl_file(anlus: list[ANLU]) -> NLFile:
    return NLFile(module=Module(name="prop", target="python"), anlus=anlus)


def _build_dag_from_edges(size: int, edges: list[tuple[int, int]]) -> NLFile:
    """Create an NLFile where node i can only depend on nodes < i."""
    deps_by_node: dict[int, list[str]] = {i: [] for i in range(size)}
    for dep, node in edges:
        dep_name = f"n{dep}"
        token = f"[{dep_name}]"
        if token not in deps_by_node[node]:
            deps_by_node[node].append(token)

    anlus = [
        ANLU(
            identifier=f"n{i}",
            purpose=f"node {i}",
            returns="void",
            depends=deps_by_node[i],
        )
        for i in range(size)
    ]
    return _make_nl_file(anlus)


@given(
    size=st.integers(min_value=1, max_value=12),
    edges=st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=11),
            st.integers(min_value=0, max_value=11),
        ),
        max_size=60,
    ),
)
def test_resolver_orders_random_dag(size: int, edges: list[tuple[int, int]]) -> None:
    """Resolver should succeed and preserve dependency ordering for any DAG."""
    # Keep only edges within graph bounds and acyclic direction dep < node.
    filtered = [(dep, node) for dep, node in edges if dep < node < size]
    nl_file = _build_dag_from_edges(size, filtered)

    result = resolve_dependencies(nl_file)
    assert result.success is True

    order = [a.identifier for a in result.order]
    assert len(order) == size
    positions = {name: i for i, name in enumerate(order)}

    for anlu in nl_file.anlus:
        for dep in anlu.depends:
            dep_name = dep.strip("[]")
            assert positions[dep_name] < positions[anlu.identifier]


@given(size=st.integers(min_value=1, max_value=12))
def test_resolver_accepts_self_dependency(size: int) -> None:
    """Self-dependency is treated as recursion and should not fail resolution."""
    anlus = []
    for i in range(size):
        deps = []
        if i == 0:
            deps = [f"[n{i}]"]  # explicit recursion on first node
        elif i > 0:
            deps = [f"[n{i-1}]"]
        anlus.append(
            ANLU(identifier=f"n{i}", purpose=f"node {i}", returns="void", depends=deps)
        )

    result = resolve_dependencies(_make_nl_file(anlus))
    assert result.success is True
    assert len(result.order) == size


@given(name=st.text(min_size=1, max_size=8, alphabet=st.characters(min_codepoint=97, max_codepoint=122)))
def test_resolver_reports_missing_dependency(name: str) -> None:
    """Any unknown dependency identifier should produce a missing-dependency error."""
    missing = f"{name}_missing"
    nl_file = _make_nl_file(
        [
            ANLU(
                identifier="entry",
                purpose="entry",
                returns="void",
                depends=[f"[{missing}]"],
            )
        ]
    )

    result = resolve_dependencies(nl_file)
    assert result.success is False
    assert any(err.missing_dep == missing for err in result.errors)
