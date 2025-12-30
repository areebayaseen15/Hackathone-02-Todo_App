# Quickstart Guide: Intermediate Todo Features

**Feature**: Intermediate Todo Features
**Branch**: 1-intermediate-features
**Date**: 2025-12-29

## Overview

This guide provides step-by-step instructions for implementing intermediate features in the Phase I Todo App. Features include task priorities, categories, keyword search, filtering, and sorting.

## Implementation Checklist

### Phase 1A: Data Model Foundation

- [ ] Add `Priority` enum to `src/todo/models.py`
- [ ] Add `priority` field to `Task` dataclass (type: `Priority`, default: `Priority.MEDIUM`)
- [ ] Add `category` field to `Task` dataclass (type: `Optional[str]`, default: `None`)
- [ ] Update `Task` docstring to document new fields
- [ ] Test: Create task with new fields via Python REPL

```python
# src/todo/models.py - Add before Task class:
class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Modify Task dataclass:
@dataclass
class Task:
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    priority: Priority = Priority.MEDIUM  # NEW
    category: Optional[str] = None       # NEW
```

### Phase 1B: Service Logic

- [ ] Add `validate_priority()` function to `src/todo/services.py`
- [ ] Add `validate_category()` function to `src/todo/services.py`
- [ ] Add `search_tasks()` function to `src/todo/services.py`
- [ ] Add `filter_tasks()` function to `src/todo/services.py`
- [ ] Add `sort_by_priority()` function to `src/todo/services.py`
- [ ] Add `sort_alphabetically()` function to `src/todo/services.py`
- [ ] Modify `create_task()` to accept `priority` and `category` parameters
- [ ] Modify `update_task()` to update `priority` and `category` fields

```python
# src/todo/services.py - Add validation functions:

def validate_priority(priority_str: str) -> Priority:
    cleaned = priority_str.strip().casefold()
    for priority in Priority:
        if priority.value == cleaned:
            return priority
    raise ValueError(f"Invalid priority '{priority_str}'. Must be one of: high, medium, low")

def validate_category(category_str: str) -> Optional[str]:
    cleaned = category_str.strip()
    if not cleaned:
        return None
    if len(cleaned) > 50:
        raise ValueError(f"Category must be 50 characters or less. Got {len(cleaned)} characters.")
    return cleaned

# Add search, filter, sort functions (see contracts/ for details)
```

### Phase 1C: Storage Layer

- [ ] Add `search(keyword: str) -> List[Task]` wrapper method
- [ ] Add `filter_by_status(status: bool) -> List[Task]` wrapper method
- [ ] Add `filter_by_priority(priority: Priority) -> List[Task]` wrapper method
- [ ] Add `filter_by_category(category: str) -> List[Task]` wrapper method
- [ ] Add `sort_by(criteria: str) -> List[Task]` wrapper method

**Note**: Storage methods are thin wrappers around service functions. See `contracts/` for detailed specifications.

### Phase 1D: CLI Presentation

- [ ] Update `display_main_menu()` to include new options (6, 7, 8)
- [ ] Modify `display_add_task()` for priority and category prompts
- [ ] Modify `display_update_task()` for priority and category updates
- [ ] Modify `display_tasks()` table format with Priority and Category columns
- [ ] Add `display_search_menu()` screen (see `contracts/search-tasks.md`)
- [ ] Add `display_filter_menu()` screen (see `contracts/filter-tasks.md`)
- [ ] Add `display_sort_menu()` screen (see `contracts/sort-tasks.md`)
- [ ] Add `display_filtered_tasks(title: str, tasks: List[Task])` helper function

```python
# Updated main menu:
def display_main_menu() -> int:
    print("""
  [1] Add Task
  [2] View Tasks
  [3] Update Task
  [4] Delete Task
  [5] Toggle Task Status
  [6] Search Tasks        # NEW
  [7] Filter Tasks        # NEW
  [8] Sort Tasks          # NEW
  [9] Exit               # Renumbered from 6
""")
```

**Column Widths for Table Display**:
```python
COLUMN_WIDTHS = {
    "id": 5,
    "priority": 9,
    "category": 10,
    "status": 12,
    "title": 30,
    "created_at": 19
}
```

### Phase 1E: Error Handling

- [ ] Add validation error for invalid priority values
- [ ] Add validation error for category length > 50
- [ ] Add empty search keyword validation error
- [ ] Add "no results found" messages for search/filter
- [ ] Add "no tasks available" message for empty task list
- [ ] Test all error messages display correctly

## Testing Guide

### 1. Task Creation with Priority and Category

```bash
uv run todo

# Test 1: Create task with all fields
[1] Add Task
Title: Finish report
Description: [Enter]
Priority: high
Category: work

# Expected: Task created with ID, HIGH priority, work category
```

### 2. Search by Keyword

```bash
# Test 1: Search for task in title
[6] Search Tasks
Keyword: report

# Expected: Shows tasks with "report" in title

# Test 2: Search for task in description
[6] Search Tasks
Keyword: meeting

# Expected: Shows tasks with "meeting" in description

# Test 3: Case-insensitive search
[6] Search Tasks
Keyword: REPORT

# Expected: Same results as "report" (case-insensitive)
```

### 3. Filter Tasks

```bash
# Test 1: Filter by status
[7] Filter Tasks
[1] By Status
Status: pending

# Expected: Shows only incomplete tasks

# Test 2: Filter by priority
[7] Filter Tasks
[2] By Priority
Priority: high

# Expected: Shows only high-priority tasks

# Test 3: Multiple filters (status + priority)
[7] Filter Tasks
[1] By Status -> pending
[2] By Priority -> high

# Expected: Shows tasks that are BOTH pending AND high priority

# Test 4: Clear all filters
[7] Filter Tasks
[4] Clear All Filters

# Expected: Shows all tasks, filters cleared
```

### 4. Sort Tasks

```bash
# Test 1: Sort by priority
[8] Sort Tasks
[1] Sort by Priority

# Expected: Tasks ordered HIGH → MEDIUM → LOW, newer first within groups

# Test 2: Sort alphabetically
[8] Sort Tasks
[2] Sort Alphabetically

# Expected: Tasks ordered A-Z by title, newer first for same titles

# Test 3: Return to default order
[8] Sort Tasks
[3] Default Order

# Expected: Tasks ordered by ID (original order)
```

### 5. Edge Cases

```bash
# Test 1: Invalid priority
[1] Add Task
Title: Test
Priority: urgent

# Expected: Error message "Invalid priority 'urgent'. Must be one of: high, medium, low"

# Test 2: Category too long
[1] Add Task
Title: Test
Category: {51 characters}

# Expected: Error message "Category must be 50 characters or less"

# Test 3: Empty search keyword
[6] Search Tasks
Keyword: [Enter]

# Expected: Error message "Keyword cannot be empty"

# Test 4: No search results
[6] Search Tasks
Keyword: nonexistent

# Expected: Message "No tasks found matching 'nonexistent'"

# Test 5: No tasks available
[6] Search Tasks (with empty task list)

# Expected: Message "No tasks available to search"
```

## File Modifications Summary

| File | Changes | Lines Affected (approx) |
|------|---------|------------------------|
| `src/todo/models.py` | Add Priority enum, update Task dataclass | +15 |
| `src/todo/services.py` | Add validation, search, filter, sort functions | +100 |
| `src/todo/storage.py` | Add wrapper methods | +20 |
| `src/todo/cli.py` | Add menus, update display formats | +150 |
| **Total** | | **~285 lines** |

## Common Issues and Solutions

### Issue: Import Error for Priority enum

**Error**: `NameError: name 'Priority' is not defined`

**Solution**: Ensure `Priority` enum is defined in `models.py` before `Task` dataclass and is imported in `services.py` and `cli.py`:
```python
from .models import Task, Priority  # Add Priority to import
```

### Issue: Category truncation in display

**Issue**: Long category names break table alignment

**Solution**: Implement truncation with ellipsis:
```python
def truncate(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text.ljust(max_len)
    return text[:max_len - 3].ljust(max_len - 3) + "..."
```

### Issue: Filter state not clearing

**Issue**: Filters persist when returning to main menu

**Solution**: This is expected behavior. Users can clear filters via Filter menu option 4. Add a note in the display:
```
Active filters: status=pending, priority=high
(Use [4] Clear All Filters in Filter Tasks menu to reset)
```

### Issue: Sorting filtered results

**Issue**: Sort applies to all tasks, not filtered set

**Solution**: Ensure `sort_tasks()` operates on the displayed (filtered) task list, not the full list:
```python
# In display sort menu:
current_tasks = get_display_tasks()  # May be filtered
sorted_tasks = sort_by_priority(current_tasks)
display_tasks(sorted_tasks)
```

## Backward Compatibility

### Testing with Existing Tasks

If you have existing tasks from Phase I (before priority/category):

1. Run the app with existing tasks in memory
2. Tasks should automatically get `priority=Priority.MEDIUM` and `category=None`
3. These tasks should appear in all views and operations

**Note**: In Phase I (in-memory only), compatibility is session-based. No database migration needed.

## Completion Checklist

- [ ] All Phase 1A-1E tasks completed
- [ ] All tests in Testing Guide pass
- [ ] Error messages are clear and user-friendly
- [ ] Table formatting displays correctly
- [ ] Existing Phase I features still work
- [ ] No import errors or runtime exceptions
- [ ] User can complete all new workflows without confusion

## Next Steps

After completing implementation:

1. Run manual testing for all features
2. Verify edge cases are handled correctly
3. Test backward compatibility with existing tasks
4. Update `README.md` with new feature documentation
5. Consider generating tasks for implementation via `/sp.tasks`

---

*This quickstart provides a roadmap for implementing intermediate Todo features.*
