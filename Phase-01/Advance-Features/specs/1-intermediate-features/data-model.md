# Data Model: Intermediate Todo Features

**Feature**: Intermediate Todo Features
**Branch**: 1-intermediate-features
**Date**: 2025-12-29

## Overview

This document defines the data model changes required to add intermediate features (priorities, categories) to the Phase I Todo App. All changes maintain backward compatibility with existing Phase I task data.

---

## Entity: Task

### Modified Entity (Updated from Phase I)

**File**: `src/todo/models.py`

```python
from dataclasses import dataclass, field
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

@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier for the task (auto-generated, positive integer)
        title: Short descriptive name of the task (1-100 characters, required)
        description: Detailed description of the task (0-500 characters, optional)
        is_completed: Completion status of the task (default: False)
        created_at: Timestamp when task was created (auto-generated, immutable)
        priority: Priority level of the task (HIGH/MEDIUM/LOW, default: MEDIUM)
        category: Optional category or tag for grouping (0-50 characters, optional)
    """

    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    priority: Priority = Priority.MEDIUM  # NEW: Default to MEDIUM
    category: Optional[str] = None       # NEW: Optional category
```

### Field Specifications

| Field | Type | Default | Constraints | Description |
|-------|------|---------|-------------|-------------|
| `id` | `int` | Auto-generated | Positive integer, unique | Unique identifier |
| `title` | `str` | Required | 1-100 characters, non-empty | Short descriptive name |
| `description` | `str` | Empty string | 0-500 characters | Detailed description |
| `is_completed` | `bool` | `False` | Boolean only | Completion status |
| `created_at` | `datetime` | Auto-generated | Immutable | Creation timestamp |
| `priority` | `Priority` | `Priority.MEDIUM` | Enum: HIGH/MEDIUM/LOW | Priority level |
| `category` | `Optional[str]` | `None` | 0-50 characters, optional | Category tag |

### Field Validation Rules

#### Priority Field
- **Type**: Must be `Priority` enum value
- **Default**: `Priority.MEDIUM` if not specified
- **Valid Values**: `Priority.HIGH`, `Priority.MEDIUM`, `Priority.LOW`
- **Case-Insensitive Input**: User input "high", "HIGH", "High" all map to `Priority.HIGH`
- **Validation**: Invalid values raise `ValueError`

#### Category Field
- **Type**: `Optional[str]` (string or `None`)
- **Default**: `None` (no category)
- **Length**: 0-50 characters
- **Validation**: Strings > 50 characters raise `ValueError`
- **Whitespace**: Leading/trailing whitespace is trimmed
- **Empty String**: Empty string after trim is treated as `None`
- **Special Characters**: Any printable characters allowed

### Validation Functions

```python
def validate_priority(priority_str: str) -> Priority:
    """Parse case-insensitive priority string to Priority enum.

    Args:
        priority_str: User-provided priority string

    Returns:
        Priority enum value

    Raises:
        ValueError: If string doesn't match any priority value
    """
    cleaned = priority_str.strip().casefold()
    for priority in Priority:
        if priority.value == cleaned:
            return priority
    raise ValueError(
        f"Invalid priority '{priority_str}'. "
        f"Must be one of: {', '.join([p.value for p in Priority])}"
    )

def validate_category(category_str: str) -> Optional[str]:
    """Validate and clean category string.

    Args:
        category_str: User-provided category string

    Returns:
        Cleaned category string or None if empty

    Raises:
        ValueError: If category exceeds 50 characters
    """
    cleaned = category_str.strip()

    if not cleaned:
        return None

    if len(cleaned) > 50:
        raise ValueError(
            f"Category must be 50 characters or less. "
            f"Got {len(cleaned)} characters."
        )

    return cleaned
```

### State Transitions

#### Priority Transitions
```
HIGH    ↔ MEDIUM ↔ LOW
```
- Any priority can transition to any other priority
- No restrictions on priority changes
- Default for new tasks: MEDIUM

#### Category Transitions
```
None ↔ Any valid category (0-50 chars)
```
- Task can change category or have no category
- No category hierarchy or constraints
- Any printable characters allowed

### Enum Usage Examples

```python
# Creating tasks with explicit priority
task1 = Task(
    id=1,
    title="Urgent task",
    description="Must do today",
    is_completed=False,
    created_at=datetime.now(),
    priority=Priority.HIGH  # Explicit HIGH priority
)

# Creating task with default priority (MEDIUM)
task2 = Task(
    id=2,
    title="Normal task",
    description="Regular priority",
    is_completed=False,
    created_at=datetime.now(),
    # priority defaults to Priority.MEDIUM
)

# Creating task with category
task3 = Task(
    id=3,
    title="Work task",
    description="Project deliverable",
    is_completed=False,
    created_at=datetime.now(),
    category="work"
)

# Parsing user input to priority
user_input = "high"  # or "HIGH", "High"
priority_enum = validate_priority(user_input)  # Returns Priority.HIGH
```

### Backward Compatibility

#### Existing Task Migration
Tasks created before this feature will lack `priority` and `category` attributes.

**Migration Strategy** (Session-based, in-memory):
```python
# When loading existing tasks, check for missing attributes
def ensure_task_compatibility(task: Task) -> Task:
    """Ensure task has all required attributes."""
    if not hasattr(task, 'priority'):
        task.priority = Priority.MEDIUM
    if not hasattr(task, 'category'):
        task.category = None
    return task
```

**Note**: In Phase I (in-memory only), this migration only applies during runtime if old task objects exist. No database migration needed.

#### Type Safety
- New fields use type hints (`Priority`, `Optional[str]`)
- Existing code using Task objects will need to be updated to handle new fields
- Default values ensure existing code doesn't break if new fields are ignored

---

## Relationships

**Task Entity Relationships**:
- No relationships to other entities (Phase I constraint)
- Task is independent, self-contained object
- Categories are simple strings, not related entities

---

## Data Flow

### Creation Flow
```
User Input
  → validate_priority()
  → validate_category()
  → Task(
        id=storage.next_id(),
        title=validated_title,
        description=validated_description,
        is_completed=False,
        created_at=datetime.now(),
        priority=Priority.MEDIUM or validated,
        category=validated_category or None
    )
  → storage.add(task)
```

### Update Flow
```
User Input
  → validate_priority() [if updating priority]
  → validate_category() [if updating category]
  → Update task fields
  → storage.update(task)
```

### Search/Filter Flow
```
Task Collection
  → filter_by_status() [optional]
  → filter_by_priority() [optional]
  → filter_by_category() [optional]
  → search_by_keyword() [optional]
  → sort_by_priority() or sort_alphabetically() [optional]
  → Display filtered/sorted tasks
```

---

## Constraints & Invariants

### Invariants
1. **Priority Enum**: All `priority` values are valid `Priority` enum members
2. **Category Length**: All `category` values are ≤ 50 characters or `None`
3. **ID Uniqueness**: All `id` values are unique (existing Phase I invariant)
4. **ID Immutability**: `id` cannot be changed after creation (existing Phase I invariant)
5. **Created At Immutability**: `created_at` cannot be changed (existing Phase I invariant)

### Constraints
1. **In-Memory Only**: All tasks lost on application exit (Phase I constraint)
2. **Single User**: No user ID or ownership (Phase I constraint)
3. **No Persistence**: No file or database storage (Phase I constraint)
4. **Standard Library**: No external packages (Phase I constraint)

---

## Display Representation

### String Representation
```python
def __str__(self) -> str:
    """Human-readable task representation."""
    status = "[X]" if self.is_completed else "[ ]"
    category_str = self.category or "-"
    return (
        f"#{self.id} {status} {self.priority.value.upper()} "
        f"[{category_str}] {self.title}"
    )

# Example output: #1 [X] HIGH [work] Finish report
```

### Table Display
```
ID    | Priority | Category | Status      | Title
1     | HIGH     | work     | [X]         | Finish report
2     | MEDIUM   |         | [ ]         | Buy groceries
```

---

## Testing Considerations

### Unit Tests
- `validate_priority()` with valid inputs (case variations)
- `validate_priority()` with invalid inputs
- `validate_category()` with valid inputs (within limits)
- `validate_category()` with invalid inputs (> 50 chars)
- `Task` creation with all fields specified
- `Task` creation with default values
- Task field updates

### Integration Tests
- Create task with priority and category
- Update task priority
- Update task category
- Search tasks by keyword
- Filter tasks by priority
- Filter tasks by category
- Sort tasks by priority
- Sort tasks alphabetically

### Edge Cases
- Empty category string (should become `None`)
- Whitespace-only category (should become `None`)
- Category exactly 50 characters (should succeed)
- Category 51 characters (should error)
- Priority with mixed case input (should parse correctly)
- Invalid priority input (should raise error)

---

*This data model extends the Phase I Task entity with priority and category fields while maintaining backward compatibility and Phase I constraints.*
