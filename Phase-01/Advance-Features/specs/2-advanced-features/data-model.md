# Data Model: Advanced Todo Features (Recurring Tasks & Due Dates)

**Feature**: Advanced Todo Features
**Branch**: 2-advanced-features
**Date**: 2025-12-30

## Overview

This document defines data model changes required to add recurring tasks and due dates to Phase I Todo App. All changes maintain backward compatibility with existing Phase I and Intermediate task data.

---

## Entity: Task

### Modified Entity (Updated from Intermediate Phase)

**File**: `src/todo/models.py`

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class Priority(Enum):
    """Priority levels for tasks.

    Values are ordered from highest to lowest urgency.
    """
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Recurrence(Enum):
    """Recurrence patterns for tasks.

    Values indicate how often a task repeats.
    """
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier for task (auto-generated, positive integer)
        title: Short descriptive name of task (1-100 characters, required)
        description: Detailed description of task (0-500 characters, optional)
        is_completed: Completion status of task (default: False)
        created_at: Timestamp when task was created (auto-generated, immutable)
        priority: Priority level of task (HIGH/MEDIUM/LOW, default: MEDIUM)
        category: Optional category or tag for grouping (0-50 characters, optional)
        due_date: Optional due date or deadline (YYYY-MM-DD format, optional)
        recurrence: Recurrence pattern (NONE/DAILY/WEEKLY/MONTHLY, default: NONE)
        parent_task_id: Optional reference to originating task ID (for recurring chains)
    """

    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    priority: Priority = Priority.MEDIUM
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    recurrence: Recurrence = Recurrence.NONE
    parent_task_id: Optional[int] = None
```

### Field Specifications

| Field | Type | Default | Constraints | Description |
|-------|------|---------|-------------|
| `id` | `int` | Auto-generated | Positive integer, unique | Unique identifier |
| `title` | `str` | Required | 1-100 characters, non-empty | Short descriptive name |
| `description` | `str` | Empty string | 0-500 characters | Detailed description |
| `is_completed` | `bool` | `False` | Boolean only | Completion status |
| `created_at` | `datetime` | Auto-generated | Immutable | Creation timestamp |
| `priority` | `Priority` | `Priority.MEDIUM` | Enum: HIGH/MEDIUM/LOW | Priority level |
| `category` | `Optional[str]` | `None` | 0-50 characters, optional | Category tag |
| `due_date` | `Optional[datetime]` | `None` | YYYY-MM-DD format, optional | Due date |
| `recurrence` | `Recurrence` | `Recurrence.NONE` | Enum: NONE/DAILY/WEEKLY/MONTHLY | Recurrence pattern |
| `parent_task_id` | `Optional[int]` | `None` | References valid task ID, optional | Parent task reference |

### Field Validation Rules

#### Due Date Field
- **Type**: `Optional[datetime]` (datetime or `None`)
- **Default**: `None` (no due date)
- **Format**: YYYY-MM-DD (ISO 8601 date only, no time component)
- **Input Validation**:
  - Must match regex `^\d{4}-\d{2}-\d{2}$`
  - Must be valid calendar date
  - Must handle leap years correctly
  - Empty string after trim → `None`
  - Whitespace-only string → `None`
- **Date Validation**: Invalid dates (Feb 31, Apr 31) raise `ValueError`
- **Time Component**: Always midnight (00:00:00) for date-only input

#### Recurrence Field
- **Type**: Must be `Recurrence` enum value
- **Default**: `Recurrence.NONE` if not specified
- **Valid Values**: `Recurrence.NONE`, `Recurrence.DAILY`, `Recurrence.WEEKLY`, `Recurrence.MONTHLY`
- **Case-Insensitive Input**: User input "daily", "DAILY", "Daily" all map to `Recurrence.DAILY`
- **Validation**: Invalid values raise `ValueError`
- **Auto-Creation Logic**: Requires `due_date` to be set for automatic next occurrence creation

#### Parent Task ID Field
- **Type**: `Optional[int]` (integer or `None`)
- **Default**: `None` (no parent)
- **Purpose**: Tracks recurring task chains
- **Directionality**: Points backward (child → parent)
- **Constraint**: Must reference valid task ID if not `None`
- **Immutability**: Set once at creation, never changed

### Validation Functions

```python
def validate_due_date(date_str: str) -> Optional[datetime]:
    """Parse and validate due date string.

    Args:
        date_str: User-provided date string in YYYY-MM-DD format

    Returns:
        datetime object with date component, time set to midnight, or None if empty

    Raises:
        ValueError: If format is invalid or date is not a valid calendar date
    """
    cleaned = date_str.strip()

    if not cleaned:
        return None

    # Validate format first
    if len(cleaned) != 10 or cleaned[4] != '-' or cleaned[7] != '-':
        raise ValueError(
            f"Invalid date format. Use YYYY-MM-DD. Got: '{date_str}'"
        )

    try:
        year = int(cleaned[0:4])
        month = int(cleaned[5:7])
        day = int(cleaned[8:10])

        # Validate ranges
        if month < 1 or month > 12:
            raise ValueError(f"Invalid month: {month}. Must be 01-12.")

        if day < 1 or day > 31:
            raise ValueError(f"Invalid day: {day}. Must be 01-31.")

        # Create datetime to catch invalid calendar dates (e.g., Feb 31)
        due_date = datetime(year, month, day)

        return due_date

    except ValueError as e:
        # Check if it's our custom error or datetime validation
        if "must be" in str(e):
            raise
        raise ValueError(
            f"Invalid date: '{date_str}'. {str(e)}"
        )


def validate_recurrence(recurrence_str: str) -> Recurrence:
    """Parse case-insensitive recurrence string to Recurrence enum.

    Args:
        recurrence_str: User-provided recurrence string

    Returns:
        Recurrence enum value

    Raises:
        ValueError: If string doesn't match any recurrence value
    """
    cleaned = recurrence_str.strip().casefold()
    for recurrence in Recurrence:
        if recurrence.value == cleaned:
            return recurrence
    valid_values = ', '.join([r.value for r in Recurrence])
    raise ValueError(
        f"Invalid recurrence '{recurrence_str}'. Must be one of: {valid_values}"
    )
```

### Recurrence Calculation Functions

```python
def calculate_next_due_date(current_date: datetime, recurrence: Recurrence) -> datetime:
    """Calculate next due date based on recurrence pattern.

    Args:
        current_date: Current due date of task
        recurrence: Recurrence pattern

    Returns:
        Next due date

    Raises:
        ValueError: If recurrence is not recognized
    """
    from datetime import timedelta

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

        # Use min(day, last_day) to handle case where day doesn't exist in target month
        return datetime(year, month, min(day, last_day))

    raise ValueError(f"Unknown recurrence pattern: {recurrence}")
```

### Due Date Display Functions

```python
def format_due_date(due_date: Optional[datetime]) -> str:
    """Format due date for display.

    Args:
        due_date: Due date datetime or None

    Returns:
        Formatted string: "TODAY", "YYYY-MM-DD", or "No due date"
    """
    if due_date is None:
        return "No due date"

    today = datetime.now().date()
    task_date = due_date.date()

    if task_date == today:
        return "TODAY"

    return due_date.strftime("%Y-%m-%d")


def get_days_overdue(due_date: datetime) -> int:
    """Calculate days overdue for a task.

    Args:
        due_date: Due date of task

    Returns:
        Number of days overdue (positive if overdue, 0 if not overdue)
    """
    today = datetime.now().date()
    task_date = due_date.date()
    delta = today - task_date
    return max(0, delta.days)


def is_overdue(due_date: Optional[datetime]) -> bool:
    """Check if a task is overdue.

    Args:
        due_date: Due date of task (can be None)

    Returns:
        True if overdue, False otherwise
    """
    if due_date is None:
        return False
    today = datetime.now().date()
    return due_date.date() < today
```

### State Transitions

#### Recurrence Transitions
```
NONE ↔ DAILY ↔ WEEKLY ↔ MONTHLY
```
- Any recurrence can transition to any other recurrence
- Changing recurrence affects future occurrences only
- Default for new tasks: NONE
- Changing to NONE stops future auto-creation

#### Due Date Transitions
```
None ↔ Any valid date (YYYY-MM-DD)
```
- Task can have due date added, removed, or changed
- Changing due date on a recurring task affects future occurrences
- Past due dates are allowed (task becomes overdue)

#### Parent Task ID Transitions
```
None → Valid task ID (set once at creation)
```
- parent_task_id is set only when a new occurrence is created
- Never changes after creation
- Links child task to completed parent task

### Recurrence Chain Structure

```
Original Task (id=1, parent_task_id=None)
    ├─> First Occurrence (id=2, parent_task_id=1) [completed]
    │       └─> Second Occurrence (id=3, parent_task_id=2) [pending]
    │               └─> Third Occurrence (id=4, parent_task_id=3) [not created yet]
    └─> Direct Child (id=5, parent_task_id=1) [completed]
            └─> Grandchild (id=6, parent_task_id=5) [pending]
```

- Linear chain: Each task points to its immediate predecessor
- No circular references (parent_task_id < child.id)
- Independent deletion: Deleting a parent does not delete children

### Enum Usage Examples

```python
# Creating task with due date and weekly recurrence
task1 = Task(
    id=1,
    title="Weekly team meeting",
    description="Sync on progress",
    is_completed=False,
    created_at=datetime.now(),
    priority=Priority.MEDIUM,
    category="work",
    due_date=datetime(2025, 12, 30),
    recurrence=Recurrence.WEEKLY,
    parent_task_id=None
)

# Creating task with daily recurrence
task2 = Task(
    id=2,
    title="Take medication",
    description="Vitamins",
    is_completed=False,
    created_at=datetime.now(),
    priority=Priority.HIGH,
    category="health",
    due_date=datetime(2025, 12, 30),
    recurrence=Recurrence.DAILY
)

# Parsing user input to due date
user_input = "2025-12-30"
due_datetime = validate_due_date(user_input)  # Returns datetime(2025, 12, 30)

# Parsing user input to recurrence
user_input = "weekly"  # or "WEEKLY", "Weekly"
recurrence_enum = validate_recurrence(user_input)  # Returns Recurrence.WEEKLY

# Creating next occurrence
if task1.recurrence != Recurrence.NONE and task1.due_date:
    next_date = calculate_next_due_date(task1.due_date, task1.recurrence)
    next_task = Task(
        id=0,  # Will be assigned by storage
        title=task1.title,
        description=task1.description,
        is_completed=False,
        created_at=datetime.now(),
        priority=task1.priority,
        category=task1.category,
        due_date=next_date,
        recurrence=task1.recurrence,
        parent_task_id=task1.id
    )
```

### Backward Compatibility

#### Existing Task Migration
Tasks created before this feature will lack `due_date`, `recurrence`, and `parent_task_id` attributes.

**Migration Strategy** (Session-based, in-memory):
```python
# When loading existing tasks, check for missing attributes
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

**Note**: In Phase I (in-memory only), this migration only applies during runtime if old task objects exist. No database migration needed.

#### Type Safety
- New fields use type hints (`Optional[datetime]`, `Recurrence`, `Optional[int]`)
- Existing code using Task objects will need to be updated to handle new fields
- Default values ensure existing code doesn't break if new fields are ignored

---

## Relationships

**Task Entity Relationships**:
- No foreign key relationships to other entities (Phase I constraint)
- Task is independent, self-contained object
- `parent_task_id` is an informational reference, not a relationship constraint
- Categories are simple strings, not related entities

---

## Data Flow

### Recurring Task Completion Flow
```
User marks task complete
  → Check if task has recurrence and due_date
  → If yes: Calculate next due date
  → Create new task with parent_task_id = current task id
  → Mark current task as completed
  → Display confirmation with new task ID and due date
```

### Due Date Update Flow
```
User provides due date string
  → validate_due_date()
  → Parse YYYY-MM-DD format
  → Validate calendar date (leap year, month days)
  → Return datetime (time = 00:00:00)
  → Update task.due_date
  → storage.update(task)
```

---

## Constraints & Invariants

### Invariants
1. **Priority Enum**: All `priority` values are valid `Priority` enum members
2. **Category Length**: All `category` values are ≤ 50 characters or `None`
3. **Recurrence Enum**: All `recurrence` values are valid `Recurrence` enum members
4. **Due Date Format**: All `due_date` values are `datetime` objects or `None`
5. **ID Uniqueness**: All `id` values are unique (existing Phase I invariant)
6. **ID Immutability**: `id` cannot be changed after creation (existing Phase I invariant)
7. **Created At Immutability**: `created_at` cannot be changed (existing Phase I invariant)
8. **Parent Directionality**: `parent_task_id` always references a task with smaller id (no cycles)

### Constraints
1. **In-Memory Only**: All tasks lost on application exit (Phase I constraint)
2. **Single User**: No user ID or ownership (Phase I constraint)
3. **No Persistence**: No file or database storage (Phase I constraint)
4. **Standard Library**: No external packages (Phase I constraint)
5. **No Time Component**: Due dates are date-only (time always midnight)

---

## Display Representation

### Enhanced String Representation
```python
def __str__(self) -> str:
    """Human-readable task representation with advanced fields."""
    status = "[X]" if self.is_completed else "[ ]"
    category_str = self.category or "-"
    due_str = format_due_date(self.due_date)
    recurrence_str = self.recurrence.value.upper()

    if is_overdue(self.due_date) and not self.is_completed:
        days = get_days_overdue(self.due_date)
        due_str = f"{due_str} ({days} days overdue)"

    return (
        f"#{self.id} {status} {self.priority.value.upper()} "
        f"[{category_str}] {recurrence_str} Due: {due_str} "
        f"{self.title}"
    )

# Example output: #1 [ ] HIGH [work] WEEKLY Due: 2025-12-30 Weekly team meeting
```

### Enhanced Table Display
```
ID    | Priority | Due Date    | Status      | Title                          | Created
1     | HIGH     | 2025-12-30  | [ ]         | Weekly meeting                 | 2025-12-30 14:30:00
2     | MEDIUM   | 2025-12-28  | [X] OVERDUE | Take vitamins                  | 2025-12-30 08:00:00
3     | LOW      | No due date | [X]         | Buy groceries                  | 2025-12-30 12:00:00
```

---

## Testing Considerations

### Unit Tests
- `validate_due_date()` with valid formats
- `validate_due_date()` with invalid formats
- `validate_due_date()` with invalid calendar dates (Feb 31, Apr 31)
- `validate_due_date()` with leap year edge cases
- `validate_recurrence()` with valid inputs (case variations)
- `validate_recurrence()` with invalid inputs
- `calculate_next_due_date()` for DAILY recurrence
- `calculate_next_due_date()` for WEEKLY recurrence
- `calculate_next_due_date()` for MONTHLY recurrence (including edge cases)
- `format_due_date()` for today, future, and None
- `get_days_overdue()` calculation
- `is_overdue()` logic

### Integration Tests
- Create task with due date and recurrence
- Complete recurring task and verify next occurrence created
- Update task due date
- View task list with overdue indicators

### Edge Cases
- Due date exactly today (should show "TODAY")
- Due date in past (should show overdue)
- Recurring task without due date (should not auto-create)
- Monthly recurrence from Jan 31 (should go to Feb 28/29)
- Leap year calculation (Feb 29, 2024 vs Feb 28, 2025)
- Backward compatibility with existing tasks

---

## Summary

This data model extends Phase I and Intermediate Task entity with due_date, recurrence, and parent_task_id fields. It includes:

1. **New Enum**: `Recurrence` (NONE/DAILY/WEEKLY/MONTHLY)
2. **New Optional Fields**: `due_date`, `recurrence`, `parent_task_id`
3. **Validation Functions**: Date parsing, recurrence validation
4. **Recurrence Logic**: Next date calculation with edge case handling
5. **Display Functions**: Due date formatting, overdue detection
6. **Backward Compatibility**: Migration for existing tasks

All changes maintain Phase I constraints: in-memory storage only, no external dependencies, console-based interface.
