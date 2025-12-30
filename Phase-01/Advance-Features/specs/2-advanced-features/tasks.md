# Tasks: Advanced Todo Features (Recurring Tasks & Due Dates)

**Feature**: Advanced Todo Features
**Branch**: `2-advanced-features`
**Plan**: `specs/2-advanced-features/plan.md`
**Date**: 2025-12-30

## Summary

Implementation of recurring tasks (daily/weekly/monthly) with automatic next occurrence creation, and due dates with validation and overdue detection. Analytics and smart views excluded per user's `/sp.plan` request (separate phase).

---

## Dependencies

### Story Dependencies

| Story | Dependent On |
|--------|---------------|
| None | Foundation - no dependencies |

All user stories are independent - no story blocks another.

---

## Phase 1: Setup

**Goal**: Extend data model with Recurrence enum and new Task fields.

- [X] T001 Add Recurrence enum to src/todo/models.py
- [X] T002 Extend Task dataclass with due_date, recurrence, parent_task_id fields
- [X] T003 Add utility functions (format_due_date, is_overdue, get_days_overdue, calculate_next_due_date)
- [X] T004 Update ensure_task_compatibility() with new attribute defaults

---

## Phase 2: Foundation - Service Layer

**Goal**: Add validation and business logic for due dates and recurrence.

- [X] T005 Add validate_due_date() function to src/todo/services.py
- [X] T006 Add validate_recurrence() function to src/todo/services.py

---

## Phase 3: User Story 1 - Recurring Tasks

**Goal**: Users can set tasks to repeat with automatic next occurrence creation.

**Independent Test**: Create recurring task, mark complete, verify next occurrence auto-created with parent_task_id reference.

- [X] T007 [US1] Extend add_task() to accept due_date_str and recurrence_str parameters
- [X] T008 [US1] Extend add_task() to call validation functions and create Task with new fields
- [X] T009 [US1] Extend toggle_task() to check for recurrence and due_date
- [X] T010 [US1] Extend toggle_task() to calculate next due date using calculate_next_due_date()
- [X] T011 [US1] Extend toggle_task() to create next occurrence task with parent_task_id
- [X] T012 [US1] Extend toggle_task() to return tuple (original_task, next_task_or_none)
- [ ] T013 [US1] Test: Create daily recurring task and verify next occurrence created
- [ ] T014 [US1] Test: Create weekly recurring task and verify next occurrence created
- [ ] T015 [US1] Test: Create monthly recurring task and verify next occurrence created
- [ ] T016 [US1] Test: Complete recurring task and verify parent_task_id set on new occurrence
- [ ] T017 [US1] Test: Recurring task without due date does not create next occurrence
- [ ] T018 [US1] Test: Monthly recurrence from Jan 31 goes to Feb 28/29 (leap year check)

---

## Phase 4: User Story 2 - Due Dates & Deadlines

**Goal**: Users can assign due dates with validation, view overdue indicators.

**Independent Test**: Create task with due date, view task list, verify overdue/TODAY indicators shown.

- [X] T019 [US2] Extend update_task() to accept due_date_str parameter
- [X] T020 [US2] Extend update_task() to validate and update due_date field (allow None for removal)
- [ ] T021 [US2] Test: Create task with valid date format (YYYY-MM-DD)
- [ ] T022 [US2] Test: Create task with invalid date format (12/30/2025) - verify error
- [ ] T023 [US2] Test: Create task with invalid calendar date (2025-02-31) - verify error
- [ ] T024 [US2] Test: Create task with leap year date (2024-02-29) - verify success
- [ ] T025 [US2] Test: Create task with non-leap year date (2025-02-29) - verify error
- [ ] T026 [US2] Test: Update task due date to new value
- [ ] T027 [US2] Test: Update task to remove due date (press Enter)
- [ ] T028 [US2] Test: Create task with past due date - verify accepted

---

## Phase 5: CLI Layer Integration

**Goal**: Update CLI prompts and display to support due dates and recurrence.

- [X] T029 Add format_due_date, is_overdue imports to src/todo/cli.py
- [X] T030 Extend add_task() CLI to prompt for due date (optional, YYYY-MM-DD)
- [X] T031 Extend add_task() CLI to prompt for recurrence (optional, none/daily/weekly/monthly)
- [X] T032 Extend add_task() CLI success display to show due date and recurrence
- [X] T033 Extend update_task() CLI to show current due date and recurrence
- [X] T034 Extend update_task() CLI to prompt for new due date (optional, keep current with Enter)
- [X] T035 Extend update_task() CLI to prompt for new recurrence (optional, keep current with Enter)
- [X] T036 Extend update_task() CLI success display to show updated due date and recurrence
- [X] T037 Extend toggle_task() CLI to detect recurring task completion (next_task not None)
- [X] T038 Extend toggle_task() CLI to display next occurrence info (new task ID, due date, parent_task_id)
- [X] T039 Extend toggle_task() CLI to display original and next occurrence details
- [X] T040 Extend display_task_list() to show due date column
- [X] T041 Extend display_task_list() to show OVERDUE indicator in status column for overdue pending tasks
- [X] T042 Extend display_task_list() to show TODAY for tasks due today
- [X] T043 Extend display_task_list() to show "No due date" for tasks without due date
- [X] T044 Extend display_task_list() to show overdue count in summary line

---

## Phase 6: Backward Compatibility

**Goal**: Ensure existing tasks from Intermediate Phase still work.

- [X] T045 Verify ensure_task_compatibility() is called in get_all_tasks()
- [X] T046 Verify ensure_task_compatibility() is called in get_task()
- [ ] T047 Test: Run app with existing Intermediate Phase tasks - verify defaults applied

---

## Phase 7: Integration Testing

**Goal**: Verify all features work together end-to-end.

- [ ] T048 Test: Create task with due date and recurrence, view in task list
- [ ] T049 Test: Complete recurring task, verify next appears in list
- [ ] T050 Test: View task list with overdue task - verify OVERDUE shown
- [ ] T051 Test: View task list with today's task - verify TODAY shown
- [ ] T052 Test: View task list with mixed due dates (past, today, future, none)
- [ ] T053 Test: Update task due date from None to date
- [ ] T054 Test: Update task recurrence from NONE to WEEKLY
- [ ] T055 Test: Delete original recurring task - verify child task still exists

---

## Phase 8: Polish

**Goal**: Finalize implementation with cleanup and validation.

- [ ] T056 Review all code for PEP 8 compliance
- [ ] T057 Add docstrings to all new functions
- [ ] T058 Verify all console output matches spec examples
- [ ] T059 Run complete manual test scenario from quickstart.md

---

## Total Tasks

**Count**: 59 tasks

**By Story**:
- Setup: 4 tasks
- Service Layer Foundation: 2 tasks
- User Story 1 (Recurring Tasks): 12 tasks
- User Story 2 (Due Dates): 10 tasks
- CLI Layer: 16 tasks
- Backward Compatibility: 3 tasks
- Integration Testing: 8 tasks
- Polish: 4 tasks

---

## Parallel Execution Opportunities

The following tasks can be executed in parallel (different files, no dependencies on incomplete tasks):

### Parallel Group 1: Service Layer Validation (T005, T006)
- Both functions in same file (services.py)
- No dependencies between them
- Can implement simultaneously

### Parallel Group 2: CLI Display Updates (T040-T044)
- All in same file (cli.py)
- Independent updates to display_task_list()
- Can implement simultaneously

### Parallel Group 3: CLI Task Operations (T029-T039)
- All in same file (cli.py)
- Different functions but no blocking dependencies
- Can implement in small batches

---

## Implementation Strategy

**MVP First** (Minimum Viable Product):
- Start with User Story 2 (Due Dates) - simpler, enables task tracking
- Then implement User Story 1 (Recurring Tasks) - builds on due date foundation

**Incremental Delivery**:
- After each Phase: Run app, test features manually, validate against spec
- Stop and fix issues before proceeding to next phase

**Testing Approach**:
- Manual testing per Phase I constraints (no automated tests)
- Use quickstart.md scenarios as test checklist
- Verify each feature independently before integration

---

## Format Validation

✅ All tasks follow checklist format:
- Each task starts with `- [ ]` (checkbox)
- Task ID is sequential (T001-T059)
- User story tasks include [US1], [US2] labels
- All tasks include specific file paths
- No unresolved placeholders

---

**Next Steps**:
1. Execute Phase 1 (Setup) - T001-T004
2. Execute Phase 2 (Service Foundation) - T005-T006
3. Execute Phase 3 (US1 - Recurring Tasks) - T007-T018
4. Execute Phase 4 (US2 - Due Dates) - T019-T028
5. Execute Phase 5 (CLI Integration) - T029-T044
6. Execute Phase 6 (Backward Compatibility) - T045-T047
7. Execute Phase 7 (Integration Testing) - T048-T055
8. Execute Phase 8 (Polish) - T056-T059
