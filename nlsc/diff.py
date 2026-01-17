"""
NLS Diff - Show changes since last compile

Compares current .nl file state against lockfile to detect:
- New ANLUs
- Modified ANLUs
- Removed ANLUs
- Unchanged ANLUs
"""

import difflib
from dataclasses import dataclass
from typing import Literal

from .schema import NLFile
from .lockfile import Lockfile, hash_anlu


@dataclass
class ANLUChange:
    """Represents a change to a single ANLU"""
    identifier: str
    status: Literal["unchanged", "modified", "new", "removed"]
    details: str = ""


def get_anlu_changes(nl_file: NLFile, lockfile: Lockfile) -> list[ANLUChange]:
    """
    Compare current NL file against lockfile to detect changes.

    Args:
        nl_file: Current parsed NL file
        lockfile: Previous lockfile from last compile

    Returns:
        List of ANLUChange objects describing each ANLU's status
    """
    changes = []

    # Get current ANLU identifiers and their hashes
    current_anlus = {anlu.identifier: anlu for anlu in nl_file.anlus}

    # Get previous ANLU hashes from lockfile
    previous_hashes = {}
    if lockfile:
        # Check for anlus attribute (added by read_lockfile)
        if hasattr(lockfile, "anlus") and lockfile.anlus:
            for anlu_id, anlu_data in lockfile.anlus.items():
                if isinstance(anlu_data, dict):
                    previous_hashes[anlu_id] = anlu_data.get("source_hash", "")
        # Also check modules structure
        elif lockfile.modules:
            for mod_name, mod_lock in lockfile.modules.items():
                for anlu_id, anlu_lock in mod_lock.anlus.items():
                    previous_hashes[anlu_id] = anlu_lock.source_hash

    # Check each current ANLU
    for anlu_id, anlu in current_anlus.items():
        # Compute current hash using same function as lockfile
        current_hash = hash_anlu(anlu)

        if anlu_id not in previous_hashes:
            # New ANLU
            changes.append(ANLUChange(
                identifier=anlu_id,
                status="new",
                details="New ANLU added"
            ))
        elif previous_hashes[anlu_id] != current_hash:
            # Modified ANLU
            changes.append(ANLUChange(
                identifier=anlu_id,
                status="modified",
                details="Content changed"
            ))
        else:
            # Unchanged
            changes.append(ANLUChange(
                identifier=anlu_id,
                status="unchanged",
                details=""
            ))

    # Check for removed ANLUs
    for anlu_id in previous_hashes:
        if anlu_id not in current_anlus:
            changes.append(ANLUChange(
                identifier=anlu_id,
                status="removed",
                details="ANLU removed"
            ))

    return changes


def format_changes_output(changes: list[ANLUChange]) -> str:
    """
    Format changes for console output with colors.

    Args:
        changes: List of ANLUChange objects

    Returns:
        Formatted string for console output
    """
    if not changes:
        return "No ANLUs found."

    lines = []

    for change in sorted(changes, key=lambda c: c.identifier):
        if change.status == "unchanged":
            status_str = "  "  # No marker for unchanged
            line = f"[{change.identifier}] - unchanged"
        elif change.status == "modified":
            status_str = "M "
            line = f"[{change.identifier}] - modified"
        elif change.status == "new":
            status_str = "+ "
            line = f"[{change.identifier}] - new"
        elif change.status == "removed":
            status_str = "- "
            line = f"[{change.identifier}] - removed"
        else:
            status_str = "? "
            line = f"[{change.identifier}] - {change.status}"

        lines.append(line)

    return "\n".join(lines)


def format_stat_output(changes: list[ANLUChange]) -> str:
    """
    Format summary statistics for --stat output.

    Args:
        changes: List of ANLUChange objects

    Returns:
        Summary string with counts
    """
    counts = {
        "unchanged": 0,
        "modified": 0,
        "new": 0,
        "removed": 0,
    }

    for change in changes:
        counts[change.status] = counts.get(change.status, 0) + 1

    parts = []
    if counts["new"]:
        parts.append(f"{counts['new']} new")
    if counts["modified"]:
        parts.append(f"{counts['modified']} modified")
    if counts["removed"]:
        parts.append(f"{counts['removed']} removed")
    if counts["unchanged"]:
        parts.append(f"{counts['unchanged']} unchanged")

    if not parts:
        return "No changes"

    return ", ".join(parts)


def generate_full_diff(original_code: str, new_code: str, filename: str = "output.py") -> str:
    """
    Generate unified diff between original and new Python code.

    Args:
        original_code: Previous Python code
        new_code: New Python code
        filename: Filename for diff header

    Returns:
        Unified diff string
    """
    original_lines = original_code.splitlines(keepends=True)
    new_lines = new_code.splitlines(keepends=True)

    diff = difflib.unified_diff(
        original_lines,
        new_lines,
        fromfile=f"a/{filename}",
        tofile=f"b/{filename}",
    )

    result = "".join(diff)

    if not result:
        return "No changes in generated Python code."

    return result
