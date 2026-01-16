# CLAUDE.md - Agent Instructions for NLS

## Project Overview

NLS (Natural Language Source) is a compiler that translates `.nl` specification files written in plain English into executable Python code.

## Workflow: GitHub as Persistent Memory

**This project uses GitHub as its persistent memory bank across all coding sessions.**

### First Actions for Any Session

```bash
# 1. Check current issues and state
gh issue list --state open

# 2. Check current branch and status
git status && git branch

# 3. Find what to work on
gh issue list --label "in-progress"

# 4. If no in-progress, pick from backlog
gh issue list --label "ready"
```

### State Management

| State | Where It Lives |
|-------|----------------|
| **Tasks/Todos** | GitHub Issues with labels |
| **Ideas/Research** | GitHub Issues labeled `research` or `idea` |
| **Progress Tracking** | Issue comments + PR descriptions |
| **Architecture Decisions** | GitHub Wiki or issue discussions |
| **Session Handoff** | Close/update issues, push commits |

### Issue Labels

- `enhancement` — New features
- `bug` — Defects
- `research` — Investigation needed
- `idea` — Not yet scoped
- `in-progress` — Currently being worked on
- `ready` — Scoped and ready to implement
- `blocked` — Waiting on something

### TDD Discipline

**Always TDD. No exceptions.**

```bash
# 1. Create failing test (RED)
# 2. Run tests - confirm failure
pytest tests/test_X.py -v

# 3. Implement minimum to pass (GREEN)
# 4. Run tests - confirm pass
pytest tests/test_X.py -v

# 5. Refactor if needed
# 6. Commit with issue reference
git add . && git commit -m "feat(component): description

Refs #123"

# 7. Push and update issue
git push && gh issue comment 123 --body "Implemented in commit $(git rev-parse --short HEAD)"
```

### Session End Protocol

```bash
# 1. Commit all work
git add . && git commit -m "wip: session checkpoint"

# 2. Push to remote
git push

# 3. Update any in-progress issues with status
gh issue comment <number> --body "Session end: [summary of progress]"

# 4. If blocked, add blocked label
gh issue edit <number> --add-label "blocked" --body "Blocked on: [reason]"
```

---

## Commands

```bash
# Install in development mode
pip install -e .[dev]

# Run tests (use Python 3.12 on this system)
pytest tests/ -v

# Compile .nl file
nlsc compile examples/math.nl

# Verify syntax
nlsc verify examples/math.nl

# Initialize new project
nlsc init <path>
```

## Architecture

- `nlsc/parser.py` — Parses .nl files into AST
- `nlsc/resolver.py` — Validates dependencies
- `nlsc/emitter.py` — Generates Python (mock mode)
- `nlsc/lockfile.py` — Determinism via hashing
- `nlsc/schema.py` — Data structures (ANLU, TypeDefinition, etc.)

## Current Work

Check GitHub Issues: https://github.com/Mnehmos/mnehmos.nls.lang/issues

## Key Principles

1. _"The .nl file is the source. The .py file is the artifact."_
2. _"GitHub is the memory. The agent is the hands."_
3. _"TDD or it didn't happen."_
