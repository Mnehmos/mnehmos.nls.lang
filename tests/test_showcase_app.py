"""Exercise the compiled Aster showcase through its domain and HTTP boundaries."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from nlsc.emitter import emit_property_tests, emit_python
from nlsc.parser import parse_nl_file
from nlsc.pipeline import evaluate_semantic_gate


APP = Path(__file__).resolve().parents[1] / "examples/showcase/mission_control.nl"


@pytest.fixture(scope="module")
def compiled(tmp_path_factory):
    source = parse_nl_file(APP.read_text(encoding="utf-8"), source_path=APP.as_posix())
    gate = evaluate_semantic_gate(source, file_token=str(APP))
    assert not (gate.fatal + gate.strict_only + gate.scaffold_warnings)
    path = tmp_path_factory.mktemp("aster") / "mission_control.py"
    path.write_text(emit_python(source), encoding="utf-8")
    spec = importlib.util.spec_from_file_location("mission_control", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.ASSET_ROOT = APP.parent
    return module, source


def plan(**overrides):
    return {"route": ["basalt", "echo", "relay"], "battery": 160,
            "payload_limit": 45, "reserve_percent": 20, "pace": "Traverse",
            "weather": "Clear", **overrides}


def test_round_trip_includes_return_to_base(compiled):
    app, _ = compiled
    point = app.Waypoint("test", "Test", 3, 4, 10, 2, 1)
    assert app.route_distance([point], app.base()) == 10
    assert app.route_distance([], app.base()) == 0


@pytest.mark.parametrize("weather", ["Clear", "Dust", "Storm"])
@pytest.mark.parametrize("pace", ["Eco", "Traverse", "Sprint"])
def test_launch_manifest_agrees_with_readiness(compiled, weather, pace):
    app, _ = compiled
    result = app.evaluate_request(plan(battery=240, pace=pace, weather=weather), launch=True)
    report = result["report"]
    assert 0 <= result["energy_percent"] <= 100
    assert report["can_launch"]
    assert len(result["legs"]) == 4
    assert result["legs"][-1]["destination"] == "Aster Base"
    for field, leg_field in [("distance", "distance"), ("energy", "energy"), ("hours", "hours")]:
        assert sum(leg[leg_field] for leg in result["legs"]) == pytest.approx(report[field])
    assert report["remaining"] >= report["reserve"]


@pytest.mark.parametrize("payload,code", [
    (plan(route=[]), "NO_ROUTE"),
    (plan(battery=20), "POWER_RESERVE"),
    (plan(payload_limit=5, battery=240), "PAYLOAD_LIMIT"),
])
def test_launch_contracts_block_invalid_missions(compiled, payload, code):
    app, _ = compiled
    assert not app.evaluate_request(payload)["report"]["can_launch"]
    with pytest.raises(Exception) as caught:
        app.evaluate_request(payload, launch=True)
    assert caught.value.code == code


@pytest.mark.parametrize("payload", [
    plan(route=["missing"]), plan(route=["echo", "echo"]),
    plan(route="echo"), plan(battery=True), plan(battery=float("nan")),
    plan(battery=float("inf")), plan(pace="Warp"), plan(weather="Snow"),
    plan(battery=0), plan(reserve_percent=100), [],
])
def test_invalid_inputs_are_rejected(compiled, payload):
    app, _ = compiled
    with pytest.raises(ValueError):
        app.evaluate_request(payload)


def test_rover_invariants_are_executable(compiled):
    app, _ = compiled
    with pytest.raises(ValueError):
        app.Rover(160, 20, 45, "Warp", "Clear")
    with pytest.raises(ValueError):
        app.Rover(160, 20, 45, "Eco", "Snow")


def test_embedded_properties_execute(compiled):
    app, source = compiled
    code = emit_property_tests(source).replace(
        "from .mission_control import *", "from mission_control import *"
    )
    namespace = {}
    exec(code, namespace)
    count = 0
    for name, cls in namespace.items():
        if name.startswith("TestProperty"):
            for method in vars(cls):
                if method.startswith("test_"):
                    getattr(cls(), method)()
                    count += 1
    assert count >= 3


def test_http_app_and_contract_errors(compiled):
    app, _ = compiled
    server = app.create_server(port=0)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    root = f"http://127.0.0.1:{server.server_port}"
    try:
        with urlopen(root) as response:
            assert "Aster Mission Control" in response.read().decode()
        with urlopen(root + "/api/catalog") as response:
            assert len(json.load(response)["waypoints"]) == 6
        with urlopen(root + "/api/source") as response:
            assert "[authorize-launch]" in response.read().decode()
        request = Request(root + "/api/launch", data=json.dumps(plan()).encode(),
                          headers={"Content-Type": "application/json"})
        with urlopen(request) as response:
            assert len(json.load(response)["legs"]) == 4
        request = Request(root + "/api/launch", data=json.dumps(plan(battery=20)).encode(),
                          headers={"Content-Type": "application/json"})
        with pytest.raises(HTTPError) as caught:
            urlopen(request)
        assert caught.value.code == 422
        assert json.load(caught.value)["code"] == "POWER_RESERVE"
        for data in [b"{", b"null", b'{"battery": NaN}']:
            with pytest.raises(HTTPError) as caught:
                urlopen(Request(root + "/api/evaluate", data=data,
                                headers={"Content-Type": "application/json"}))
            assert caught.value.code == 400
        with pytest.raises(HTTPError) as caught:
            urlopen(root + "/../README.md")
        assert caught.value.code == 404
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)
