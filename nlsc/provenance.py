"""Edit provenance for .nl files (Issue #93).

Records where a specification's changes came from — human, LLM, or tool —
so review and CI can reason about trust.  The format is a JSON sidecar
next to the spec (``<file>.nl.provenance.json``, committed alongside the
source as an audit trail); the authoritative description lives in
``docs/provenance.md``.

The trust gate: a spec whose provenance status is ``pending`` (typically
LLM-authored, not yet reviewed) fails ``nlsc ci`` until a human marks it
``accepted``.  Specs without a provenance file are unaffected — the
mechanism is opt-in.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

PROVENANCE_SUFFIX = ".provenance.json"

VALID_SOURCES = ("human", "llm", "tool")
VALID_STATUSES = ("draft", "pending", "accepted", "rejected")


@dataclass
class ProvenanceChange:
    """One recorded change within a provenance entry."""

    type: str
    name: Optional[str] = None
    lines: Optional[list[int]] = None

    def to_json(self) -> dict:
        data: dict = {"type": self.type}
        if self.name is not None:
            data["name"] = self.name
        if self.lines is not None:
            data["lines"] = list(self.lines)
        return data


@dataclass
class Provenance:
    """Provenance record for one .nl file."""

    file: str
    source_type: str
    status: str = "draft"
    timestamp: str = ""
    model: Optional[str] = None
    conversation_id: Optional[str] = None
    changes: list[ProvenanceChange] = field(default_factory=list)
    human_review: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_json(self) -> dict:
        source: dict = {"type": self.source_type}
        if self.model:
            source["model"] = self.model
        if self.conversation_id:
            source["conversation_id"] = self.conversation_id
        data: dict = {
            "file": self.file,
            "timestamp": self.timestamp,
            "source": source,
            "changes": [change.to_json() for change in self.changes],
            "status": self.status,
        }
        if self.human_review:
            data["human_review"] = self.human_review
        return data

    @classmethod
    def from_json(cls, data: dict) -> "Provenance":
        source = data.get("source") or {}
        return cls(
            file=str(data.get("file", "")),
            source_type=str(source.get("type", "tool")),
            status=str(data.get("status", "draft")),
            timestamp=str(data.get("timestamp", "")),
            model=source.get("model"),
            conversation_id=source.get("conversation_id"),
            changes=[
                ProvenanceChange(
                    type=str(entry.get("type", "change")),
                    name=entry.get("name"),
                    lines=entry.get("lines"),
                )
                for entry in data.get("changes", [])
            ],
            human_review=data.get("human_review"),
        )


def provenance_path(source_path: Path) -> Path:
    """Sidecar path for a .nl file."""
    return Path(str(source_path) + PROVENANCE_SUFFIX)


def validation_errors(record: Provenance) -> list[str]:
    """Structural problems with a provenance record."""
    problems: list[str] = []
    if record.source_type not in VALID_SOURCES:
        problems.append(
            f"unknown source type '{record.source_type}' "
            f"(expected one of: {', '.join(VALID_SOURCES)})"
        )
    if record.status not in VALID_STATUSES:
        problems.append(
            f"unknown status '{record.status}' "
            f"(expected one of: {', '.join(VALID_STATUSES)})"
        )
    return problems


def write_provenance(record: Provenance, path: Path) -> None:
    """Write the sidecar (deterministic key order)."""
    path.write_text(
        json.dumps(record.to_json(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def read_provenance(path: Path) -> tuple[Optional[Provenance], Optional[str]]:
    """Read a sidecar; returns (record, error_message)."""
    if not path.exists():
        return None, None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return None, f"malformed provenance file: {exc}"
    if not isinstance(data, dict):
        return None, "malformed provenance file: expected a JSON object"
    record = Provenance.from_json(data)
    problems = validation_errors(record)
    if problems:
        return None, "; ".join(problems)
    return record, None


_NAME_TOKEN = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")


def guess_changes(source_path: Path) -> list[ProvenanceChange]:
    """Best-effort change inventory: the ANLUs defined in the file.

    Keeps the record useful without diffing against a previous revision;
    ``nlsc provenance <file> --status ...`` refreshes it on every write.
    """
    try:
        from .parser import parse_nl_file

        nl_file = parse_nl_file(
            source_path.read_text(encoding="utf-8"), source_path=str(source_path)
        )
    except Exception:
        return []
    changes: list[ProvenanceChange] = []
    for anlu in nl_file.anlus:
        if _NAME_TOKEN.match(anlu.identifier):
            changes.append(
                ProvenanceChange(
                    type="anlu",
                    name=anlu.identifier,
                    lines=[anlu.line_number] if anlu.line_number else None,
                )
            )
    return changes
