# Contract: Toggle Recurring Task (Complete and Create Next)

**Feature**: Advanced Todo Features
**Contract ID**: ADV-002
**Date**: 2025-12-30

## Purpose

Define the contract for toggling task completion status with automatic next occurrence creation for recurring tasks.

## Actors

- **User**: Interacts with the CLI to complete/uncomplete tasks
- **CLI**: Collects task ID and displays results
- **Service**: Contains business logic for toggling and auto-creation
- **Storage**: Manages in-memory task storage

## Pre-Conditions

1. Application is running
2. User has selected "Mark Task as Complete/Incomplete" from main menu
3. At least one task exists in storage

## Input Specification

### Input Fields

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `task_id` | Integer | Yes | Must be positive integer, must reference existing task |

### Input Flow

```
================================================================================
                          TOGGLE TASK
================================================================================
Enter task ID to toggle status: [User input - required]
```

## Processing

### Step 1: Validate and Retrieve Task
- Parse task_id as integer
- Check if positive → Error: "Task ID must be a positive number"
- Call `storage.get_by_id(task_id)`
- Not found → Error: "Task with ID {task_id} not found"
- Return task object

### Step 2: Ensure Task Compatibility
- Call `ensure_task_compatibility(task)`
- Set default values for missing attributes (due_date, recurrence, parent_task_id)

### Step 3: Toggle Completion Status
- Toggle `task.is_completed` (True ↔ False)

### Step 4: Check for Recurring Task Completion
- **If toggling to incomplete**:
  - No next occurrence creation
  - Store and return task
- **If toggling to complete AND task has recurrence != NONE AND task has due_date**:
  - **Proceed to Step 5 for auto-creation**
- **Otherwise**:
  - Store and return task (no auto-creation)

### Step 5: Calculate Next Due Date
```python
if task.recurrence == Recurrence.DAILY:
    next_date = task.due_date + timedelta(days=1)
elif task.recurrence == Recurrence.WEEKLY:
    next_date = task.due_date + timedelta(weeks=1)
elif task.recurrence == Recurrence.MONTHLY:
    # Handle month-end edge cases (e.g., Jan 31 → Feb 28/29)
    year = task.due_date.year
    month = task.due_date.month + 1
    if month > 12:
        month = 1
        year += 1
    day = task.due_date.day
    last_day = (datetime(year, month + 1, 1) - timedelta(days=1)).day
    next_date = datetime(year, month, min(day, last_day))
```

### Step 6: Create Next Occurrence Task
```python
next_task = Task(
    id=0,  # Will be assigned by storage
    title=task.title,
    description=task.description,
    is_completed=False,
    created_at=datetime.now(),
    priority=task.priority,
    category=task.category,
    due_date=next_date,
    recurrence=task.recurrence,
    parent_task_id=task.id
)
```

### Step 7: Store Both Tasks
- Call `storage.update(task)` to update original task
- Call `storage.add(next_task)` to create next occurrence
- Storage assigns auto-generated ID to next_task
- Return both tasks

## Output Specification

### Success Response - Non-Recurring Task (or Recurring without Due Date)

```
================================================================================
Task status updated!
ID: {task_id}
Title: {title}
Status: [X] completed (or [ ] pending)
================================================================================
Press Enter to continue...
```

### Success Response - Recurring Task with Auto-Creation

```
================================================================================
Task completed! Next occurrence created.
New task ID: {new_task_id}
Next due date: {YYYY-MM-DD}

Original Task:
ID: {original_id}
Title: {title}
Recurrence: {RECURRENCE}
Due Date: {YYYY-MM-DD}
Status: [X] completed

Next Occurrence:
ID: {new_task_id}
Title: {title}
Recurrence: {RECURRENCE}
Due Date: {YYYY-MM-DD}
Status: [ ] pending
Parent Task ID: {original_id}
================================================================================
Press Enter to continue...
```

### Error Response

```
================================================================================
Error: {error_message}
================================================================================
Press Enter to continue...
```

## Post-Conditions

1. Original task completion status is toggled
2. For recurring tasks with due dates: new occurrence is created
3. New occurrence references original task via parent_task_id
4. Both tasks are stored in memory
5. Original task remains in storage (not deleted)

## Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| Task not found | Error message: "Task with ID {id} not found" |
| Invalid task ID (not integer) | Error message: "Task ID must be a positive number" |
| Recurring task without due date | Task toggled, no auto-creation |
| Non-recurring task | Task toggled, no auto-creation |
| Toggling back to incomplete | Task toggled, no auto-creation |
| Monthly recurrence from Jan 31 | Next occurrence on Feb 28/29 |
| Leap year calculation | Handled correctly (Feb 29 valid only in leap years) |
| Task completed multiple times | Each completion creates new occurrence |

## Examples

### Example 1: Complete Daily Recurring Task

**Context**: Task ID 10 is a daily recurring task due on 2025-12-30

**Input**:
```
Enter task ID to toggle status: 10
```

**Output**:
```
================================================================================
Task completed! Next occurrence created.
New task ID: 11
Next due date: 2025-12-31

Original Task:
ID: 10
Title: Take medication
Recurrence: DAILY
Due Date: 2025-12-30
Status: [X] completed

Next Occurrence:
ID: 11
Title: Take medication
Recurrence: DAILY
Due Date: 2025-12-31
Status: [ ] pending
Parent Task ID: 10
================================================================================
Press Enter to continue...
```

### Example 2: Complete Weekly Recurring Task

**Context**: Task ID 10 is a weekly recurring task due on Monday, 2025-12-30

**Input**:
```
Enter task ID to toggle status: 10
```

**Output**:
```
================================================================================
Task completed! Next occurrence created.
New task ID: 11
Next due date: 2026-01-05

Original Task:
ID: 10
Title: Weekly team meeting
Recurrence: WEEKLY
Due Date: 2025-12-30
Status: [X] completed

Next Occurrence:
ID: 11
Title: Weekly team meeting
Recurrence: WEEKLY
Due Date: 2026-01-05
Status: [ ] pending
Parent Task ID: 10
================================================================================
Press Enter to continue...
```

### Example 3: Complete Monthly Recurring Task (End of Month)

**Context**: Task ID 10 is a monthly recurring task due on Jan 31, 2025

**Input**:
```
Enter task ID to toggle status: 10
```

**Output**:
```
================================================================================
Task completed! Next occurrence created.
New task ID: 11
Next due date: 2025-02-28

Original Task:
ID: 10
Title: Pay rent
Recurrence: MONTHLY
Due Date: 2025-01-31
Status: [X] completed

Next Occurrence:
ID: 11
Title: Pay rent
Recurrence: MONTHLY
Due Date: 2025-02-28
Status: [ ] pending
Parent Task ID: 10
================================================================================
Press Enter to continue...
```

### Example 4: Complete Monthly Recurring Task (Leap Year)

**Context**: Task ID 10 is a monthly recurring task due on Jan 31, 2024 (leap year)

**Input**:
```
Enter task ID to toggle status: 10
```

**Output**:
```
================================================================================
Task completed! Next occurrence created.
New task ID: 11
Next due date: 2024-02-29

Original Task:
ID: 10
Title: Monthly report
Recurrence: MONTHLY
Due Date: 2024-01-31
Status: [X] completed

Next Occurrence:
ID: 11
Title: Monthly report
Recurrence: MONTHLY
Due Date: 2024-02-29
Status: [ ] pending
Parent Task ID: 10
================================================================================
Press Enter to continue...
```

### Example 5: Complete Non-Recurring Task

**Input**:
```
Enter task ID to toggle status: 5
```

**Output**:
```
================================================================================
Task status updated!
ID: 5
Title: Buy groceries
Status: [X] completed
================================================================================
Press Enter to continue...
```

### Example 6: Recurring Task Without Due Date

**Context**: Task ID 10 has recurrence=weekly but no due_date

**Input**:
```
Enter task ID to toggle status: 10
```

**Output**:
```
================================================================================
Task status updated!
ID: 10
Title: Recurring task (no due date)
Recurrence: WEEKLY
Status: [X] completed
================================================================================
Press Enter to continue...
```

### Example 7: Task Not Found

**Input**:
```
Enter task ID to toggle status: 999
```

**Output**:
```
================================================================================
Error: Task with ID 999 not found
================================================================================
Press Enter to continue...
```

## Test Cases

### TC-001: Complete daily recurring task
- **Input**: Daily recurring task with due date
- **Expected**: Next occurrence due tomorrow (due_date + 1 day)

### TC-002: Complete weekly recurring task
- **Input**: Weekly recurring task with due date
- **Expected**: Next occurrence due in 7 days

### TC-003: Complete monthly recurring task (normal month)
- **Input**: Monthly recurring task due on 15th
- **Expected**: Next occurrence due on 15th of next month

### TC-004: Complete monthly recurring task (31st to 28th)
- **Input**: Monthly recurring task due on Jan 31
- **Expected**: Next occurrence due on Feb 28

### TC-005: Complete monthly recurring task (31st to 29th, leap year)
- **Input**: Monthly recurring task due on Jan 31, 2024
- **Expected**: Next occurrence due on Feb 29, 2024

### TC-006: Complete non-recurring task
- **Input**: Task with recurrence=none
- **Expected**: Task toggled, no auto-creation

### TC-007: Complete recurring task without due date
- **Input**: Recurring task with due_date=None
- **Expected**: Task toggled, no auto-creation

### TC-008: Toggle back to incomplete
- **Input**: Toggle completed task back to pending
- **Expected**: Task toggled, no auto-creation

### TC-009: Invalid task ID
- **Input**: Task ID 999 (doesn't exist)
- **Expected**: Error message, no changes

### TC-010: Non-integer task ID
- **Input**: "abc" instead of number
- **Expected**: Error message, no changes

### TC-011: Multiple completions
- **Input**: Complete task, complete again (toggle off), complete again
- **Expected**: Each completion creates new occurrence if conditions met

### TC-012: Verify parent_task_id is set
- **Input**: Complete recurring task
- **Expected**: New occurrence has parent_task_id = original task id
