"""Issue #146: package model — manifest, resolution, and package lock.

Slice 1: local path dependencies with semver constraints, resolution
into ``@use`` search roots, and an offline content-hashed project lock.
"""

from __future__ import annotations

import json

import pytest

from nlsc.pkg import (
    MANIFEST_NAME,
    PackageError,
    load_manifest,
    matching_package_root,
    package_content_hash,
    package_search_roots,
    read_package_lock,
    resolve_dependencies,
    verify_package_lock,
    version_satisfies,
    write_package_lock,
)


def _write_manifest(project_dir, dependencies: dict, *, name="acme.project", version="1.0.0"):
    manifest = {
        "schema": "nls.pkg/1",
        "name": name,
        "version": version,
        "dependencies": dependencies,
    }
    path = project_dir / MANIFEST_NAME
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


def _make_package(root, *, version="1.2.0", domains=("charge",)):
    root.mkdir(parents=True, exist_ok=True)
    (root / MANIFEST_NAME).write_text(
        json.dumps({"schema": "nls.pkg/1", "name": root.name, "version": version}),
        encoding="utf-8",
    )
    for domain in domains:
        target = root / "v1" / f"{domain}.nl"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            f"@module {domain}\n[{domain}]\nPURPOSE: {domain}\nRETURNS: 1\n",
            encoding="utf-8",
        )
    return root


# --------------------------------------------------------------------------
# Version constraints
# --------------------------------------------------------------------------


def test_version_satisfies_ranges():
    assert version_satisfies("1.2.3", "*")
    assert version_satisfies("1.2.3", "1.2.3")
    assert not version_satisfies("1.2.4", "1.2.3")
    assert version_satisfies("1.9.0", "^1.2.0")
    assert not version_satisfies("2.0.0", "^1.2.0")
    assert version_satisfies("0.2.5", "^0.2.0")
    assert not version_satisfies("0.3.0", "^0.2.0")
    assert version_satisfies("1.2.9", "~1.2.0")
    assert not version_satisfies("1.3.0", "~1.2.0")
    assert not version_satisfies("not-a-version", "*")


# --------------------------------------------------------------------------
# Manifest loading
# --------------------------------------------------------------------------


def test_manifest_round_trip(tmp_path):
    _write_manifest(tmp_path, {"acme.payments": {"path": "../payments", "version": "^1.0.0"}})
    manifest = load_manifest(tmp_path)
    assert manifest.name == "acme.project"
    assert manifest.dependencies["acme.payments"].path == "../payments"
    assert manifest.dependencies["acme.payments"].version == "^1.0.0"


def test_missing_manifest_is_epkg001(tmp_path):
    with pytest.raises(PackageError) as excinfo:
        load_manifest(tmp_path)
    assert excinfo.value.code == "EPKG001"


def test_malformed_manifest_is_epkg001(tmp_path):
    (tmp_path / MANIFEST_NAME).write_text("{not json", encoding="utf-8")
    with pytest.raises(PackageError) as excinfo:
        load_manifest(tmp_path)
    assert excinfo.value.code == "EPKG001"


def test_dependency_without_path_is_epkg001(tmp_path):
    _write_manifest(tmp_path, {"acme.payments": {"version": "^1.0.0"}})
    with pytest.raises(PackageError) as excinfo:
        load_manifest(tmp_path)
    assert excinfo.value.code == "EPKG001"


def test_invalid_constraint_string_is_epkg001(tmp_path):
    _write_manifest(tmp_path, {"acme.payments": {"path": "../p", "version": 5}})
    with pytest.raises(PackageError) as excinfo:
        load_manifest(tmp_path)
    assert excinfo.value.code == "EPKG001"


# --------------------------------------------------------------------------
# Resolution
# --------------------------------------------------------------------------


def test_resolve_dependencies_records_version_and_hash(tmp_path):
    _make_package(tmp_path / "vendor" / "payments", version="1.4.0")
    _write_manifest(
        tmp_path, {"acme.payments": {"path": "vendor/payments", "version": "^1.0.0"}}
    )
    resolved = resolve_dependencies(tmp_path, load_manifest(tmp_path))
    assert [package.name for package in resolved] == ["acme.payments"]
    assert resolved[0].version == "1.4.0"
    assert resolved[0].content_hash.startswith("sha256:")
    assert resolved[0].root == (tmp_path / "vendor" / "payments").resolve()


def test_missing_dependency_path_is_epkg002(tmp_path):
    _write_manifest(tmp_path, {"acme.payments": {"path": "vendor/missing"}})
    with pytest.raises(PackageError) as excinfo:
        resolve_dependencies(tmp_path, load_manifest(tmp_path))
    assert excinfo.value.code == "EPKG002"


def test_unsatisfied_version_is_epkg003(tmp_path):
    _make_package(tmp_path / "vendor" / "payments", version="2.0.0")
    _write_manifest(
        tmp_path, {"acme.payments": {"path": "vendor/payments", "version": "^1.0.0"}}
    )
    with pytest.raises(PackageError) as excinfo:
        resolve_dependencies(tmp_path, load_manifest(tmp_path))
    assert excinfo.value.code == "EPKG003"


def test_content_hash_tracks_file_changes(tmp_path):
    package = _make_package(tmp_path / "pkg")
    before = package_content_hash(package)
    (package / "v1" / "charge.nl").write_text("changed\n", encoding="utf-8")
    assert package_content_hash(package) != before


# --------------------------------------------------------------------------
# @use search roots
# --------------------------------------------------------------------------


def test_package_search_roots_are_opt_in(tmp_path):
    assert package_search_roots(tmp_path) == []


def test_matching_package_root_longest_prefix(tmp_path):
    roots = [("acme", tmp_path / "a"), ("acme.payments", tmp_path / "b")]
    match = matching_package_root("acme.payments.charge", roots)
    assert match is not None
    name, root, remainder = match
    assert name == "acme.payments"
    assert root == tmp_path / "b"
    assert remainder == "charge"
    assert matching_package_root("other.domain", roots) is None


def test_package_search_roots_from_manifest(tmp_path):
    _make_package(tmp_path / "vendor" / "payments")
    _write_manifest(tmp_path, {"acme.payments": {"path": "vendor/payments"}})
    roots = package_search_roots(tmp_path)
    assert roots == [("acme.payments", (tmp_path / "vendor" / "payments").resolve())]


# --------------------------------------------------------------------------
# Package lock
# --------------------------------------------------------------------------


def test_lock_round_trip_and_verify(tmp_path):
    _make_package(tmp_path / "vendor" / "payments", version="1.2.0")
    _write_manifest(tmp_path, {"acme.payments": {"path": "vendor/payments"}})
    manifest = load_manifest(tmp_path)
    resolved = resolve_dependencies(tmp_path, manifest)

    lock_path = tmp_path / "nls.pkg.lock"
    write_package_lock(lock_path, manifest, resolved)
    recorded = read_package_lock(lock_path)
    assert recorded["acme.payments"]["version"] == "1.2.0"
    assert recorded["acme.payments"]["hash"] == resolved[0].content_hash
    assert verify_package_lock(lock_path, tmp_path, manifest) == []


def test_verify_reports_content_drift(tmp_path):
    _make_package(tmp_path / "vendor" / "payments", version="1.2.0")
    _write_manifest(tmp_path, {"acme.payments": {"path": "vendor/payments"}})
    manifest = load_manifest(tmp_path)
    resolved = resolve_dependencies(tmp_path, manifest)
    lock_path = tmp_path / "nls.pkg.lock"
    write_package_lock(lock_path, manifest, resolved)

    (tmp_path / "vendor" / "payments" / "v1" / "charge.nl").write_text(
        "changed\n", encoding="utf-8"
    )
    errors = verify_package_lock(lock_path, tmp_path, manifest)
    assert any("content changed since lock" in error for error in errors)


def test_verify_reports_missing_and_extra_entries(tmp_path):
    _make_package(tmp_path / "vendor" / "payments")
    _write_manifest(tmp_path, {"acme.payments": {"path": "vendor/payments"}})
    manifest = load_manifest(tmp_path)
    resolved = resolve_dependencies(tmp_path, manifest)

    lock_path = tmp_path / "nls.pkg.lock"
    write_package_lock(lock_path, manifest, resolved)
    assert verify_package_lock(tmp_path / "absent.lock", tmp_path, manifest) != []


# --------------------------------------------------------------------------
# CLI: `nlsc install` and package-backed `@use`
# --------------------------------------------------------------------------

PACKAGE_DOMAIN = """@module charge
[charge-card]
PURPOSE: charge a card
INPUTS:
  - amount: number
LOGIC:
  1. receipt = amount
RETURNS: receipt
"""

APP_SOURCE = """@module app
@use acme.payments.charge

[run]
PURPOSE: run the app
INPUTS:
  - amount: number
LOGIC:
  1. receipt = amount
RETURNS: receipt
"""


def _project(tmp_path, *, version="1.2.0", constraint="^1.0.0"):
    package = tmp_path / "vendor" / "payments"
    _make_package(package, version=version)
    (package / "v1" / "charge.nl").write_text(PACKAGE_DOMAIN, encoding="utf-8")
    _write_manifest(
        tmp_path, {"acme.payments": {"path": "vendor/payments", "version": constraint}}
    )
    return tmp_path


def test_install_writes_lock_and_check_passes(tmp_path, capsys):
    from nlsc.cli import main

    project = _project(tmp_path)
    assert main(["install", str(project)]) == 0
    captured = capsys.readouterr()
    assert "Resolved 1 package dependencies" in captured.out
    lock_path = project / "nls.pkg.lock"
    assert lock_path.is_file()

    assert main(["install", str(project), "--check"]) == 0
    assert "Package lock is current" in capsys.readouterr().out


def test_install_check_detects_drift(tmp_path, capsys):
    from nlsc.cli import main

    project = _project(tmp_path)
    assert main(["install", str(project)]) == 0
    capsys.readouterr()
    (project / "vendor" / "payments" / "v1" / "charge.nl").write_text(
        "changed\n", encoding="utf-8"
    )
    assert main(["install", str(project), "--check"]) == 1
    captured = capsys.readouterr()
    assert "EPKG004" in captured.err


def test_install_reports_missing_manifest(tmp_path, capsys):
    from nlsc.cli import main

    assert main(["install", str(tmp_path)]) == 1
    assert "EPKG001" in capsys.readouterr().err


def test_install_json_payload(tmp_path, capsys):
    from nlsc.cli import main

    project = _project(tmp_path)
    assert main(["install", "--json", str(project)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["command"] == "install"
    assert payload["packages"] == ["acme.payments"]
    assert payload["lockfile"].endswith("nls.pkg.lock")


def test_install_rejects_unsatisfied_version(tmp_path, capsys):
    from nlsc.cli import main

    project = _project(tmp_path, version="2.0.0", constraint="^1.0.0")
    assert main(["install", str(project)]) == 1
    assert "EPKG003" in capsys.readouterr().err


def test_use_resolves_through_package_root(tmp_path, capsys):
    from nlsc.cli import main

    project = _project(tmp_path)
    app = project / "app.nl"
    app.write_text(APP_SOURCE, encoding="utf-8")
    assert main(["compile", str(app)]) == 0
    captured = capsys.readouterr()
    assert "@use acme.payments.charge" in captured.out
    assert "vendor" in captured.out


def test_use_without_package_still_reports_euse001(tmp_path, capsys):
    from nlsc.cli import main

    project = _project(tmp_path)
    app = project / "app.nl"
    app.write_text(
        APP_SOURCE.replace("acme.payments.charge", "acme.payments.missing"),
        encoding="utf-8",
    )
    assert main(["compile", str(app)]) == 1
    assert "EUSE001" in capsys.readouterr().err


# --------------------------------------------------------------------------
# Review follow-ups: robustness and edge cases
# --------------------------------------------------------------------------


def test_malformed_manifest_does_not_crash_compile(tmp_path, capsys):
    """A broken manifest surfaces as EPKG001 from install, never a traceback."""
    from nlsc.cli import main

    project = _project(tmp_path)
    (project / "nls.pkg.json").write_text("{not json", encoding="utf-8")
    app = project / "app.nl"
    app.write_text(APP_SOURCE, encoding="utf-8")

    # Compilation treats an unusable manifest as no packages (opt-in), and
    # the missing package domain then fails cleanly with EUSE001.
    assert main(["compile", str(app)]) == 1
    assert "EUSE001" in capsys.readouterr().err

    assert main(["install", str(project)]) == 1
    assert "EPKG001" in capsys.readouterr().err


def test_install_from_subdirectory_finds_project_root(tmp_path, capsys):
    from nlsc.cli import main

    project = _project(tmp_path)
    nested = project / "src" / "deep"
    nested.mkdir(parents=True)
    assert main(["install", str(nested)]) == 0
    captured = capsys.readouterr()
    assert "Resolved 1 package dependencies" in captured.out
    assert (project / "nls.pkg.lock").is_file()


def test_manifest_rejects_absolute_and_empty_paths(tmp_path):
    from nlsc.pkg import load_manifest

    for bad in ("", str(tmp_path / "elsewhere")):
        _write_manifest(tmp_path, {"acme.payments": {"path": bad}})
        with pytest.raises(PackageError) as excinfo:
            load_manifest(tmp_path)
        assert excinfo.value.code == "EPKG001"


def test_manifest_rejects_unsupported_constraint(tmp_path):
    from nlsc.pkg import load_manifest

    _write_manifest(tmp_path, {"acme.payments": {"path": "vendor/p", "version": ">=1.0"}})
    with pytest.raises(PackageError) as excinfo:
        load_manifest(tmp_path)
    assert excinfo.value.code == "EPKG001"


def test_prerelease_range_semantics():
    assert version_satisfies("0.0.3", "^0.0.3")
    assert not version_satisfies("0.0.4", "^0.0.3")


def test_lock_stores_relative_paths(tmp_path):
    _make_package(tmp_path / "vendor" / "payments")
    _write_manifest(tmp_path, {"acme.payments": {"path": "vendor/payments"}})
    manifest = load_manifest(tmp_path)
    resolved = resolve_dependencies(tmp_path, manifest)
    lock_path = tmp_path / "nls.pkg.lock"
    write_package_lock(lock_path, manifest, resolved)
    content = lock_path.read_text(encoding="utf-8")
    assert "path: vendor/payments" in content
    assert str(tmp_path) not in content


def test_content_hash_is_order_independent(tmp_path):
    first = tmp_path / "a"
    second = tmp_path / "b"
    for root in (first, second):
        (root / "v1").mkdir(parents=True)
        (root / "v1" / "x.nl").write_text("x\n", encoding="utf-8")
        (root / "v1" / "y.nl").write_text("y\n", encoding="utf-8")
    assert package_content_hash(first) == package_content_hash(second)


def test_lock_reports_extra_manifest_entries(tmp_path):
    _make_package(tmp_path / "vendor" / "payments")
    _write_manifest(tmp_path, {"acme.payments": {"path": "vendor/payments"}})
    manifest = load_manifest(tmp_path)
    resolved = resolve_dependencies(tmp_path, manifest)
    lock_path = tmp_path / "nls.pkg.lock"
    write_package_lock(lock_path, manifest, resolved)

    # A dependency disappears from the manifest but stays in the lock.
    empty_manifest = load_manifest.__globals__["PackageManifest"](
        name="acme.project", version="1.0.0", dependencies={}
    )
    errors = verify_package_lock(lock_path, tmp_path, empty_manifest)
    assert any("in lockfile but not in manifest" in error for error in errors)


def test_matching_package_root_exact_name_and_false_prefix(tmp_path):
    roots = [("acme", tmp_path / "a"), ("acme.payments", tmp_path / "b")]
    exact = matching_package_root("acme.payments", roots)
    assert exact is not None and exact[0] == "acme.payments" and exact[2] == ""
    # Longest prefix wins: "acme.paymentsx" is not the "acme.payments"
    # package, so it falls back to the "acme" namespace with remainder
    # "paymentsx"; a name that is not dot-prefixed by any package misses.
    partial = matching_package_root("acme.paymentsx", roots)
    assert partial is not None and partial[0] == "acme" and partial[2] == "paymentsx"
    assert matching_package_root("acmex.payments", roots) is None


def test_use_exact_package_name_is_rejected(tmp_path, capsys):
    from nlsc.cli import main

    project = _project(tmp_path)
    app = project / "app.nl"
    app.write_text(
        APP_SOURCE.replace("@use acme.payments.charge", "@use acme.payments"),
        encoding="utf-8",
    )
    assert main(["compile", str(app)]) == 1
    assert "EUSE001" in capsys.readouterr().err


def test_install_check_json_reports_drift(tmp_path, capsys):
    from nlsc.cli import main

    project = _project(tmp_path)
    assert main(["install", str(project)]) == 0
    capsys.readouterr()
    (project / "vendor" / "payments" / "v1" / "charge.nl").write_text(
        "changed\n", encoding="utf-8"
    )
    assert main(["install", "--check", "--json", str(project)]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is False
    assert [d["code"] for d in payload["diagnostics"]] == ["EPKG004"]
