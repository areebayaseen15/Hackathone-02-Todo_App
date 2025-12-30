# Research: Advanced Todo Features

**Feature**: Advanced Todo Features (Recurring Tasks & Due Dates)
**Branch**: `2-advanced-features`
**Date**: 2025-12-30

## Overview

This document consolidates research findings for implementing recurring tasks and due dates in the Phase I Todo App. Research covers date validation, recurrence calculation, leap year handling, and month-end edge cases.

---

## Date Validation

### Decision: Use Python's built-in `datetime` module

**Rationale**: Python's `datetime` module is part of the standard library (no external dependencies), provides robust date validation including calendar correctness, and handles leap years automatically. Using standard library maintains Phase I constraints.

**Alternatives Considered**:
1. **Manual string parsing**: More error-prone, requires manual leap year logic
2. **External libraries (dateutil, arrow)**: Violates Phase I constraint (no external packages)
3. **Custom regex-only validation**: Doesn't catch calendar-invalid dates (e.g., Feb 31)

### Implementation Approach

```python
from datetime import datetime

def validate_due_date(date_str: str) -> Optional[datetime]:
    """Parse and validate due date string."""
    cleaned = date_str.strip()

    if not cleaned:
        return None

    # Validate format: YYYY-MM-DD
    if len(cleaned) != 10 or cleaned[4] != '-' or cleaned[7] != '-':
        raise ValueError(f"Invalid date format. Use YYYY-MM-DD. Got: '{date_str}'")

    try:
        year = int(cleaned[0:4])
        month = int(cleaned[5:7])
        day = int(cleaned[8:10])

        # Create datetime - automatically validates calendar date
        return datetime(year, month, day)

    except ValueError as e:
        raise ValueError(f"Invalid date: '{date_str}'. {str(e)}")
```

**Key Features**:
- `datetime(year, month, day)` raises `ValueError` for invalid calendar dates
- Automatically handles leap years (Feb 29 valid only in leap years)
- Empty string returns `None` (no due date)

---

## Recurrence Calculation

### Decision: Simple incremental calculation with month-end edge case handling

**Rationale**: Straightforward approach using `timedelta` for daily/weekly recurrence. Monthly recurrence requires special handling for month-end edge cases (e.g., Jan 31 → Feb 28). No need for complex scheduling libraries since we only create next occurrence, not future schedule.

**Alternatives Considered**:
1. **Full scheduler (cron-like)**: Over-engineering for this use case
2. **Business days only**: Not required by specification
3. **Date-only vs date+time**: Specification specifies date-only (time = midnight)

### Implementation Approach

```python
from datetime import timedelta

def calculate_next_due_date(current_date: datetime, recurrence: Recurrence) -> datetime:
    """Calculate next due date based on recurrence pattern."""
    if recurrence == Recurrence.NONE:
        raise ValueError("Cannot calculate next date for non-recurring task")

    if recurrence == Recurrence.DAILY:
        return current_date + timedelta(days=1)

    if recurrence == Recurrence.WEEKLY:
        return current_date + timedelta(weeks=1)

    if recurrence == Recurrence.MONTHLY:
        # Handle month-end edge cases (e.g., Jan 31 → Feb 28/29)
        year = current_date.year
        month = current_date.month + 1

        if month > 12:
            month = 1
            year += 1

        day = current_date.day

        # Get last day of target month
        last_day = (datetime(year, month + 1, 1) - timedelta(days=1)).day

        # Use min(day, last_day) to handle non-existent days
        return datetime(year, month, min(day, last_day))

    raise ValueError(f"Unknown recurrence: {recurrence}")
```

**Key Features**:
- Daily: `+timedelta(days=1)` - simple increment
- Weekly: `+timedelta(weeks=1)` - simple increment
- Monthly: Special handling for month-end (Jan 31 → last day of February)
- Month-end logic: `min(day, last_day)` ensures valid date

---

## Leap Year Handling

### Decision: Rely on Python's `datetime` module

**Rationale**: Python's `datetime` correctly implements Gregorian calendar leap year rules:
- Divisible by 4 → leap year
- Except if divisible by 100
- Unless also divisible by 400

This means:
- 2000: Divisible by 400 → **leap year** (Feb 29 valid)
- 2100: Divisible by 100 but not 400 → **not leap year** (Feb 29 invalid)
- 2024: Divisible by 4 → **leap year** (Feb 29 valid)
- 2025: Not divisible by 4 → **not leap year** (Feb 29 invalid)

**Alternatives Considered**:
1. **Manual leap year calculation**: Reimplementing existing functionality
2. **Custom calendar library**: Unnecessary complexity

### Test Cases Validated

| Date | Expected Result | Why |
|------|-----------------|------|
| 2024-02-29 | Valid | 2024 divisible by 4 → leap year |
| 2025-02-29 | Invalid | 2025 not divisible by 4 → not leap year |
| 2000-02-29 | Valid | 2000 divisible by 400 → leap year |
| 1900-02-29 | Invalid | 1900 divisible by 100, not 400 → not leap year |
| 2024-02-28 | Valid | Valid date in leap year |
| 2024-01-31 | Valid | January always has 31 days |
| 2025-02-31 | Invalid | February max 29 (leap) or 28 (non-leap) |
| 2025-04-31 | Invalid | April has 30 days |

---

## Month-End Edge Cases for Monthly Recurrence

### Decision: Last-day-of-month fallback

**Rationale**: When a monthly recurring task is due on the 31st and the next month has fewer days (e.g., February), the specification requires moving to the last valid day (Feb 28 or 29). Using `min(day, last_day)` implements this cleanly.

**Examples**:

| Current Due Date | Next Due Date | Calculation |
|----------------|----------------|-------------|
| 2025-01-31 | 2025-02-28 | Jan 31 → Feb has max 28 days (2025 not leap year) |
| 2024-01-31 | 2024-02-29 | Jan 31 → Feb has max 29 days (2024 is leap year) |
| 2025-03-31 | 2025-04-30 | Mar 31 → Apr has max 30 days |
| 2025-05-31 | 2025-06-30 | May 31 → Jun has max 30 days |
| 2025-07-31 | 2025-07-31 | Jul 31 → Jul has 31 days (stays 31) |
| 2025-01-15 | 2025-02-15 | Jan 15 → Feb has 15 days (stays 15) |

### Algorithm

```python
# Get last day of target month
last_day = (datetime(year, month + 1, 1) - timedelta(days=1)).day

# Use minimum of requested day or last available day
day = min(current_date.day, last_day)
```

**Explanation**:
- `datetime(year, month + 1, 1)` = first day of next month
- Subtract 1 day = last day of current month
- `min(day, last_day)` ensures we don't exceed month length

---

## Backward Compatibility

### Decision: Runtime attribute checking with default values

**Rationale**: Tasks created before this feature will lack new attributes (`due_date`, `recurrence`, `parent_task_id`). Checking `hasattr()` and setting defaults ensures existing code doesn't break. This is session-based only (in-memory), so no database migration needed.

**Alternatives Considered**:
1. **Versioned Task objects**: Over-engineering for Phase I
2. **Full data migration script**: Not needed for in-memory storage

### Implementation Approach

```python
def ensure_task_compatibility(task: Task) -> Task:
    """Ensure task has all required attributes."""
    # Intermediate phase attributes
    if not hasattr(task, 'priority'):
        task.priority = Priority.MEDIUM
    if not hasattr(task, 'category'):
        task.category = None

    # Advanced phase attributes
    if not hasattr(task, 'due_date'):
        task.due_date = None
    if not hasattr(task, 'recurrence'):
        task.recurrence = Recurrence.NONE
    if not hasattr(task, 'parent_task_id'):
        task.parent_task_id = None

    return task
```

**Where to Call**:
- In `get_all_tasks()` - all tasks
- In `get_task(task_id)` - single task retrieval
- Before any display or operation on task

---

## Data Model Extension Strategy

### Decision: Add optional fields to existing Task dataclass

**Rationale**: Cleanest approach maintains existing code unchanged. Optional fields with defaults ensure backward compatibility. No breaking changes to existing task IDs or structure.

**New Fields**:
```python
@dataclass
class Task:
    # ... existing fields ...
    due_date: Optional[datetime] = None
    recurrence: Recurrence = Recurrence.NONE
    parent_task_id: Optional[int] = None
```

**Alternatives Considered**:
1. **New RecurringTask subclass**: Unnecessary complexity
2. **Composition (Task + RecurrenceInfo)**: Over-engineering
3. **Versioned Task**: Not needed for in-memory

---

## CLI Display Formatting

### Decision: Enhanced table display with conditional columns

**Rationale**: Maintain existing table format while adding new columns. Display "TODAY" and "OVERDUE" as inline indicators for clarity.

**Table Structure**:

```
ID    | Priority | Due Date    | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | 2025-12-28  | [X] OVERDUE  | Pay electricity bill           | 2025-12-25 09:00:00
2     | MEDIUM   | TODAY       | [ ]          | Call dentist                   | 2025-12-30 10:30:00
3     | LOW      | No due date | [X]          | Buy groceries                  | 2025-12-30 12:00:00
```

**Status Column Logic**:
- Base: `[X]` if completed, `[ ]` if pending
- Enhancement: Append ` OVERDUE` if pending and `due_date < today`

**Due Date Column Logic**:
- `due_date == today` → Display "TODAY"
- `due_date is None` → Display "No due date"
- `due_date < today` → Display date (with OVERDUE in status column)
- `due_date > today` → Display date normally

---

## Performance Considerations

### In-Memory Performance

| Operation | Target | Implementation |
|------------|---------|----------------|
| Date validation | <1ms | Single datetime constructor call |
| Recurrence calculation | <1ms | Simple arithmetic, max 1 datetime call |
| Task toggle with auto-creation | <100ms | Retrieval + calculation + storage.add() |
| Task list display (200 tasks) | <500ms | Single iteration + formatting |

**Conclusion**: In-memory storage ensures all operations are fast. No optimization needed for Phase I scope (≤200 tasks).

---

## Summary of Decisions

| Aspect | Decision | Justification |
|---------|----------|---------------|
| Date validation | Python `datetime` module | Standard library, built-in calendar validation, leap year handling |
| Recurrence calculation | Incremental with month-end handling | Simple, meets spec, handles edge cases |
| Leap year handling | Python `datetime` automatic | Correct Gregorian calendar implementation |
| Month-end edge cases | `min(day, last_day)` | Spec requires last-day fallback |
| Backward compatibility | `hasattr()` + defaults | Clean, no breaking changes |
| Data model extension | Optional fields to existing Task | Minimal change, maintains structure |
| CLI display | Enhanced table with conditionals | Clear, maintains existing format |

All technical unknowns resolved. No Phase 0 research agents needed - standard library solutions sufficient.
