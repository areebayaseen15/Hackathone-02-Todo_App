# Contract: View Task Analytics

**Feature**: Advanced Todo Features
**Contract ID**: ADV-003
**Date**: 2025-12-30

## Purpose

Define the contract for displaying task analytics including total counts, completion rates, overdue counts, and breakdowns by priority and category.

## Actors

- **User**: Requests to view task analytics
- **CLI**: Displays formatted analytics output
- **Service**: Calculates analytics from task collection
- **Storage**: Provides access to all tasks

## Pre-Conditions

1. Application is running
2. User has selected "View Analytics" from main menu

## Input Specification

No user input required. Analytics are calculated automatically from current task collection.

## Processing

### Step 1: Retrieve All Tasks
- Call `storage.get_all()`
- Return list of all tasks

### Step 2: Ensure Task Compatibility
- For each task, call `ensure_task_compatibility(task)`
- Set default values for missing attributes (due_date, recurrence, parent_task_id)

### Step 3: Calculate Basic Statistics
```python
total_tasks = len(tasks)
completed_tasks = sum(1 for t in tasks if t.is_completed)
pending_tasks = total_tasks - completed_tasks
```

### Step 4: Calculate Overdue Count
```python
today = datetime.now().date()
overdue_tasks = sum(
    1 for t in tasks
    if not t.is_completed and t.due_date and t.due_date.date() < today
)
```

### Step 5: Calculate Completion Percentage
```python
if total_tasks > 0:
    completed_percentage = (completed_tasks / total_tasks) * 100.0
else:
    completed_percentage = 0.0
```

### Step 6: Calculate Priority Breakdown
```python
priority_breakdown = {
    Priority.HIGH: 0,
    Priority.MEDIUM: 0,
    Priority.LOW: 0
}

for task in tasks:
    priority_breakdown[task.priority] += 1

# Calculate overdue per priority
priority_overdue = {}
for priority in Priority:
    priority_overdue[priority] = sum(
        1 for t in tasks
        if (t.priority == priority and not t.is_completed
            and t.due_date and t.due_date.date() < today)
    )
```

### Step 7: Calculate Category Breakdown
```python
category_breakdown = {}

for task in tasks:
    if task.category:
        category_breakdown[task.category] = \
            category_breakdown.get(task.category, 0) + 1

# Sort categories alphabetically
category_breakdown = dict(sorted(category_breakdown.items()))
```

### Step 8: Return Analytics Object
```python
return TaskAnalytics(
    total_tasks=total_tasks,
    completed_count=completed_tasks,
    pending_count=pending_tasks,
    overdue_count=overdue_tasks,
    completed_percentage=completed_percentage,
    priority_breakdown=priority_breakdown,
    category_breakdown=category_breakdown
)
```

## Output Specification

### Success Response - With Tasks

```
================================================================================
                           TASK ANALYTICS
================================================================================
Total Tasks: {total_tasks}
Completed: {completed_count} tasks ({completed_percentage}%)
Pending: {pending_count} tasks ({pending_percentage}%)
Overdue: {overdue_count} tasks

Breakdown by Priority:
  HIGH:   {high_count} tasks ({high_overdue_count} overdue)
  MEDIUM: {medium_count} tasks ({medium_overdue_count} overdue)
  LOW:    {low_count} tasks ({low_overdue_count} overdue)

Breakdown by Category:
  {category_1}:    {count_1} tasks
  {category_2}:    {count_2} tasks
  ...
================================================================================
Press Enter to continue...
```

### Success Response - No Tasks

```
================================================================================
                           TASK ANALYTICS
================================================================================
Total Tasks: 0
Completed: 0 tasks (0.0%)
Pending: 0 tasks (0.0%)
Overdue: 0 tasks

Breakdown by Priority:
  HIGH:   0 tasks (0 overdue)
  MEDIUM: 0 tasks (0 overdue)
  LOW:    0 tasks (0 overdue)

Breakdown by Category:
  (No categories)
================================================================================
Press Enter to continue...
```

### Success Response - No Categories

```
================================================================================
                           TASK ANALYTICS
================================================================================
Total Tasks: 5
Completed: 2 tasks (40.0%)
Pending: 3 tasks (60.0%)
Overdue: 1 tasks

Breakdown by Priority:
  HIGH:   1 tasks (1 overdue)
  MEDIUM: 3 tasks (0 overdue)
  LOW:    1 tasks (0 overdue)

Breakdown by Category:
  (No categories - all tasks have no category)
================================================================================
Press Enter to continue...
```

## Post-Conditions

1. Analytics are displayed to user
2. No modifications to task data
3. Analytics reflect current state only (no historical tracking)

## Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| No tasks in storage | All counts show 0, percentages show 0.0% |
| All tasks completed | Pending = 0, Overdue = 0 |
| All tasks pending | Completed = 0 |
| Tasks with no due dates | Overdue count excludes them |
| Tasks with no categories | Category breakdown shows "(No categories)" |
| Categories with different cases | Treated as different categories (case-sensitive) |
| Tasks in single category | Show that category with count |

## Examples

### Example 1: Mixed Task States

**Current Tasks**:
- 15 total tasks
- 6 completed, 9 pending
- 2 overdue
- Priority breakdown: 3 HIGH (2 overdue), 8 MEDIUM (0 overdue), 4 LOW (0 overdue)
- Category breakdown: work=6, personal=5, shopping=2, health=2

**Output**:
```
================================================================================
                           TASK ANALYTICS
================================================================================
Total Tasks: 15
Completed: 6 tasks (40.0%)
Pending: 9 tasks (60.0%)
Overdue: 2 tasks

Breakdown by Priority:
  HIGH:   3 tasks (2 overdue)
  MEDIUM: 8 tasks (0 overdue)
  LOW:    4 tasks (0 overdue)

Breakdown by Category:
  health:    2 tasks
  personal:   5 tasks
  shopping:   2 tasks
  work:       6 tasks
================================================================================
Press Enter to continue...
```

### Example 2: All Tasks Completed

**Current Tasks**: 10 tasks, all completed

**Output**:
```
================================================================================
                           TASK ANALYTICS
================================================================================
Total Tasks: 10
Completed: 10 tasks (100.0%)
Pending: 0 tasks (0.0%)
Overdue: 0 tasks

Breakdown by Priority:
  HIGH:   2 tasks (0 overdue)
  MEDIUM: 5 tasks (0 overdue)
  LOW:    3 tasks (0 overdue)

Breakdown by Category:
  work:      6 tasks
  personal:   4 tasks
================================================================================
Press Enter to continue...
```

### Example 3: Empty Task List

**Current Tasks**: None

**Output**:
```
================================================================================
                           TASK ANALYTICS
================================================================================
Total Tasks: 0
Completed: 0 tasks (0.0%)
Pending: 0 tasks (0.0%)
Overdue: 0 tasks

Breakdown by Priority:
  HIGH:   0 tasks (0 overdue)
  MEDIUM: 0 tasks (0 overdue)
  LOW:    0 tasks (0 overdue)

Breakdown by Category:
  (No categories)
================================================================================
Press Enter to continue...
```

### Example 4: Tasks Without Categories

**Current Tasks**: 5 tasks, none have categories

**Output**:
```
================================================================================
                           TASK ANALYTICS
================================================================================
Total Tasks: 5
Completed: 3 tasks (60.0%)
Pending: 2 tasks (40.0%)
Overdue: 0 tasks

Breakdown by Priority:
  HIGH:   1 tasks (0 overdue)
  MEDIUM: 2 tasks (0 overdue)
  LOW:    2 tasks (0 overdue)

Breakdown by Category:
  (No categories - all tasks have no category)
================================================================================
Press Enter to continue...
```

## Test Cases

### TC-001: Analytics with mixed states
- **Input**: Mix of completed, pending, overdue tasks
- **Expected**: Correct counts and percentages

### TC-002: Analytics with all completed
- **Input**: All tasks completed
- **Expected**: Completed = total, Pending = 0, Overdue = 0, Percentage = 100%

### TC-003: Analytics with all pending
- **Input**: All tasks pending
- **Expected**: Completed = 0, Pending = total, Percentage = 0%

### TC-004: Analytics with no tasks
- **Input**: Empty task list
- **Expected**: All counts = 0, percentages = 0%

### TC-005: Priority breakdown accuracy
- **Input**: Tasks with different priorities
- **Expected**: Correct count per priority level

### TC-006: Priority overdue calculation
- **Input**: Mix of overdue and not overdue by priority
- **Expected**: Correct overdue count per priority

### TC-007: Category breakdown with categories
- **Input**: Tasks with various categories
- **Expected**: Correct count per category, sorted alphabetically

### TC-008: Category breakdown without categories
- **Input**: All tasks have no category
- **Expected**: Display "(No categories - all tasks have no category)"

### TC-009: Category breakdown partial categories
- **Input**: Some tasks with categories, some without
- **Expected**: Only categorized tasks appear in breakdown

### TC-010: Percentage calculation rounding
- **Input**: 7 tasks, 3 completed
- **Expected**: 42.857...% → Display as 42.9% or 42.86%

### TC-011: Due date tasks overdue detection
- **Input**: Tasks with past due dates
- **Expected**: Correctly counted as overdue

### TC-012: Due date tasks not overdue
- **Input**: Tasks with future or today's due dates
- **Expected**: Not counted as overdue

### TC-013: No due date tasks
- **Input**: Tasks without due dates
- **Expected**: Not counted in overdue (even if old)
