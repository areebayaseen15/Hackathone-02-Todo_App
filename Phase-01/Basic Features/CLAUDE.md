# Claude Code Instructions

This document provides instructions for Claude Code when working on the Todo Application project.

## Project Overview

This is the "Evolution of Todo" project - a multi-phase hackathon project that evolves from a simple console app to a distributed cloud-native AI system.

**Current Phase**: Phase I - In-Memory Python Console App

## Constitution Reference

All development must comply with `CONSTITUTION.md`. Key principles:

1. **Spec-Driven Development**: No code without approved specifications
2. **Development Hierarchy**: Constitution → Specs → Plan → Tasks → Implementation
3. **No Feature Invention**: Only implement what is specified
4. **Phase Isolation**: Do not introduce future phase concepts

## Phase I Constraints

The following are **STRICTLY FORBIDDEN** in Phase I:

- Database connections or queries
- File read/write operations
- Network/HTTP requests
- Authentication/authorization
- External package dependencies
- Web frameworks or APIs
- Multi-threading or async operations
- Any Phase II-V features

## Project Structure

```
todo-app/
├── CONSTITUTION.md      # Supreme governing document
├── CLAUDE.md            # This file
├── README.md            # User documentation
├── pyproject.toml       # UV project configuration
├── specs/               # Specification documents
│   ├── PHASE-I-SPEC.md  # What to build
│   ├── PHASE-I-PLAN.md  # How to build it
│   └── PHASE-I-TASKS.md # Task breakdown
└── src/todo/            # Source code
    ├── __init__.py      # Package marker
    ├── __main__.py      # python -m todo entry
    ├── main.py          # Application entry point
    ├── models.py        # Task dataclass
    ├── storage.py       # In-memory storage
    ├── services.py      # Business logic
    └── cli.py           # CLI interface
```

## Code Organization

### Layer Responsibilities

| Module | Responsibility |
|--------|----------------|
| `models.py` | Task data structure only |
| `storage.py` | In-memory list management, ID generation |
| `services.py` | Business validation, task operations |
| `cli.py` | User interaction, display, input handling |
| `main.py` | Dependency wiring, application startup |

### Layer Rules

1. CLI only calls services (never storage directly)
2. Services call storage for data operations
3. Models are shared across all layers
4. No circular dependencies

## Running the Application

```bash
# Using UV
uv run todo

# Using Python module
uv run python -m todo
```

## Development Commands

```bash
# Sync dependencies
uv sync

# Run the application
uv run todo

# Check Python version
python --version  # Must be 3.13+
```

## Specification Documents

Before making changes, consult:

1. `CONSTITUTION.md` - Supreme rules
2. `specs/PHASE-I-SPEC.md` - Feature requirements
3. `specs/PHASE-I-PLAN.md` - Technical approach
4. `specs/PHASE-I-TASKS.md` - Implementation tasks

## Change Protocol

1. Verify change aligns with specification
2. Check Constitution compliance
3. Update specification if requirements change
4. Implement following the plan
5. Validate against acceptance criteria

## Error Handling

- Display user-friendly messages
- Never show stack traces to users
- Validate at service layer
- Use `ValidationError` for input errors
- Return `None` for not-found cases

## Testing Approach

Phase I uses manual testing via the CLI. Test scenarios are defined in `specs/PHASE-I-SPEC.md` Section 9.

Key test cases:
- Add task with valid/invalid input
- View empty and populated task lists
- Update with partial changes
- Delete with confirmation/cancellation
- Toggle status both directions
