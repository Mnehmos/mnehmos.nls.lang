# Edit Provenance

Who wrote this revision — a human, an LLM, or a tool? NLS records the
answer in a **provenance sidecar** next to the spec, and the CI gate
refuses to pass LLM-authored changes until a human reviews them.

```
src/payments.nl
src/payments.nl.provenance.json    <- committed alongside the source
```

The sidecar is an audit trail: commit it with the spec so review history
travels with the code.

## Format

```json
{
  "file": "payments.nl",
  "timestamp": "2026-09-12T10:30:00+00:00",
  "source": {
    "type": "llm",
    "model": "claude-3-opus",
    "conversation_id": "abc123"
  },
  "changes": [
    { "type": "anlu", "name": "charge-payment", "lines": [12] }
  ],
  "status": "pending",
  "human_review": null
}
```

| Field | Values |
| --- | --- |
| `source.type` | `human`, `llm`, `tool` |
| `status` | `draft`, `pending`, `accepted`, `rejected` |
| `source.model`, `source.conversation_id` | optional, for LLM edits |
| `changes` | record of what changed; `nlsc provenance` refreshes it with the ANLUs in the file |
| `human_review` | set to `accepted` when a human accepts the revision |

## CLI

```bash
# Read
nlsc provenance src/payments.nl            # human-readable JSON
nlsc provenance src/payments.nl --json     # structured, with recorded: false when absent

# Record an LLM proposal (blocks CI until reviewed)
nlsc provenance src/payments.nl \
  --source llm --model claude-3-opus --conversation abc123 \
  --status pending

# Human review
nlsc provenance src/payments.nl --status accepted
nlsc provenance src/payments.nl --status rejected

# Record a human/tool revision, or remove the sidecar entirely
nlsc provenance src/payments.nl --source human --status accepted
nlsc provenance src/payments.nl --clear
```

## The workflow: LLM proposes → human reviews → CI verifies

1. **An LLM proposes a change.** After applying it, record:

   ```bash
   nlsc provenance src/payments.nl --source llm --model <model> --status pending
   ```

2. **CI refuses.** `nlsc ci src/payments.nl` fails with `EPROV001`
   ("provenance status is 'pending'; review required") — no LLM-authored
   revision reaches a release without a human in the loop.

3. **A human reviews** the natural-language spec (the point of NLS: the
   change is reviewable without reading generated code) and either
   accepts or rejects it:

   ```bash
   nlsc provenance src/payments.nl --status accepted   # unlocks CI
   ```

4. **CI verifies.** `nlsc ci` now reports `provenance: accepted` in its
   stage summary and proceeds to the semantic gate, lockfile check, and
   tests.

Malformed sidecars fail everywhere they are read (`EPROV002`) — a typo
cannot silently downgrade the trust check. A spec **without** a sidecar
is unaffected: provenance is opt-in, so existing projects keep working.

## Design notes

- **Sidecar, not source header.** Provenance changes on every edit; the
  spec should not churn for audit metadata, and generated artifacts and
  hashes stay untouched.
- **A gate, not a signature.** The format records intent and review
  status; it does not cryptographically attest authorship. Pair it with
  signed commits if you need non-repudiation.
- **`changes` is best-effort.** The CLI records the ANLUs present when a
  sidecar is created; richer diffs can be added by callers (for example
  MCP tooling) by writing the sidecar directly in this format.
