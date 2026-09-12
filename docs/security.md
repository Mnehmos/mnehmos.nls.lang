# Security Model

What a `.nl` file can and cannot do, what you are trusting when you run one,
and how to handle untrusted input. NLS compiles to host-language source
(Python or TypeScript) and runs it; treat `.nl` files as **code**, because
that is what they are.

## What executes, and when

Static commands never execute file content:

| Command | Executes the `.nl` file? | Notes |
| --- | --- | --- |
| `nlsc verify`, `nlsc ir`, `nlsc graph`, `nlsc diff` | **No** | Parse, lower, check only. |
| `nlsc compile`, `nlsc lock:update` | **No** | Emits and syntax-validates artifacts (`py_compile` / `tsc`); does not run them. |
| `nlsc ci` | **No** (unless `--test`) | `--test` executes generated tests. |
| `nlsc test`, `nlsc run`, `nlsc watch --test` | **Yes** | Generated code runs in a subprocess. |

Analyzing an untrusted file with `verify`/`ir`/`graph` does not run it — but
it does consume CPU and memory, so resource limits still apply.

## Trust levels

From weakest to strongest privileges:

1. **Structural NLS core** — literals, references, calls, operators,
   branches. The compiler proves what it can; executable prose is
   rejected. No host access beyond what the semantics require (and
   division/modulo failures are typed).
2. **`@use <stdlib domain>`** — bundled, reviewed NLS modules resolved from
   the toolchain's stdlib roots. Read-only resolution; no code execution
   during resolution.
3. **`@imports <module>`** — host-language imports. The compiler treats the
   module as an explicitly unknown symbol, but at runtime Python/Node
   import normally: **whatever is on `sys.path`/`node_modules` is trusted
   completely**. A malicious package shadowing `math` or `json` executes.
4. **`@literal python { ... }`** — verbatim host code. Full privileges of
   the process. This is the sanctioned escape hatch and the highest trust
   level; review literal blocks like any source file.

The capability matrix matters for CI: `@literal` and `@main` are
Python-target features, and compiling them to TypeScript fails with
`ETARGET002` rather than dropping them
(see the [language spec](language-spec.md#target-capability-matrix)).

## Running untrusted files: `nlsc run --sandbox`

```bash
nlsc run untrusted.nl --sandbox            # default 30s wall-clock limit
nlsc run untrusted.nl --sandbox --timeout 5
```

The sandbox runs the generated program in an isolated interpreter
(`python -I`: no environment variables, no user site-packages, current
directory off `sys.path`) with an audit hook installed before user code is
imported. Blocked:

- process execution — `os.system`, `subprocess.Popen`, `os.exec*`/`spawn*`;
- networking — `socket.connect`/`bind`/`getaddrinfo`, `urllib`,
  `http.client`, `ftplib`, `smtplib`;
- native interop — `ctypes.dlopen`/`dlsym`;
- filesystem mutation — write-mode `open`, `os.remove`/`rename`/`mkdir`/
  `rmdir`/`chmod`, `shutil` copy/move/rmtree — except writes inside the
  run's own temporary directory (scratch space);
- browser launching — `webbrowser.open`.

Read-only file access is permitted. Violations raise `PermissionError:
sandbox: blocked '<event>'` and exit non-zero; a run exceeding the timeout
is killed.

### Honest limits

**The sandbox is defense in depth, not a security boundary.** Audit hooks
markedly raise the bar against accidental damage and casual malicious
input, but a determined attacker can bypass them (native extensions loaded
before the hook, reflection tricks, resource exhaustion). Everything the
sandbox does is in-process and advisory.

For genuinely untrusted code, add an **OS-level boundary** and run NLS
inside it:

- containers (Docker/Podman) with no network, a read-only root filesystem,
  and dropped capabilities;
- a VM or cloud sandbox (Firecracker, gVisor, Windows Sandbox);
- macOS `sandbox-exec` profiles, Linux `bubblewrap`/`firejail`/seccomp.

## Threat model summary

| Threat | Mitigation |
| --- | --- |
| Malicious `.nl` executed via `run`/`test` | `--sandbox` for accidents; OS-level isolation for hostile input |
| Malicious `@imports` package (dependency confusion, shadowing) | Pin and audit your environment; run with `-I` semantics; never rely on `sys.path` order for trust. `ESEM013` warns when module/file names shadow stdlib modules |
| `@literal` blocks doing anything | Review them; they are native code by design. Capability matrix refuses silent drops across targets |
| Compiler crashing on hostile input | Diagnostics instead of tracebacks; resource limits still required |
| Supply chain of the toolchain itself | Install `nlsc` from PyPI with hashes; CI pins versions |

## Responsible disclosure

Security issues in `nlsc` (compiler, sandbox, LSP, or the VS Code
extension) should be reported privately, not in public issues:

- **Preferred:** GitHub's private vulnerability reporting — the repository's
  **Security** tab → **Report a vulnerability**.
- Include: affected version (`nlsc --version`), a minimal reproducer
  (`.nl` file and command), and the observed impact.
- We aim to acknowledge within 72 hours and to ship a fix or mitigation for
  confirmed issues as a patch release, crediting reporters who wish to be
  named.

Please do not include real credentials, personal data, or third-party
systems in reproducers.
