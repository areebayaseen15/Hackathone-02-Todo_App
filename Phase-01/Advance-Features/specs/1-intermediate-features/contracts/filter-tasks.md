# Contract: Filter Tasks

**Feature**: Intermediate Todo Features
**Type**: CLI Command Specification
**Date**: 2025-12-29

## Command

`filter_tasks` - Filter task list by status, priority, and/or category

## User Flow

1. System displays "FILTER TASKS" header
2. System displays filter options menu
3. User selects filter type or clears filters
4. System prompts for filter value (if applicable)
5. System applies filter (AND logic with existing filters)
6. System displays filtered tasks in table format
7. System displays active filter criteria
8. System pauses for user to press Enter
9. System returns to filter menu (or main menu option)

## Menu Specification

### Filter Menu

```
================================================================================
                            FILTER TASKS
================================================================================
Available filters:
  [1] By Status (pending/completed)
  [2] By Priority (high/medium/low)
  [3] By Category
  [4] Clear All Filters
  [5] Back to Main Menu

Active filters: {display active filters or "None"}
Enter your choice (1-5): _
```

## Input Specification

### Filter Type Selection

| Option | Filter | Value Type | Input |
|---------|---------|-------------|--------|
| 1 | Status | String | "pending" or "completed" |
| 2 | Priority | String | "high"/"medium"/"low" |
| 3 | Category | String | Category name |
| 4 | Clear All | N/A | Clears all active filters |
| 5 | Back | N/A | Returns to main menu |

### Filter Value Validation

**Status**:
- Accepts: "pending", "completed"
- Case-insensitive
- Error: "Invalid status. Must be 'pending' or 'completed'"

**Priority**:
- Accepts: "high", "medium", "low"
- Case-insensitive
- Error: "Invalid priority '{value}'. Must be one of: high, medium, low"

**Category**:
- Accepts any category name (0-50 chars)
- Case-insensitive matching
- Empty input returns to filter menu

## Filter Logic

### AND Logic
Multiple filters are applied with AND logic:
```
Filtered Tasks = All Tasks
  AND matches status filter (if active)
  AND matches priority filter (if active)
  AND matches category filter (if active)
```

### Active Filter Tracking

```python
@dataclass
class FilterState:
    status: Optional[bool] = None    # None=All, True=Completed, False=Pending
    priority: Optional[Priority] = None
    category: Optional[str] = None

    def is_active(self) -> bool:
        return any([self.status is not None,
                    self.priority is not None,
                    self.category is not None])

    def display(self) -> str:
        parts = []
        if self.status is not None:
            parts.append(f"status={'completed' if self.status else 'pending'}")
        if self.priority is not None:
            parts.append(f"priority={self.priority.value}")
        if self.category is not None:
            parts.append(f"category={self.category}")
        return ", ".join(parts) if parts else "None"
```

## Output Specification

### Filtered Tasks Display

```
================================================================================
Filtered Tasks: {count} task{plural} ({filter criteria})
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
{id}   | {PRIORITY} | {category} | {[X] or [ ]} | {title}            | {created_at}
...
--------------------------------------------------------------------------------
Press Enter to continue...
```

### No Results Display

```
================================================================================
No tasks match the current filters
Active filters: {filter criteria}
================================================================================
Press Enter to continue...
```

### Empty Task List Display

```
================================================================================
No tasks available to filter
================================================================================
Press Enter to continue...
```

### Filters Cleared Display

```
All filters cleared. Showing all tasks.
================================================================================
Total: {count} task{plural}
================================================================================
Press Enter to continue...
```

## Function Signature

```python
def filter_tasks(
    tasks: List[Task],
    filters: FilterState
) -> List[Task]:
    """Filter tasks by status, priority, and/or category.

    Args:
        tasks: List of tasks to filter
        filters: Active filter criteria

    Returns:
        List of tasks matching all active filters (AND logic)
    """
```

## Filter Implementation

```python
def filter_tasks(tasks: List[Task], filters: FilterState) -> List[Task]:
    filtered = tasks

    # Filter by status
    if filters.status is not None:
        filtered = [t for t in filtered if t.is_completed == filters.status]

    # Filter by priority
    if filters.priority is not None:
        filtered = [t for t in filtered if t.priority == filters.priority]

    # Filter by category (case-insensitive)
    if filters.category is not None:
        category_lower = filters.category.casefold()
        filtered = [t for t in filtered
                    if t.category and category_lower in t.category.casefold()]

    return filtered
```

## Success Criteria

- [ ] Filter menu displays all options correctly
- [ ] Active filters are displayed
- [ ] Status filter works (pending/completed)
- [ ] Priority filter works (high/medium/low)
- [ ] Category filter works (case-insensitive)
- [ ] Multiple filters apply with AND logic
- [ ] Clear All Filters resets all filter state
- [ ] Filtered results display correctly
- [ ] "No tasks match" message shown when no results
- [ ] "No tasks available" shown when task list is empty

## Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| No active filters | Shows all tasks |
| Single filter active | Shows matching tasks |
| Multiple filters active | Shows tasks matching ALL filters (AND logic) |
| Conflicting filters (status=pending AND completed) | No results, "No tasks match" message |
| Filter with no matches | "No tasks match current filters" message |
| Filter with empty task list | "No tasks available to filter" message |
| Category not found | No tasks match for that category filter |
| Case variations in category | Case-insensitive matching works |
| Clear All Filters | Returns to showing all tasks |
| Back to Main Menu | Exits filter menu, keeps filters active |

## Dependencies

- `Task` dataclass with `is_completed`, `priority`, `category` fields
- `FilterState` dataclass for tracking active filters
- `Priority` enum
- List of tasks from storage

## User Examples

**Example 1: Filter by status**
```
================================================================================
                            FILTER TASKS
================================================================================
Available filters:
  [1] By Status (pending/completed)
  [2] By Priority (high/medium/low)
  [3] By Category
  [4] Clear All Filters
  [5] Back to Main Menu

Active filters: None
Enter your choice (1-5): 1
Enter status to filter (pending/completed): pending

================================================================================
Filtered Tasks: 3 tasks (status=pending)
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | work     | [ ]         | Finish report                  | 2025-12-29 11:45:00
3     | LOW      |         | [ ]         | Buy groceries                  | 2025-12-29 10:30:00
4     | HIGH     | work     | [ ]         | Prepare presentation           | 2025-12-29 12:00:00
--------------------------------------------------------------------------------
Press Enter to continue...
```

**Example 2: Filter by priority (with existing status filter)**
```
================================================================================
                            FILTER TASKS
================================================================================
Active filters: status=pending
Enter your choice (1-5): 2
Enter priority to filter (high/medium/low): high

================================================================================
Filtered Tasks: 2 tasks (status=pending, priority=high)
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | work     | [ ]         | Finish report                  | 2025-12-29 11:45:00
4     | HIGH     | work     | [ ]         | Prepare presentation           | 2025-12-29 12:00:00
--------------------------------------------------------------------------------
Press Enter to continue...
```

**Example 3: Filter by category**
```
================================================================================
                            FILTER TASKS
================================================================================
Active filters: status=pending, priority=high
Enter your choice (1-5): 3
Enter category to filter: work

================================================================================
Filtered Tasks: 2 tasks (status=pending, priority=high, category=work)
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | work     | [ ]         | Finish report                  | 2025-12-29 11:45:00
4     | HIGH     | work     | [ ]         | Prepare presentation           | 2025-12-29 12:00:00
--------------------------------------------------------------------------------
Press Enter to continue...
```

**Example 4: Clear all filters**
```
================================================================================
                            FILTER TASKS
================================================================================
Active filters: status=pending, priority=high, category=work
Enter your choice (1-5): 4

All filters cleared. Showing all tasks.
================================================================================
Total: 4 tasks
================================================================================
Press Enter to continue...
```

**Example 5: No results**
```
================================================================================
                            FILTER TASKS
================================================================================
Active filters: None
Enter your choice (1-5): 1
Enter status to filter (pending/completed): completed

================================================================================
No tasks match the current filters
Active filters: status=completed
================================================================================
Press Enter to continue...
```

**Example 6: Back to main menu**
```
================================================================================
                            FILTER TASKS
================================================================================
Active filters: status=pending, priority=high
Enter your choice (1-5): 5
[Returns to main menu, filters remain active]
```

---

*This contract defines* Filter Tasks *command with status, priority, and category filtering.*
