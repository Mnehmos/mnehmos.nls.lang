# Aster Mission Control

A runnable `.nl` app: plan a fictional rover expedition, balance power and sample
capacity, then follow its simulated journey back to base.

## Run it

From the repository root, with the compiler installed:

```sh
python -m nlsc run examples/showcase/mission_control.nl --strict
```

Open **http://127.0.0.1:8765**. Stop the server with **Ctrl+C**.
The app uses the Python standard library and local browser assets. There are no
additional web dependencies or API keys. Keep `web.html` beside the `.nl` file.

To run the included generated artifact directly:

```sh
python examples/showcase/mission_control.py
```

Set `ASTER_PORT` to use a different port. For example, in PowerShell:

```powershell
$env:ASTER_PORT = "8766"
python -m nlsc run examples/showcase/mission_control.nl --strict
```

## Take the tour

1. Start with **Balanced survey**. Select more sites on the map or the site cards.
2. Reorder stops with the flight-plan arrows. The round-trip distance changes.
3. Lower the battery to **20 kWh** to see the power-reserve contract block launch.
4. Reset, then lower sample capacity to **5 kg** to see the payload contract.
5. Try **Eco**, **Sprint**, and **Dust storm** to explore energy/time tradeoffs.
6. Reset and **Launch simulation**. All four legs finish at Aster Base. Export the
   flight log to a JSON preview with copy and file-download actions, or stop
   playback to produce an explicitly partial log.
7. Open **Under the hood** to read and copy the `.nl` source behind the results.

The plan is saved in this browser's local storage. Flight logs stay in the page
until exported; reloading clears the active playback.

## What this demonstrates

| NLS capability | Application |
| --- | --- |
| Named ANLUs with `PURPOSE`, `INPUTS`, `LOGIC`, and `RETURNS` | 19 operations for planning, resource budgets, and the flight manifest |
| `@type` constraints | Four records: `Waypoint`, `Rover`, `Readiness`, and `Leg` |
| `@invariant` | Rover driving mode and weather must belong to the supported sets |
| Ordered `GUARDS` with stable error codes | `NO_ROUTE`, `POWER_RESERVE`, and `PAYLOAD_LIMIT` are checked again on the server when launching |
| Total `IF / THEN / ELSE` branches | Every route result and status is defined on every path |
| Recursion, lists, and optional inputs | Route walkers use an optional cursor and include the return leg |
| Explicit `DEPENDS` | The compiler can generate the operation dependency graph |
| Checked `EFFECTS: pure` declarations | Driving-mode and weather arithmetic declare effect bounds |
| `[planned]`, `[budgeted]`, `[checked]` state markers | Labels on the assessment steps for graph inspection |
| `@test` and `@property` | 35 embedded examples and three generated Hypothesis properties |
| `@literal python` and `@main` | Standard-library HTTP/JSON adapter and executable entry point |
| `.nl.lock` and strict CI | Reproducible generated Python with a frozen-lockfile gate |

The browser displays the compiled model's results. The Python literal block
validates JSON types, calls the NLS constructors and operations, and serves the
interface. `web.html` handles the map, controls, request cancellation, local plan
storage, and playback. The percentage gauge also uses the compiled
`clamp-percent` operation exercised by the property tests.

## Model assumptions

This is a fictional survey model. Distances are straight-line kilometers in a
local grid, and every mission includes the return to base. Travel energy assumes
the **full planned sample payload on every leg**, giving a conservative estimate;
sampling consumes 3 kW. Eco/Traverse/Sprint use 6/9/12 km/h and energy factors of
0.85/1/1.35. Dust and storms multiply driving energy by 1.25 and 1.6. The terrain
illustration and coordinates are decorative; the six site coordinates in the NLS
catalog are the model's inputs.

Playback advances one leg every 1.4 seconds. The displayed mission hours are the
calculated duration, independent of animation time. The exported JSON separates
the planned manifest from the completed legs and records `running`, `stopped`,
or `completed` explicitly.

## Verify or modify it

Edit `mission_control.nl`, then regenerate its Python, embedded tests, and lock:

```sh
python -m nlsc fmt examples/showcase/mission_control.nl
python -m nlsc compile examples/showcase/mission_control.nl --strict
python -m nlsc ci examples/showcase/mission_control.nl --compile --test
python -m pytest tests/test_showcase_app.py -q
```

The CLI runs the 35 `@test` examples. The integration suite also executes the
three generated `@property` tests and checks real HTTP responses, invalid inputs,
launch failures, and consistency between whole-route totals and individual legs.

Inspect the dependency graph or target-neutral IR:

```sh
python -m nlsc graph examples/showcase/mission_control.nl --format mermaid
python -m nlsc ir examples/showcase/mission_control.nl --strict --check
```

This runnable showcase targets **Python**. NLS also has a TypeScript backend, but
the complete app uses Python-only `@literal`, `@main`, and property-test features.
For the current expression parser, the walkers write indexed access as
`route[(index)]` to distinguish it from bracketed ANLU references; slicing is
outside the strict expression subset. Invariant strings use single quotes so
their generated diagnostic messages remain valid Python.

The intent linter additionally reports heuristic warnings for functions without
guards/invariants and branch-protected indexing. Those style warnings are
separate from strict semantic verification and the executable CI gate above.
