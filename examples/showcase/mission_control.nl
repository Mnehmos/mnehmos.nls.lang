# ASTER MISSION CONTROL
# A runnable NLS showcase. The expedition rules below are compiled NLS.
# The @literal block only adapts HTTP/JSON to those rules and serves web.html.
# Run: python -m nlsc run examples/showcase/mission_control.nl --strict
# Fictional rover model for exploring the language, not flight software.

@nls 0.1
@module mission_control
@version 1.0.0
@target python
@imports math

@type Waypoint {
  code: string, required
  name: string, required
  x: number
  y: number
  science: number, min: 0
  sample_kg: number, min: 0
  dwell_hours: number, min: 0
}

@type Rover {
  battery: number, min: 20, max: 240
  reserve_percent: number, min: 10, max: 40
  payload_limit: number, min: 5, max: 90
  pace: string, required
  weather: string, required
}

@invariant Rover {
  pace in ['Eco', 'Traverse', 'Sprint']
  weather in ['Clear', 'Dust', 'Storm']
}

@type Readiness {
  status: string
  can_launch: boolean
  distance: number, min: 0
  hours: number, min: 0
  energy: number, min: 0
  remaining: number
  reserve: number, min: 0
  energy_margin: number
  payload: number, min: 0
  payload_margin: number
  science: number, min: 0
}

@type Leg {
  destination: string
  code: string
  x: number
  y: number
  distance: number, min: 0
  energy: number, min: 0
  hours: number, min: 0
  science: number, min: 0
}

[base]
PURPOSE: Locate the rover's starting point and required return destination.
RETURNS: Waypoint("base", "Aster Base", 0, 0, 0, 0, 0)

[catalog]
PURPOSE: Offer six fictional survey sites with explicit scientific and payload tradeoffs.
RETURNS: [Waypoint("basalt", "Basalt Gate", 6, 3, 18, 4, 0.5), Waypoint("echo", "Echo Crater", 12, 9, 38, 9, 1.2), Waypoint("glass", "Glass Dunes", 20, 5, 26, 6, 0.8), Waypoint("ridge", "North Ridge", 8, 19, 42, 11, 1.5), Waypoint("delta", "Delta Shelf", 21, 20, 58, 15, 2), Waypoint("relay", "Relay Spire", 3, 12, 22, 3, 0.4)]

[distance-between]
PURPOSE: Measure the straight-line distance between two sites in kilometers.
INPUTS:
  - origin:      Waypoint
  - destination: Waypoint
LOGIC:
  1. dx = destination.x - origin.x
  2. dy = destination.y - origin.y
RETURNS: math.sqrt(dx * dx + dy * dy)

[route-distance]
PURPOSE: Recursively total an ordered route, always including its return to base.
INPUTS:
  - route:  list of Waypoint
  - origin: Waypoint
  - cursor: number, optional
LOGIC:
  1. IF cursor is not None THEN cursor -> index ELSE 0 -> index
  2. IF index >= len(route) THEN [distance-between](origin, [base]()) -> distance ELSE [distance-between](origin, route[(index)]) + [route-distance](route, route[(index)], index + 1) -> distance
RETURNS: distance
DEPENDS: [distance-between], [base]

[science-total]
PURPOSE: Sum the science points collected at the selected stops.
INPUTS:
  - route: list of Waypoint
LOGIC:
  1. FOR EACH stop IN route: ADD stop.science -> total
RETURNS: total

[payload-total]
PURPOSE: Sum the sample mass that must fit in the rover's cargo bay.
INPUTS:
  - route: list of Waypoint
LOGIC:
  1. FOR EACH stop IN route: ADD stop.sample_kg -> total
RETURNS: total

[sampling-hours]
PURPOSE: Sum the time spent collecting samples rather than driving.
INPUTS:
  - route: list of Waypoint
LOGIC:
  1. FOR EACH stop IN route: ADD stop.dwell_hours -> total
RETURNS: total

[pace-factor]
PURPOSE: Trade energy efficiency for travel speed.
INPUTS:
  - pace: string
GUARDS:
  - pace in ["Eco", "Traverse", "Sprint"] -> ValueError("Choose Eco, Traverse, or Sprint")
LOGIC:
  1. IF pace == "Sprint" THEN 1.35 -> fast_factor ELSE 1 -> fast_factor
  2. IF pace == "Eco" THEN 0.85 -> factor ELSE fast_factor -> factor
RETURNS: factor
EFFECTS: pure

[travel-speed]
PURPOSE: Map the selected driving mode to kilometers per hour.
INPUTS:
  - pace: string
GUARDS:
  - pace in ["Eco", "Traverse", "Sprint"] -> ValueError("Choose Eco, Traverse, or Sprint")
LOGIC:
  1. IF pace == "Sprint" THEN 12 -> fast_speed ELSE 9 -> fast_speed
  2. IF pace == "Eco" THEN 6 -> speed ELSE fast_speed -> speed
RETURNS: speed
EFFECTS: pure

[weather-factor]
PURPOSE: Increase driving energy demand under dust and storm conditions.
INPUTS:
  - weather: string
GUARDS:
  - weather in ["Clear", "Dust", "Storm"] -> ValueError("Choose Clear, Dust, or Storm")
LOGIC:
  1. IF weather == "Storm" THEN 1.6 -> storm_factor ELSE 1.25 -> storm_factor
  2. IF weather == "Clear" THEN 1 -> factor ELSE storm_factor -> factor
RETURNS: factor
EFFECTS: pure

[energy-needed]
PURPOSE: Budget driving with the full planned payload on every leg, plus sampling at 3 kW.
INPUTS:
  - distance: number
  - payload:  number
  - sampling: number
  - rover:    Rover
GUARDS:
  - distance >= 0 -> ValueError("Distance cannot be negative")
  - payload >= 0 -> ValueError("Payload cannot be negative")
  - sampling >= 0 -> ValueError("Sampling time cannot be negative")
LOGIC:
  1. consumption = 1.2 + payload * 0.015
  2. driving = distance * consumption * [pace-factor](rover.pace) * [weather-factor](rover.weather)
RETURNS: driving + sampling * 3
DEPENDS: [pace-factor], [weather-factor]
EFFECTS: pure

[mission-hours]
PURPOSE: Combine driving time with sample collection time.
INPUTS:
  - distance: number
  - sampling: number
  - pace:     string
RETURNS: distance / [travel-speed](pace) + sampling
DEPENDS: [travel-speed]

[reserve-energy]
PURPOSE: Protect the operator's chosen fraction of the battery from mission use.
INPUTS:
  - rover: Rover
RETURNS: rover.battery * rover.reserve_percent / 100

[readiness-label]
PURPOSE: Explain the first unmet launch condition in a stable order.
INPUTS:
  - stops:          number
  - energy_margin:  number
  - payload_margin: number
LOGIC:
  1. IF payload_margin < 0 THEN "OVER CAPACITY" -> cargo_status ELSE "READY TO EXPLORE" -> cargo_status
  2. IF energy_margin < 0 THEN "LOW POWER" -> power_status ELSE cargo_status -> power_status
  3. IF stops == 0 THEN "AWAITING ROUTE" -> status ELSE power_status -> status
RETURNS: status
EFFECTS: pure

[assess-mission]
PURPOSE: Turn a proposed route and rover configuration into an auditable launch decision.
INPUTS:
  - route: list of Waypoint
  - rover: Rover
GUARDS:
  - len(route) <= 6 -> ValueError("A mission supports at most six stops")
LOGIC:
  1. [planned] distance = [route-distance](route, [base]())
  2. payload = [payload-total](route)
  3. sampling = [sampling-hours](route)
  4. [budgeted] energy = [energy-needed](distance, payload, sampling, rover)
  5. reserve = [reserve-energy](rover)
  6. remaining = rover.battery - energy
  7. energy_margin = remaining - reserve
  8. payload_margin = rover.payload_limit - payload
  9. [checked] can_launch = len(route) > 0 and energy_margin >= 0 and payload_margin >= 0
  10. status = [readiness-label](len(route), energy_margin, payload_margin)
RETURNS: Readiness(status, can_launch, distance, [mission-hours](distance, sampling, rover.pace), energy, remaining, reserve, energy_margin, payload, payload_margin, [science-total](route))
DEPENDS: [route-distance], [base], [payload-total], [sampling-hours], [energy-needed], [reserve-energy], [readiness-label], [mission-hours], [science-total]

[authorize-launch]
PURPOSE: Refuse launch when the route, energy reserve, or sample capacity contract fails.
INPUTS:
  - route:  list of Waypoint
  - report: Readiness
GUARDS:
  - len(route) > 0 -> ValueError(NO_ROUTE, "Choose at least one survey site before launch")
  - report.energy_margin >= 0 -> ValueError(POWER_RESERVE, "This route would consume the protected energy reserve")
  - report.payload_margin >= 0 -> ValueError(PAYLOAD_LIMIT, "The planned samples exceed the cargo capacity")
RETURNS: report

[make-leg]
PURPOSE: Describe one travel segment using the same energy and time rules as the planner.
INPUTS:
  - origin:      Waypoint
  - destination: Waypoint
  - payload:     number
  - rover:       Rover
LOGIC:
  1. distance = [distance-between](origin, destination)
  2. energy = [energy-needed](distance, payload, destination.dwell_hours, rover)
  3. hours = [mission-hours](distance, destination.dwell_hours, rover.pace)
RETURNS: Leg(destination.name, destination.code, destination.x, destination.y, distance, energy, hours, destination.science)
DEPENDS: [distance-between], [energy-needed], [mission-hours]

[build-legs]
PURPOSE: Recursively create a flight manifest ending safely at Aster Base.
INPUTS:
  - route:   list of Waypoint
  - origin:  Waypoint
  - payload: number
  - rover:   Rover
  - cursor:  number, optional
LOGIC:
  1. IF cursor is not None THEN cursor -> index ELSE 0 -> index
  2. IF index >= len(route) THEN [[make-leg](origin, [base](), payload, rover)] -> legs ELSE [[make-leg](origin, route[(index)], payload, rover)] + [build-legs](route, route[(index)], payload, rover, index + 1) -> legs
RETURNS: legs
DEPENDS: [make-leg], [base]

[clamp-percent]
PURPOSE: Keep display percentages within a valid progress range.
INPUTS:
  - value: number
RETURNS: min(100, max(0, value))

@test [distance-between] {
  distance_between(base(), Waypoint("t", "Test", 3, 4, 0, 0, 0)) == 5
  distance_between(base(), base()) == 0
}

@test [route-distance] {
  route_distance([], base()) == 0
  route_distance([Waypoint("t", "Test", 3, 4, 0, 0, 0)], base()) == 10
}

@test [science-total] {
  science_total([]) == 0
  science_total(catalog()) == 204
}


@test [payload-total] {
  payload_total([]) == 0
  payload_total(catalog()) == 48
}

@test [sampling-hours] {
  sampling_hours([]) == 0
  sampling_hours([Waypoint("t", "Test", 0, 0, 0, 0, 2)]) == 2
}

@test [pace-factor] {
  pace_factor("Eco") == 0.85
  pace_factor("Traverse") == 1
  pace_factor("Sprint") == 1.35
}

@test [weather-factor] {
  weather_factor("Clear") == 1
  weather_factor("Dust") == 1.25
  weather_factor("Storm") == 1.6
}

@test [energy-needed] {
  energy_needed(10, 0, 1, Rover(160, 20, 45, "Traverse", "Clear")) == 15
  energy_needed(0, 0, 0, Rover(160, 20, 45, "Eco", "Storm")) == 0
}

@test [mission-hours] {
  mission_hours(12, 1, "Eco") == 3
  mission_hours(12, 1, "Sprint") == 2
}

@test [reserve-energy] {
  reserve_energy(Rover(160, 20, 45, "Traverse", "Clear")) == 32
  reserve_energy(Rover(100, 40, 45, "Traverse", "Clear")) == 40
}

@test [readiness-label] {
  readiness_label(0, 10, 10) == "AWAITING ROUTE"
  readiness_label(1, -1, 10) == "LOW POWER"
  readiness_label(1, 10, -1) == "OVER CAPACITY"
  readiness_label(1, 0, 0) == "READY TO EXPLORE"
}

@test [assess-mission] {
  assess_mission([], Rover(160, 20, 45, "Traverse", "Clear")).can_launch == False
  assess_mission([], Rover(160, 20, 45, "Traverse", "Clear")).remaining == 160
  assess_mission([Waypoint("t", "Test", 3, 4, 10, 2, 1)], Rover(160, 20, 45, "Traverse", "Clear")).can_launch == True
  assess_mission(catalog(), Rover(240, 20, 5, "Eco", "Clear")).can_launch == False
}

@test [build-legs] {
  len(build_legs([Waypoint("t", "Test", 3, 4, 10, 2, 1)], base(), 2, Rover(160, 20, 45, "Traverse", "Clear"))) == 2
  build_legs([], base(), 0, Rover(160, 20, 45, "Traverse", "Clear"))[0].destination == "Aster Base"
}

@test [clamp-percent] {
  clamp_percent(-10) == 0
  clamp_percent(150) == 100
  clamp_percent(42) == 42
}

@property [clamp-percent] {
  forall x: number -> clamp_percent(x) >= 0
  forall x: number -> clamp_percent(x) <= 100
  forall x: number -> clamp_percent(clamp_percent(x)) == clamp_percent(x)
}

# Standard-library HTTP adapter. Domain decisions call compiled ANLUs above.
# No third-party web framework, account, API key, or remote service is needed.
@literal python {
import json
import os
import sys
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ASSET_ROOT = next(
    (Path(p) for p in [str(Path(__file__).parent), *sys.path]
     if p and (Path(p) / "mission_control.nl").is_file()
     and (Path(p) / "web.html").is_file()),
    Path(__file__).parent,
)

def evaluate_request(data, launch=False):
    """Validate transport types, then call compiled NLS constructors and rules."""
    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object")
    codes = data.get("route", [])
    if not isinstance(codes, list) or any(not isinstance(code, str) for code in codes):
        raise ValueError("Route must be a list of site codes")
    available = {site.code: site for site in catalog()}
    if len(codes) > 6 or len(set(codes)) != len(codes):
        raise ValueError("Choose each site at most once, up to six stops")
    if any(code not in available for code in codes):
        raise ValueError("Route contains an unknown survey site")
    numeric = {}
    for key, default in [("battery", 160), ("reserve_percent", 20), ("payload_limit", 45)]:
        value = data.get(key, default)
        if type(value) not in (int, float) or not math.isfinite(value):
            raise ValueError(key + " must be a finite number")
        numeric[key] = value
    rover = Rover(**numeric, pace=data.get("pace", "Traverse"), weather=data.get("weather", "Clear"))
    route = [available[code] for code in codes]
    report = assess_mission(route, rover)
    if launch:
        authorize_launch(route, report)
    legs = build_legs(route, base(), report.payload, rover) if route else []
    return {"report": asdict(report), "energy_percent": clamp_percent(report.energy / rover.battery * 100),
            "legs": [asdict(leg) for leg in legs],
            "route": [asdict(site) for site in route], "rover": asdict(rover)}

class MissionHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def reply(self, status, body, content_type="application/json; charset=utf-8"):
        if not isinstance(body, bytes):
            body = json.dumps(body, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/":
            self.reply(200, (ASSET_ROOT / "web.html").read_bytes(), "text/html; charset=utf-8")
        elif path == "/api/catalog":
            self.reply(200, {"waypoints": [asdict(site) for site in catalog()], "base": asdict(base())})
        elif path == "/api/source":
            self.reply(200, (ASSET_ROOT / "mission_control.nl").read_bytes(), "text/plain; charset=utf-8")
        elif path == "/favicon.ico":
            self.reply(204, b"")
        else:
            self.reply(404, {"error": "Not found"})

    def do_POST(self):
        path = urlsplit(self.path).path
        if path not in ("/api/evaluate", "/api/launch"):
            self.reply(404, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 16384:
                raise ValueError("Expected a JSON request smaller than 16 KB")
            data = json.loads(self.rfile.read(length))
            result = evaluate_request(data, launch=path == "/api/launch")
            self.reply(200, result)
        except (ValueError, TypeError, KeyError, OverflowError) as error:
            code = getattr(error, "code", "INVALID_PLAN")
            self.reply(400 if code == "INVALID_PLAN" else 422, {"error": str(error), "code": code})

def create_server(port=8765):
    """Bind only to the local computer. Port zero is useful for smoke tests."""
    return ThreadingHTTPServer(("127.0.0.1", port), MissionHandler)

def serve_showcase():
    port = int(os.environ.get("ASTER_PORT", "8765"))
    with create_server(port) as server:
        print("Aster Mission Control: http://127.0.0.1:" + str(server.server_port), flush=True)
        print("Local fictional rover simulation. Press Ctrl+C to stop.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
}

@main {
  serve_showcase()
}
