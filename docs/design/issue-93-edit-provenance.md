# Issue #93 — Standardized Edit Provenance for `.nl` Changes

Run: `run-20260212-issues-001`  
Task: `task-003-issue-93-provenance-spec`

This document defines the **normative, machine-parseable** format for recording provenance of edits to `.nl` files.

---

## 1) Scope and intent

This spec standardizes edit metadata so tooling can:

1. Audit who/what changed an `.nl` file.
2. Validate provenance records consistently.
3. Exchange provenance across CLI, editors, automation, and CI.

Out of scope:

* Runtime semantics of `.nl` execution.
* Compiler behavior changes.

---

## 2) Canonical record format

Each edit event MUST be encoded as one JSON object with this top-level shape:

```json
{
  "schema_version": "1.0.0",
  "record_id": "epr_01K2X9M59YV7A8B2WQ4KJ6R3T1",
  "timestamp": "2026-02-12T17:00:00Z",
  "run_id": "run-20260212-issues-001",
  "task_id": "task-003-issue-93-provenance-spec",
  "target": {
    "path": "docs/language-spec.md",
    "file_type": "nl_doc",
    "before_sha256": "e3b0c44298fc1c149afbf4c8996fb924...",
    "after_sha256": "4f0c3a6b8f4f8f1646c9c1cce4d5e87f..."
  },
  "edit": {
    "operation": "update",
    "summary": "Add normative provenance reference section",
    "change_set": {
      "format": "unified_diff",
      "content": "@@ ..."
    }
  },
  "source": {
    "kind": "human",
    "id": "user:mnehm",
    "display_name": "Mnehmos"
  },
  "context": {
    "workspace": "f:/Github/mnehmos.nls.lang",
    "tool": "manual-edit"
  }
}
```

---

## 3) Field contract

### 3.1 Required fields

| Field | Type | Constraints |
| --- | --- | --- |
| `schema_version` | string | SemVer, MUST match supported major (currently `1.x.y`) |
| `record_id` | string | Stable unique ID, pattern `^epr_[A-Za-z0-9_-]{10,64}$` |
| `timestamp` | string | RFC3339 UTC timestamp |
| `target` | object | MUST include `path`, `file_type`, `before_sha256`, `after_sha256` |
| `edit` | object | MUST include `operation`, `summary`, `change_set` |
| `source` | object | MUST include `kind`, `id` |

### 3.2 Optional fields

| Field | Type | Notes |
| --- | --- | --- |
| `run_id` | string | Orchestrated run identifier |
| `task_id` | string | Task identifier in a run |
| `context` | object | Environment/tool metadata |
| `source.display_name` | string | Human-friendly label |
| `source.model` | object | Required when `source.kind = "llm"` |
| `source.tool` | object | Required when `source.kind = "tool"` |

### 3.3 Enums

`target.file_type` MUST be one of:

* `nl_source` (for `*.nl`)
* `nl_lock` (for `*.nl.lock`)
* `nl_doc` (for docs/spec files describing `.nl` behavior)

`edit.operation` MUST be one of:

* `create`
* `update`
* `delete`
* `rename`
* `move`

`edit.change_set.format` MUST be one of:

* `unified_diff`
* `json_patch`
* `replace_full`

`source.kind` MUST be one of:

* `human`
* `llm`
* `tool`

---

## 4) Validation rules (normative)

1. `schema_version` MUST match `^1\.[0-9]+\.[0-9]+$` for this spec revision.
2. `timestamp` MUST be UTC (`Z` suffix).
3. `target.path` MUST be a relative repository path; absolute paths are invalid.
4. `target.before_sha256` and `target.after_sha256` MUST be lowercase hex SHA-256 (64 chars) **or** the literal `null` for non-existent side:
   * `create` => `before_sha256 = null`, `after_sha256 != null`
   * `delete` => `before_sha256 != null`, `after_sha256 = null`
   * `update|rename|move` => both non-null
5. `edit.summary` MUST be non-empty, max 280 chars.
6. `edit.change_set.content` MUST be non-empty.
7. Conditional requirements:
   * If `source.kind = "human"`, `source.id` SHOULD use `user:<id>` format.
   * If `source.kind = "llm"`, `source.model.provider` and `source.model.name` are REQUIRED.
   * If `source.kind = "tool"`, `source.tool.name` and `source.tool.version` are REQUIRED.

---

## 5) JSON Schema (reference implementation)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://mnehmos.github.io/schemas/edit-provenance/v1.json",
  "title": "Edit Provenance Record v1",
  "type": "object",
  "required": ["schema_version", "record_id", "timestamp", "target", "edit", "source"],
  "additionalProperties": false,
  "properties": {
    "schema_version": { "type": "string", "pattern": "^1\\.[0-9]+\\.[0-9]+$" },
    "record_id": { "type": "string", "pattern": "^epr_[A-Za-z0-9_-]{10,64}$" },
    "timestamp": { "type": "string", "format": "date-time", "pattern": "Z$" },
    "run_id": { "type": "string", "minLength": 1 },
    "task_id": { "type": "string", "minLength": 1 },
    "target": {
      "type": "object",
      "required": ["path", "file_type", "before_sha256", "after_sha256"],
      "additionalProperties": false,
      "properties": {
        "path": { "type": "string", "pattern": "^(?![A-Za-z]:)(?!/).+" },
        "file_type": { "type": "string", "enum": ["nl_source", "nl_lock", "nl_doc"] },
        "before_sha256": {
          "anyOf": [
            { "type": "string", "pattern": "^[a-f0-9]{64}$" },
            { "type": "null" }
          ]
        },
        "after_sha256": {
          "anyOf": [
            { "type": "string", "pattern": "^[a-f0-9]{64}$" },
            { "type": "null" }
          ]
        }
      }
    },
    "edit": {
      "type": "object",
      "required": ["operation", "summary", "change_set"],
      "additionalProperties": false,
      "properties": {
        "operation": { "type": "string", "enum": ["create", "update", "delete", "rename", "move"] },
        "summary": { "type": "string", "minLength": 1, "maxLength": 280 },
        "change_set": {
          "type": "object",
          "required": ["format", "content"],
          "additionalProperties": false,
          "properties": {
            "format": { "type": "string", "enum": ["unified_diff", "json_patch", "replace_full"] },
            "content": { "type": "string", "minLength": 1 }
          }
        }
      }
    },
    "source": {
      "type": "object",
      "required": ["kind", "id"],
      "additionalProperties": false,
      "properties": {
        "kind": { "type": "string", "enum": ["human", "llm", "tool"] },
        "id": { "type": "string", "minLength": 1 },
        "display_name": { "type": "string", "minLength": 1 },
        "model": {
          "type": "object",
          "required": ["provider", "name"],
          "additionalProperties": false,
          "properties": {
            "provider": { "type": "string", "minLength": 1 },
            "name": { "type": "string", "minLength": 1 }
          }
        },
        "tool": {
          "type": "object",
          "required": ["name", "version"],
          "additionalProperties": false,
          "properties": {
            "name": { "type": "string", "minLength": 1 },
            "version": { "type": "string", "minLength": 1 }
          }
        }
      },
      "allOf": [
        {
          "if": { "properties": { "kind": { "const": "llm" } }, "required": ["kind"] },
          "then": { "required": ["model"] }
        },
        {
          "if": { "properties": { "kind": { "const": "tool" } }, "required": ["kind"] },
          "then": { "required": ["tool"] }
        }
      ]
    },
    "context": {
      "type": "object",
      "additionalProperties": true,
      "properties": {
        "workspace": { "type": "string" },
        "tool": { "type": "string" }
      }
    }
  }
}
```

---

## 6) Normative examples

### 6.1 Human-authored edit

```json
{
  "schema_version": "1.0.0",
  "record_id": "epr_01K2X9N5T7XG3AAQKPS8R61P6F",
  "timestamp": "2026-02-12T17:03:00Z",
  "target": {
    "path": "examples/workflow_engine.nl",
    "file_type": "nl_source",
    "before_sha256": "1111111111111111111111111111111111111111111111111111111111111111",
    "after_sha256": "2222222222222222222222222222222222222222222222222222222222222222"
  },
  "edit": {
    "operation": "update",
    "summary": "Clarify PURPOSE sentence in [execute-workflow]",
    "change_set": {
      "format": "unified_diff",
      "content": "@@ -1,5 +1,5 @@ ..."
    }
  },
  "source": {
    "kind": "human",
    "id": "user:mnehm",
    "display_name": "Mnehmos"
  }
}
```

### 6.2 LLM-authored edit

```json
{
  "schema_version": "1.0.0",
  "record_id": "epr_01K2X9P3M9P4W5YQ2T6A5B6J9R",
  "timestamp": "2026-02-12T17:05:00Z",
  "run_id": "run-20260212-issues-001",
  "task_id": "task-003-issue-93-provenance-spec",
  "target": {
    "path": "docs/language-spec.md",
    "file_type": "nl_doc",
    "before_sha256": "3333333333333333333333333333333333333333333333333333333333333333",
    "after_sha256": "4444444444444444444444444444444444444444444444444444444444444444"
  },
  "edit": {
    "operation": "update",
    "summary": "Add normative reference to Issue #93 provenance format",
    "change_set": {
      "format": "replace_full",
      "content": "...full replacement payload..."
    }
  },
  "source": {
    "kind": "llm",
    "id": "agent:architect",
    "model": {
      "provider": "openai",
      "name": "gpt-5.3-codex"
    }
  },
  "context": {
    "workspace": "f:/Github/mnehmos.nls.lang",
    "tool": "apply_patch"
  }
}
```

### 6.3 Tool-authored edit

```json
{
  "schema_version": "1.0.0",
  "record_id": "epr_01K2X9QKJ42QTT8F1M3FWA9AB2",
  "timestamp": "2026-02-12T17:07:00Z",
  "target": {
    "path": "examples/workflow_engine.nl.lock",
    "file_type": "nl_lock",
    "before_sha256": "5555555555555555555555555555555555555555555555555555555555555555",
    "after_sha256": "6666666666666666666666666666666666666666666666666666666666666666"
  },
  "edit": {
    "operation": "update",
    "summary": "Refresh lockfile after dependency graph normalization",
    "change_set": {
      "format": "json_patch",
      "content": "[{\"op\":\"replace\",\"path\":\"/hash\",\"value\":\"...\"}]"
    }
  },
  "source": {
    "kind": "tool",
    "id": "tool:nlsc",
    "tool": {
      "name": "nlsc",
      "version": "0.1.0"
    }
  }
}
```

---

## 7) Versioning guidance

1. `schema_version` follows SemVer.
2. Producers/consumers MUST reject unsupported **major** versions.
3. Minor/patch upgrades within major `1` MUST remain backward compatible.
4. On a breaking change, increment major and publish a new schema identifier (for example, `.../v2.json`).

---

## 8) Implementation notes (non-normative)

* Persist provenance as newline-delimited JSON (`.jsonl`) for append-only audit streams.
* Store full diffs out-of-band when large; retain stable references in `edit.change_set.content`.

