# Implementation Plan: Advanced Todo Features

**Branch**: `2-advanced-features` | **Date**: 2025-12-30 | **Spec**: `specs/2-advanced-features/spec.md`

**Input**: Feature specification from `/specs/2-advanced-features/spec.md`

**Note**: This template is filled in by `/sp.plan` command. See `.specify/templates/commands/plan.md` for execution workflow.

## Summary

Implement recurring tasks (daily/weekly/monthly) with automatic next occurrence creation upon completion, and due dates with validation, overdue detection, and time-aware display. Scope limited to in-memory Python console app with backward compatibility for existing tasks. Exclude analytics and smart views from this implementation.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: datetime (standard library), typing (standard library), dataclasses (standard library)
**Storage**: In-memory list (`TaskStorage` class - no database, no file persistence)
**Testing**: Manual console testing (per Phase I constraints)
**Target Platform**: CLI (console-based, no GUI)
**Project Type**: Single (monolithic Python package)
**Performance Goals**: <100ms for recurring task auto-creation, <500ms for task list display
**Constraints**: Phase I - no persistence, no external packages, no network/HTTP
**Scale/Scope**: Up to 200 tasks in memory per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Constitution Principle | Status | Justification |
|---------------------|--------|---------------|
| Spec-Driven Development | PASS | Following approved spec from `/specs/2-advanced-features/spec.md` |
| Phase Isolation | PASS | Only implementing recurring tasks and due dates (Phase I scope) |
| Technology Constraints | PASS | Using standard library only (datetime, typing, dataclasses) |
| Clean Architecture | PASS | Maintaining separation: models, services, CLI layers |
| No Breaking Changes | PASS | Extending Task dataclass with new optional fields |

## Project Structure

### Documentation (this feature)

```text
specs/2-advanced-features/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
└── contracts/           # Phase 1 output (/sp.plan command)
    ├── add-recurring-task.md
    ├── toggle-recurring-task.md
    ├── view-analytics.md      # Not implementing in this phase
    └── smart-views.md       # Not implementing in this phase
```

### Source Code (repository root)

```text
src/todo/
├── __init__.py           # Package marker
├── models.py             # Task dataclass with new fields (due_date, recurrence, parent_task_id)
├── storage.py            # In-memory storage (unchanged)
├── services.py           # Business logic extensions for due dates and recurrence
├── cli.py                # CLI interface updates (no analytics/smart views yet)
├── __main__.py           # Module entry point (unchanged)
└── main.py              # Application entry point (unchanged)

tests/
└── manual/               # Manual testing scenarios (not automated - Phase I constraint)
```

**Structure Decision**: Single project layout with extended existing modules. New fields added to existing Task dataclass in `models.py`. Service layer extended with validation and recurrence logic in `services.py`. CLI layer updated with prompts for due date and recurrence in `cli.py`. No new modules required - clean extension approach.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|--------------|-----------------------------------|
| None | N/A | N/A - all requirements within constraints |
