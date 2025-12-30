# Quickstart: Advanced Todo Features (Recurring Tasks & Due Dates)

**Feature**: Advanced Todo Features
**Branch**: `2-advanced-features`
**Date**: 2025-12-30

## Overview

This quickstart guide provides step-by-step instructions for implementing recurring tasks and due dates in the Phase I Todo App. Focus is on clean extension without breaking existing functionality.

---

## Prerequisites

- Python 3.13+ installed
- UV package manager installed
- Existing Todo App with Basic and Intermediate features working
- Approved specification: `specs/2-advanced-features/spec.md`
- Implementation plan: `specs/2-advanced-features/plan.md`

---

## Implementation Steps

### Step 1: Extend Data Model (`src/todo/models.py`)

**Action**: Add `Recurrence` enum and extend `Task` dataclass with new fields.

```python
# Add Recurrence enum
class Recurrence(Enum):
    """Recurrence patterns for tasks."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

# Extend Task dataclass
@dataclass
class Task:
    # ... existing fields ...
    due_date: Optional[datetime] = None
    recurrence: Recurrence = Recurrence.NONE
    parent_task_id: Optional[int] = None
```

**Add utility functions**:
```python
def format_due_date(due_date: Optional[datetime]) -> str:
    """Format due date for display."""
    if due_date is None:
        return "No due date"
    today = datetime.now().date()
    task_date = due_date.date()
    if task_date == today:
        return "TODAY"
    return due_date.strftime("%Y-%m-%d")

def is_overdue(due_date: Optional[datetime]) -> bool:
    """Check if task is overdue."""
    if due_date is None:
        return False
    today = datetime.now().date()
    return due_date.date() < today

def get_days_overdue(due_date: datetime) -> int:
    """Calculate days overdue."""
    today = datetime.now().date()
    task_date = due_date.date()
    delta = today - task_date
    return max(0, delta.days)

def calculate_next_due_date(current_date: datetime, recurrence: Recurrence) -> datetime:
    """Calculate next due date based on recurrence pattern."""
    from datetime import timedelta

    if recurrence == Recurrence.NONE:
        raise ValueError("Cannot calculate next date for non-recurring task")

    if recurrence == Recurrence.DAILY:
        return current_date + timedelta(days=1)

    if recurrence == Recurrence.WEEKLY:
        return current_date + timedelta(weeks=1)

    if recurrence == Recurrence.MONTHLY:
        year = current_date.year
        month = current_date.month + 1
        if month > 12:
            month = 1
            year += 1
        day = current_date.day
        last_day = (datetime(year, month + 1, 1) - timedelta(days=1)).day
        return datetime(year, month, min(day, last_day))

    raise ValueError(f"Unknown recurrence: {recurrence}")
```

**Update `ensure_task_compatibility()`**:
```python
def ensure_task_compatibility(task: Task) -> Task:
    """Ensure task has all required attributes."""
    # Existing logic for priority and category
    if not hasattr(task, 'priority'):
        task.priority = Priority.MEDIUM
    if not hasattr(task, 'category'):
        task.category = None

    # New attributes for advanced features
    if not hasattr(task, 'due_date'):
        task.due_date = None
    if not hasattr(task, 'recurrence'):
        task.recurrence = Recurrence.NONE
    if not hasattr(task, 'parent_task_id'):
        task.parent_task_id = None

    return task
```

---

### Step 2: Extend Service Layer (`src/todo/services.py`)

**Add validation functions**:
```python
def validate_due_date(date_str: str) -> Optional[datetime]:
    """Parse and validate due date string."""
    cleaned = date_str.strip()
    if not cleaned:
        return None

    if len(cleaned) != 10 or cleaned[4] != '-' or cleaned[7] != '-':
        raise ValueError(f"Invalid date format. Use YYYY-MM-DD. Got: '{date_str}'")

    try:
        year = int(cleaned[0:4])
        month = int(cleaned[5:7])
        day = int(cleaned[8:10])

        if month < 1 or month > 12:
            raise ValueError(f"Invalid month: {month}. Must be 01-12.")

        if day < 1 or day > 31:
            raise ValueError(f"Invalid day: {day}. Must be 01-31.")

        return datetime(year, month, day)

    except ValueError as e:
        if "must be" in str(e):
            raise
        raise ValueError(f"Invalid date: '{date_str}'. {str(e)}")

def validate_recurrence(recurrence_str: str) -> Recurrence:
    """Parse case-insensitive recurrence string to Recurrence enum."""
    cleaned = recurrence_str.strip().casefold()
    for recurrence in Recurrence:
        if recurrence.value == cleaned:
            return recurrence
    valid_values = ', '.join([r.value for r in Recurrence])
    raise ValueError(f"Invalid recurrence '{recurrence_str}'. Must be one of: {valid_values}")
```

**Update `add_task()`**:
```python
def add_task(
    self,
    title: str,
    description: str = "",
    priority_str: str = "medium",
    category_str: str = "",
    due_date_str: str = "",      # NEW
    recurrence_str: str = "none"    # NEW
) -> Task:
    # ... existing validation ...
    clean_due_date = validate_due_date(due_date_str)      # NEW
    clean_recurrence = validate_recurrence(recurrence_str)  # NEW

    task = Task(
        id=0,
        title=clean_title,
        description=clean_description,
        is_completed=False,
        created_at=datetime.now(),
        priority=clean_priority,
        category=clean_category,
        due_date=clean_due_date,         # NEW
        recurrence=clean_recurrence,        # NEW
        parent_task_id=None
    )

    return self._storage.add(task)
```

**Update `update_task()`**:
```python
def update_task(
    self,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    priority_str: str | None = None,
    category_str: str | None = None,
    due_date_str: str | None = None,     # NEW
    recurrence_str: str | None = None    # NEW
) -> Task | None:
    # ... existing task retrieval ...
    if due_date_str is not None:
        if due_date_str.strip():
            task.due_date = validate_due_date(due_date_str)
        else:
            task.due_date = None

    if recurrence_str is not None:
        task.recurrence = validate_recurrence(recurrence_str)

    self._storage.update(task)
    return task
```

**Update `toggle_task()`**:
```python
def toggle_task(self, task_id: int) -> tuple[Task, Task | None]:
    """Toggle task completion, create next occurrence if recurring."""
    task = self._storage.get_by_id(task_id)
    if task is None:
        return (None, None)

    ensure_task_compatibility(task)
    task.is_completed = not task.is_completed
    self._storage.update(task)

    # Check if we need to create next occurrence
    next_task = None
    if (task.is_completed and
        task.recurrence != Recurrence.NONE and
        task.due_date is not None):

        next_date = calculate_next_due_date(task.due_date, task.recurrence)
        next_task = Task(
            id=0,
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
        next_task = self._storage.add(next_task)

    return (task, next_task)
```

---

### Step 3: Extend CLI Layer (`src/todo/cli.py`)

**Add imports**:
```python
from todo.models import format_due_date, is_overdue, Recurrence
```

**Update `display_task_list()`**:
```python
def display_task_list(tasks: list[Task], title: str = "YOUR TASKS") -> None:
    """Display tasks in tabular format with enhanced columns."""
    print(\"\n\" + \"=\" * 80)
    print(f\"{title:^80}\")
    print(\"=\" * 80)
    print(\"ID    | Priority | Due Date    | Status      | Title                          | Created\")
    print(\"-\" * 80)

    for task in tasks:
        status = \"[X]\" if task.is_completed else \"[ ]\"

        # Format due date
        if task.due_date is None:
            due_str = \"No due date\"
        else:
            due_str = format_due_date(task.due_date)
            # Check for overdue
            if is_overdue(task.due_date) and not task.is_completed:
                status += \" OVERDUE"

        title_display = task.title[:30] if len(task.title) > 30 else task.title
        created_str = task.created_at.strftime(\"%Y-%m-%d %H:%M:%S\")

        print(f\"{task.id:<6}| {task.priority:<9}| {due_str:<12}| {status:<12}| {title_display:<30}| {created_str}\")

    completed = sum(1 for t in tasks if t.is_completed)
    pending = len(tasks) - completed
    overdue = sum(1 for t in tasks if not t.is_completed and t.due_date and is_overdue(t.due_date))

    print(\"-\" * 80)
    print(f\"Total: {len(tasks)} tasks ({completed} completed, {pending} pending, {overdue} overdue)\")
    print(\"=\" * 80)
```

**Update `add_task()`**:
```python
def add_task(service: TaskService) -> None:
    \"\"\"Add a new task with due date and recurrence options.\"\"\"
    print(\"\n\" + \"=\" * 80)
    print(\"                              ADD TASK\")
    print(\"=\" * 80)

    title = input(\"Enter task title: \")
    description = input(\"Enter task description (optional, press Enter to skip): \")
    priority = input(\"Enter priority (high/medium/low, default: medium): \") or \"medium\"
    category = input(\"Enter category (optional, press Enter to skip): \")
    due_date = input(\"Enter due date (YYYY-MM-DD, optional, press Enter to skip): \")      # NEW
    recurrence = input(\"Enter recurrence (none/daily/weekly/monthly, default: none): \") or \"none\"  # NEW

    try:
        task = service.add_task(
            title=title,
            description=description,
            priority_str=priority,
            category_str=category,
            due_date_str=due_date,       # NEW
            recurrence_str=recurrence      # NEW
        )

        print(\"\n\" + \"=\" * 80)
        print(\"Task created successfully!\")
        print(f\"ID: {task.id}\")
        print(f\"Title: {task.title}\")
        print(f\"Description: {task.description or 'No description'}\")
        print(f\"Priority: {task.priority}\")
        print(f\"Category: {task.category or 'No category'}\")
        print(f\"Due Date: {format_due_date(task.due_date)}\")        # NEW
        print(f\"Recurrence: {task.recurrence}\")                       # NEW
        print(f\"Status: [{'X' if task.is_completed else ' '}] pending\")
        print(f\"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}\")
        print(\"=\" * 80)

    except ValidationError as e:
        print(f\"\nError: {e.message}\")

    input(\"\nPress Enter to continue...\")
```

**Update `toggle_task()`**:
```python
def toggle_task(service: TaskService) -> None:
    \"\"\"Toggle task completion with recurring task support.\"\"\"
    print(\"\n\" + \"=\" * 80)
    print(\"                          TOGGLE TASK\")
    print(\"=\" * 80)

    task_id_str = input(\"Enter task ID to toggle status: \")

    try:
        task_id = int(task_id_str)
        task, next_task = service.toggle_task(task_id)    # Updated to return tuple

        if task is None:
            print(f\"\nError: Task with ID {task_id} not found\")
            input(\"Press Enter to continue...\")
            return

        if next_task:
            print(\"\nTask completed! Next occurrence created.\")
            print(f\"New task ID: {next_task.id}\")
            print(f\"Next due date: {format_due_date(next_task.due_date)}\")
            print()
            print(\"Original Task:\")
            print(f\"ID: {task.id}\")
            print(f\"Title: {task.title}\")
            print(f\"Recurrence: {task.recurrence}\")
            print(f\"Due Date: {format_due_date(task.due_date)}\")
            print(f\"Status: [{'X' if task.is_completed else ' '}] completed\")
            print()
            print(\"Next Occurrence:\")
            print(f\"ID: {next_task.id}\")
            print(f\"Title: {next_task.title}\")
            print(f\"Recurrence: {next_task.recurrence}\")
            print(f\"Due Date: {format_due_date(next_task.due_date)}\")
            print(f\"Status: [{'X' if next_task.is_completed else ' '}] pending\")
            print(f\"Parent Task ID: {task.id}\")
        else:
            print(\"\nTask status updated!\")
            print(f\"ID: {task.id}\")
            print(f\"Title: {task.title}\")
            print(f\"Status: [{'X' if task.is_completed else ' '}] completed\" if task.is_completed else f\"Status: [{' ' if not task.is_completed else 'X'}] pending\")

    except ValueError:
        print(\"\nError: Task ID must be a number\")

    print(\"=\" * 80)
    input(\"Press Enter to continue...\")
```

---

## Testing

### Manual Test Scenarios

1. **Create task with due date and recurrence**
   - Run app → Add Task
   - Enter: "Weekly meeting", due date "2025-12-30", recurrence "weekly"
   - Verify: Task created with due date and WEEKLY recurrence

2. **Complete recurring task**
   - Find task with recurrence
   - Toggle task to complete
   - Verify: New task created with next due date (7 days later)
   - Verify: parent_task_id set to original task ID

3. **Create task without due date**
   - Run app → Add Task
   - Leave due date empty
   - Verify: Task created with due_date=None

4. **Create recurring task without due date**
   - Run app → Add Task
   - Enter recurrence "daily", leave due date empty
   - Complete task
   - Verify: No new occurrence created

5. **Test invalid date format**
   - Run app → Add Task
   - Enter due date "12/30/2025"
   - Verify: Error message displayed

6. **Test invalid calendar date**
   - Run app → Add Task
   - Enter due date "2025-02-31"
   - Verify: Error message displayed

7. **Test leap year date**
   - Run app → Add Task
   - Enter due date "2024-02-29" (leap year)
   - Verify: Task created successfully

8. **Test non-leap year date**
   - Run app → Add Task
   - Enter due date "2025-02-29" (non-leap year)
   - Verify: Error message displayed

9. **View task list with overdue**
   - Create task with past due date
   - View all tasks
   - Verify: OVERDUE indicator shown in status column

10. **View task list with today's due date**
    - Create task with today's date
    - View all tasks
    - Verify: TODAY shown in due date column

---

## Common Issues & Solutions

| Issue | Solution |
|--------|-----------|
| "ImportError: Recurrence not defined" | Add `Recurrence` enum to `models.py` before using in services |
| "ValueError: day is out of range" | Check date validation logic - ensure proper year/month/day parsing |
| Recurring task not creating next occurrence | Verify task has both recurrence != NONE and due_date is set |
| Overdue indicator not showing | Verify `is_overdue()` is called in display function |
| Backward compatibility error with old tasks | Ensure `ensure_task_compatibility()` is called in all task retrieval functions |

---

## Next Steps

After implementing recurring tasks and due dates:

1. **Run manual tests** - Verify all test scenarios pass
2. **Validate against spec** - Check spec.md requirements are met
3. **Check backward compatibility** - Ensure existing tasks still work
4. **Proceed to analytics and smart views** - When ready, implement remaining advanced features

---

**Note**: This implementation excludes analytics and smart views per user's `/sp.plan` request. Those features will be implemented in a separate phase when approved.
