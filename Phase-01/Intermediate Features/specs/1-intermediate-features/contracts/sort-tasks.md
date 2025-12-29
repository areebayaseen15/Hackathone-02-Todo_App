# Contract: Sort Tasks

**Feature**: Intermediate Todo Features
**Type**: CLI Command Specification
**Date**: 2025-12-29

## Command

`sort_tasks` - Sort task list by priority or alphabetically

## User Flow

1. System displays "SORT TASKS" header
2. System displays sort options menu
3. User selects sort method or returns to default order
4. System applies sorting to task list
5. System displays sorted tasks in table format
6. System displays sort method used
7. System pauses for user to press Enter
8. System returns to sort menu (or main menu option)

## Menu Specification

### Sort Menu

```
================================================================================
                            SORT TASKS
================================================================================
Available sort options:
  [1] Sort by Priority (HIGH → MEDIUM → LOW)
  [2] Sort Alphabetically by Title (A → Z)
  [3] Default Order (by ID/Creation Date)
  [4] Back to Main Menu

Current sort: {display current sort method}
Enter your choice (1-4): _
```

## Input Specification

### Sort Type Selection

| Option | Sort Method | Primary Key | Secondary Key | Direction |
|---------|-------------|--------------|----------------|------------|
| 1 | By Priority | Priority (value: HIGH=3, MEDIUM=2, LOW=1) | Created At | Descending (newest first) |
| 2 | Alphabetically | Title (case-insensitive) | Created At | Ascending (A → Z) for title, descending for date |
| 3 | Default Order | ID | Created At | Ascending (by ID) |
| 4 | Back | N/A | N/A | Returns to main menu |

## Sort Logic

### Sort by Priority

**Primary Key**: Priority value (HIGH > MEDIUM > LOW)
**Secondary Key**: Created At (newest first)
**Direction**: Descending

```python
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
            PRIORITY_ORDER[t.priority],  # Primary: priority value
            t.created_at                # Secondary: newest first
        ),
        reverse=True  # Descending
    )
```

**Example**:
```
Input: [Task(HIGH, "A", 10:00), Task(MEDIUM, "B", 11:00), Task(HIGH, "C", 09:00)]

Output:
ID    | Priority | Title
1     | HIGH     | A     # HIGH, newer
2     | HIGH     | C     # HIGH, older
3     | MEDIUM   | B     # MEDIUM
```

### Sort Alphabetically

**Primary Key**: Title (case-insensitive, A → Z)
**Secondary Key**: Created At (newest first)
**Direction**: Ascending for title, descending for date

```python
def sort_alphabetically(tasks: List[Task]) -> List[Task]:
    """Sort tasks alphabetically by title, secondary by created_at."""
    return sorted(
        tasks,
        key=lambda t: (
            t.title.casefold(),  # Primary: A-Z
            t.created_at         # Secondary: newest first
        )
    )
```

**Example**:
```
Input: [Task("Banana", 10:00), Task("Apple", 11:00), Task("apple", 09:00)]

Output:
ID    | Title
1     | Apple  # A-Z first, then newest
2     | apple  # Same title (case-insensitive), newer
3     | Banana
```

### Default Order

**Primary Key**: ID
**Direction**: Ascending

```python
def sort_default(tasks: List[Task]) -> List[Task]:
    """Sort tasks by default order (by ID/creation date)."""
    return sorted(tasks, key=lambda t: t.id)
```

## Output Specification

### Sorted Tasks Display

```
================================================================================
Tasks sorted by {sort method}
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
{id}   | {PRIORITY} | {category} | {[X] or [ ]} | {title}            | {created_at}
...
--------------------------------------------------------------------------------
Press Enter to continue...
```

### Sort Method Display Strings

| Option | Display String |
|---------|---------------|
| Sort by Priority | "priority" |
| Alphabetically | "alphabetically (A-Z)" |
| Default Order | "default order (by ID)" |

### Empty Task List Display

```
================================================================================
No tasks to sort
================================================================================
Press Enter to continue...
```

## Function Signatures

```python
def sort_by_priority(tasks: List[Task]) -> List[Task]:
    """Sort tasks by priority (HIGH → MEDIUM → LOW), secondary by created_at.

    Args:
        tasks: List of tasks to sort

    Returns:
        Sorted list of tasks
    """

def sort_alphabetically(tasks: List[Task]) -> List[Task]:
    """Sort tasks alphabetically by title, secondary by created_at.

    Args:
        tasks: List of tasks to sort

    Returns:
        Sorted list of tasks
    """

def sort_default(tasks: List[Task]) -> List[Task]:
    """Sort tasks by default order (by ID).

    Args:
        tasks: List of tasks to sort

    Returns:
        Sorted list of tasks
    """
```

## Success Criteria

- [ ] Sort menu displays all options correctly
- [ ] Current sort method is displayed
- [ ] Sort by priority works correctly (HIGH → MEDIUM → LOW)
- [ ] Secondary sort by created_at works within priority groups
- [ ] Alphabetical sort works correctly (A → Z)
- [ ] Alphabetical sort is case-insensitive
- [ ] Secondary sort by created_at works within same titles
- [ ] Default order restores original sort (by ID)
- [ ] Sorted tasks display correctly in table format
- [ ] "No tasks to sort" message shown when task list is empty

## Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| Single task | Task displayed (sorted trivially) |
| Empty task list | "No tasks to sort" message |
| All tasks same priority | Sorted by created_at (newest first) |
| All tasks same title | Sorted by created_at (newest first) |
| Mixed case titles | Sorted case-insensitively |
| Identical tasks (except ID) | Sorted by ID (implicit) |
| Sorting with active filters | Sorts the filtered result set |
| Resorting after sort | Applies new sort method |

## Dependencies

- `Task` dataclass with `priority`, `title`, `created_at` fields
- `Priority` enum
- `PRIORITY_ORDER` mapping for sorting
- List of tasks (potentially filtered)

## User Examples

**Example 1: Sort by priority**
```
================================================================================
                            SORT TASKS
================================================================================
Available sort options:
  [1] Sort by Priority (HIGH → MEDIUM → LOW)
  [2] Sort Alphabetically by Title (A → Z)
  [3] Default Order (by ID/Creation Date)
  [4] Back to Main Menu

Current sort: default order (by ID)
Enter your choice (1-4): 1

================================================================================
Tasks sorted by priority
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | work     | [ ]         | Finish report                  | 2025-12-29 11:45:00
4     | HIGH     | work     | [ ]         | Prepare presentation           | 2025-12-29 12:00:00
3     | LOW      |         | [ ]         | Buy groceries                  | 2025-12-29 10:30:00
2     | MEDIUM   | personal | [X]         | Call dentist                   | 2025-12-29 09:15:00
--------------------------------------------------------------------------------
Press Enter to continue...
```

**Example 2: Sort alphabetically**
```
================================================================================
                            SORT TASKS
================================================================================
Current sort: priority
Enter your choice (1-4): 2

================================================================================
Tasks sorted by alphabetically (A-Z)
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
2     | MEDIUM   | personal | [X]         | Call dentist                   | 2025-12-29 09:15:00
3     | LOW      |         | [ ]         | Buy groceries                  | 2025-12-29 10:30:00
1     | HIGH     | work     | [ ]         | Finish report                  | 2025-12-29 11:45:00
4     | HIGH     | work     | [ ]         | Prepare presentation           | 2025-12-29 12:00:00
--------------------------------------------------------------------------------
Press Enter to continue...
```

**Example 3: Default order**
```
================================================================================
                            SORT TASKS
================================================================================
Current sort: alphabetically (A-Z)
Enter your choice (1-4): 3

================================================================================
Tasks sorted by default order (by ID)
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | work     | [ ]         | Finish report                  | 2025-12-29 11:45:00
2     | MEDIUM   | personal | [X]         | Call dentist                   | 2025-12-29 09:15:00
3     | LOW      |         | [ ]         | Buy groceries                  | 2025-12-29 10:30:00
4     | HIGH     | work     | [ ]         | Prepare presentation           | 2025-12-29 12:00:00
--------------------------------------------------------------------------------
Press Enter to continue...
```

**Example 4: Empty task list**
```
================================================================================
                            SORT TASKS
================================================================================
Available sort options:
  [1] Sort by Priority (HIGH → MEDIUM → LOW)
  [2] Sort Alphabetically by Title (A → Z)
  [3] Default Order (by ID/Creation Date)
  [4] Back to Main Menu

Current sort: default order (by ID)
Enter your choice (1-4): 1

================================================================================
No tasks to sort
================================================================================
Press Enter to continue...
```

**Example 5: All tasks same priority (secondary sort)**
```
All tasks have MEDIUM priority.

================================================================================
Tasks sorted by priority
================================================================================
ID    | Priority | Title                          | Created
--------------------------------------------------------------------------------
4     | MEDIUM   | Task D (12:30)                 | 2025-12-29 12:30:00  # Newest first
2     | MEDIUM   | Task B (09:15)                 | 2025-12-29 09:15:00
1     | MEDIUM   | Task A (11:00)                 | 2025-12-29 11:00:00
3     | MEDIUM   | Task C (10:00)                 | 2025-12-29 10:00:00  # Oldest
--------------------------------------------------------------------------------
```

**Example 6: Case-insensitive alphabetical sort**
```
Tasks: ["banana", "Apple", "cherry", "apple"]

Sorted: ["Apple", "apple", "banana", "cherry"]
# Case-insensitive A-Z, with created_at as tiebreaker
```

---

*This contract defines Sort Tasks command with priority and alphabetical sorting.*
