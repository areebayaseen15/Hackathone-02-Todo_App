---
id: 2
title: Advanced features recurring tasks dates tasks
stage: tasks
date: 2025-12-30T14:10:00Z
surface: cli
model: sonnet-4-5-20250929
feature: 2-advanced-features
branch: 2-advanced-features
user: /sp.tasks
command: /sp.tasks
labels: [spec-driven, phase-i, recurring-tasks, due-dates, task-breakdown]
links:
  spec: specs/2-advanced-features/spec.md
  plan: specs/2-advanced-features/plan.md
  tasks: specs/2-advanced-features/tasks.md
files:
  - path: specs/2-advanced-features/tasks.md
    kind: created
tests: []
---

## Prompt

$ARGUMENTS

From Advanced Phase plan:
- Break down work into small, executable tasks
- Map tasks to existing modules
- Avoid any persistence mechanism

---

## Response snapshot

Generated tasks.md with 59 tasks organized into 8 phases:

**Phase 1: Setup** (4 tasks)
- T001: Add Recurrence enum to src/todo/models.py
- T002: Extend Task dataclass with new fields
- T003: Add utility functions
- T004: Update ensure_task_compatibility()

**Phase 2: Foundation - Service Layer** (2 tasks)
- T005: Add validate_due_date() function
- T006: Add validate_recurrence() function

**Phase 3: User Story 1 - Recurring Tasks** (12 tasks)
- T007-T012: Extend add_task() and toggle_task() with recurrence logic
- T013-T018: Manual tests for all recurrence scenarios

**Phase 4: User Story 2 - Due Dates** (10 tasks)
- T019-T028: Extend update_task() with due date handling
- Manual tests for date validation, overdue detection

**Phase 5: CLI Layer Integration** (16 tasks)
- T029-T044: Update CLI prompts and display for due dates and recurrence

**Phase 6: Backward Compatibility** (3 tasks)
- T045-T047: Verify existing tasks work with new fields

**Phase 7: Integration Testing** (8 tasks)
- T048-T055: End-to-end testing

**Phase 8: Polish** (4 tasks)
- T056-T059: Code review and cleanup

**Total**: 59 tasks

**Parallel Opportunities**:
- Service validation functions (T005, T006) - can be done in parallel
- CLI display updates (T040-T044) - many in same file

**Scope**: Analytics and smart views excluded per user's /sp.plan request.

---

## Outcome

- Impact: Complete task breakdown for recurring tasks and due dates implementation. Ready for execution by Claude Code.
- Files: tasks.md created with 59 tasks organized by phase and user story.
- Next prompts: /sp.implement to execute the task breakdown.
- Reflection: Tasks organized by user story (US1 for recurring, US2 for due dates) enabling independent implementation and testing. Excluded US3 (analytics) and US4 (smart views) per user's reduced scope request.

---

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Execute /sp.implement
