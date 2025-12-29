# Phase 0 Research: Intermediate Todo Features

**Feature**: Intermediate Todo Features
**Branch**: 1-intermediate-features
**Date**: 2025-12-29

## Overview

This document consolidates research findings for implementing intermediate features in the Phase I Todo App: priorities, categories, search, filters, and sorting. All research respects Phase I constraints (in-memory, standard library only, console-based).

---

## Research Topic 1: Priority Enum Implementation

### Question
How to represent task priorities (high/medium/low) with type safety and validation?

### Decision
Use Python `enum.Enum` class from the standard library.

### Rationale
- **Type Safety**: Enum prevents invalid values at runtime
- **Self-Documenting**: `Priority.HIGH` is clearer than `"high"` or `3`
- **Validation**: Automatic validation when using enum values
- **No Dependencies**: Built into Python 3.13+ (no external packages)
- **Iterable**: Can easily iterate over all valid values for UI options
- **Case Conversion**: Maps cleanly from user input strings

### Implementation Approach
```python
from enum import Enum

class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
```

**Case-Insensitive Parsing**:
```python
def validate_priority(priority_str: str) -> Priority:
    cleaned = priority_str.strip().lower()
    for priority in Priority:
        if priority.value == cleaned:
            return priority
    raise ValueError(f"Invalid priority: {priority_str}")
```

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| String constants (`HIGH = "high"`) | No type safety, prone to typos, harder to validate |
| Integer mapping (`HIGH = 3`) | Less readable, requires mapping for display |
| Plain strings (`"high"`) | No validation, manual checking required in every use |

---

## Research Topic 2: Case-Insensitive Comparison Pattern

### Question
How to handle case-insensitive matching for priorities, search keywords, and categories?

### Decision
Use `str.casefold()` for case-normalization before comparison.

### Rationale
- **Unicode Support**: `casefold()` handles more Unicode edge cases than `lower()`
- **Standard Library**: No external dependencies
- **Simple & Reliable**: One-liner normalization pattern
- **Consistent**: Same approach works for priority, search, and categories

### Implementation Approach
```python
# Priority matching
def validate_priority(priority_str: str) -> Priority:
    cleaned = priority_str.strip().casefold()
    for priority in Priority:
        if priority.value == cleaned:
            return priority
    raise ValueError(f"Invalid priority: {priority_str}")

# Keyword search
def keyword_matches(keyword: str, text: str) -> bool:
    return keyword.casefold() in text.casefold()

# Category filtering
def category_matches(category: str, task_category: Optional[str]) -> bool:
    if task_category is None:
        return False
    return category.casefold() == task_category.casefold()
```

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| `str.lower()` | Good for ASCII, but `casefold()` is better for Unicode |
| Regular expressions (`re.IGNORECASE`) | Overkill for simple case matching, slower |
| User-enforced casing | Poor UX, not user-friendly |
| Third-party libraries | Violates Phase I constraint (no external packages) |

---

## Research Topic 3: Filter State Management

### Question
How to track and manage active filter state across menu navigation in a CLI app?

### Decision
Track active filters as mutable state in the services layer, managed through a simple filter state object.

### Rationale
- **Session-Scoped**: Filters are transient (in-memory per session)
- **Services Layer**: Business logic layer owns filter logic
- **Separation of Concerns**: CLI handles user input, services apply filters
- **Simple**: No complex state management needed for Phase I
- **Clear API**: Methods accept filter criteria explicitly

### Implementation Approach
```python
from typing import Optional
from dataclasses import dataclass

@dataclass
class FilterState:
    status: Optional[bool] = None  # None=All, True=Completed, False=Pending
    priority: Optional[Priority] = None
    category: Optional[str] = None

    def clear(self) -> None:
        self.status = None
        self.priority = None
        self.category = None

    def is_active(self) -> bool:
        return any([self.status is not None,
                    self.priority is not None,
                    self.category is not None])

# In services:
def filter_tasks(tasks: List[Task], filters: FilterState) -> List[Task]:
    filtered = tasks

    if filters.status is not None:
        filtered = [t for t in filtered if t.is_completed == filters.status]

    if filters.priority is not None:
        filtered = [t for t in filtered if t.priority == filters.priority]

    if filters.category is not None:
        filtered = [t for t in filtered
                    if t.category and
                       filters.category.casefold() in t.category.casefold()]

    return filtered
```

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| CLI layer state | Violates separation of concerns - CLI shouldn't manage business logic state |
| Global variables | Poor design, hard to test, not thread-safe (even if not needed in Phase I) |
| Pass criteria per call | More complex API, no benefit, harder to extend |
| Command pattern (filter objects) | Over-engineering for simple console app |

---

## Research Topic 4: Sort Key Functions

### Question
How to implement multi-level sorting (primary + secondary criteria) in Python?

### Decision
Use Python `sorted()` with tuple keys and custom priority mapping.

### Rationale
- **Stable Sort**: `sorted()` is stable (maintains order of equal elements)
- **Tuple Keys**: Natural multi-level sorting with `(primary, secondary)`
- **Priority Mapping**: Custom mapping for non-alphabetic sort (HIGH > MEDIUM > LOW)
- **Secondary Sort**: `created_at` provides consistent tie-breaking
- **Functional**: Returns new list, doesn't modify original (safer)
- **Pythonic**: Clean, idiomatic Python code

### Implementation Approach
```python
from datetime import datetime
from typing import List

# Priority value for sorting (HIGH=3, MEDIUM=2, LOW=1)
PRIORITY_ORDER = {
    Priority.HIGH: 3,
    Priority.MEDIUM: 2,
    Priority.LOW: 1
}

def sort_by_priority(tasks: List[Task]) -> List[Task]:
    """Sort tasks by priority (HIGH → MEDIUM → LOW), secondary by created_at."""
    return sorted(
        tasks,
        key=lambda t: (
            PRIORITY_ORDER[t.priority],
            t.created_at  # Secondary sort: newer first
        ),
        reverse=True  # Descending priority and date
    )

def sort_alphabetically(tasks: List[Task]) -> List[Task]:
    """Sort tasks alphabetically by title, secondary by created_at."""
    return sorted(
        tasks,
        key=lambda t: (
            t.title.casefold(),  # Primary: A-Z
            t.created_at  # Secondary: newer first
        )
    )
```

### Sort Behavior Examples

**By Priority**:
```
Input: [Task(HIGH, "Task A", 10:00),
        Task(MEDIUM, "Task B", 11:00),
        Task(HIGH, "Task C", 09:00)]

Output: [Task(HIGH, "Task A", 10:00),  # HIGH first
         Task(HIGH, "Task C", 09:00),  # Same priority, newer first
         Task(MEDIUM, "Task B", 11:00)]  # MEDIUM next
```

**Alphabetically**:
```
Input: [Task("Banana"),
        Task("Apple"),
        Task("Cherry")]

Output: [Task("Apple"),   # A-Z order
         Task("Banana"),
         Task("Cherry")]
```

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| In-place `list.sort()` | Modifies storage, less functional, side effects |
| Custom comparator function | Deprecated in Python 3, less Pythonic |
| Multiple sorting passes | Less efficient, more code |
| External sorting libraries | Violates Phase I constraint |

---

## Research Topic 5: CLI Display Formatting

### Question
How to format task lists with new columns (Priority, Category) while maintaining readability?

### Decision
Extend existing fixed-width table format using Python f-strings with column width constraints.

### Rationale
- **Consistency**: Maintains existing table style from Phase I
- **Readable**: Fixed columns align data cleanly
- **Standard Library**: Uses Python f-strings, no dependencies
- **Truncation**: Handles long fields with ellipsis (...)
- **Compatible**: Works with existing display code structure

### Implementation Approach

**Column Specifications**:
```python
COLUMN_WIDTHS = {
    "id": 5,
    "priority": 9,       # "HIGH     "
    "category": 10,      # "work     " or truncates
    "status": 12,        # "[ ]       "
    "title": 30,         # Truncates with "..."
    "created_at": 19      # "2025-12-29 12:00:00"
}

def truncate(text: str, max_len: int) -> str:
    """Truncate text to max_len, adding ellipsis if needed."""
    if len(text) <= max_len:
        return text.ljust(max_len)
    return text[:max_len - 3].ljust(max_len - 3) + "..."

def format_task(task: Task) -> str:
    """Format a single task as a table row."""
    priority_display = task.priority.value.upper().ljust(COLUMN_WIDTHS["priority"])
    category_display = truncate(
        task.category or "",
        COLUMN_WIDTHS["category"]
    )
    status_display = "[X]" if task.is_completed else "[ ]"
    status_display = status_display.ljust(COLUMN_WIDTHS["status"])
    title_display = truncate(task.title, COLUMN_WIDTHS["title"])
    created_display = task.created_at.strftime("%Y-%m-%d %H:%M:%S")

    return (
        f"{task.id:<5} | "
        f"{priority_display} | "
        f"{category_display} | "
        f"{status_display} | "
        f"{title_display} | "
        f"{created_display}"
    )
```

**Table Display**:
```python
def display_table(title: str, tasks: List[Task]) -> None:
    print("=" * 100)
    print(f"{title:^100}")
    print("=" * 100)
    print("ID    | Priority | Category | Status      | Title                          | Created")
    print("-" * 100)

    for task in tasks:
        print(format_task(task))

    print("-" * 100)
    print(f"Total: {len(tasks)} tasks")
    print("=" * 100)
```

**Output Example**:
```
================================================================================
                              YOUR TASKS
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | work     | [ ]         | Finish report                  | 2025-12-29 11:45:00
2     | MEDIUM   | personal | [X]         | Call dentist                   | 2025-12-29 09:15:00
3     | LOW      |         | [ ]         | Buy groceries                  | 2025-12-29 10:30:00
4     | HIGH     | work     | [ ]         | Prepare presentation           | 2025-12-29 12:00:00
--------------------------------------------------------------------------------
Total: 4 tasks
================================================================================
```

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Third-party table libraries (`tabulate`, `prettytable`) | Violates Phase I constraint (no external packages) |
| CSV output format | Less readable in console, harder to scan |
| Separate views per feature | Inconsistent UX, confusing for users |
| Dynamic column widths | Harder to align, complex for simple use case |

---

## Summary

All research topics have been resolved with approaches that:

1. **Respect Phase I constraints** (in-memory, standard library, console-based)
2. **Maintain clean architecture** (separation of concerns, layered design)
3. **Provide clear implementation paths** (concrete code patterns)
4. **Handle edge cases** (validation, error messages, user feedback)
5. **Support user requirements** (priorities, categories, search, filters, sorting)

**Next Phase**: Proceed to Phase 1 design (data-model.md, contracts/, quickstart.md).

---

*This research document resolves all technical decisions for implementing intermediate Todo features.*
