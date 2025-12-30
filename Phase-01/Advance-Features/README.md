# Todo Application - Phase I

An in-memory Python console application for managing personal tasks with advanced scheduling features.

## Overview

This is Phase I of the "Evolution of Todo" project - a command-line todo application with in-memory storage. Tasks are lost when the application exits.

## Features

### Core Features
- **Add Task**: Create new tasks with title, optional description, priority, category, due date, and recurrence
- **View Tasks**: Display all tasks in a formatted table with status, priority, category, and due date
- **Update Task**: Modify task title, description, priority, category, due date, and/or recurrence
- **Delete Task**: Remove tasks with confirmation prompt
- **Mark as Completed**: Toggle task completion status

### Intermediate Features
- **Priorities**: Assign HIGH, MEDIUM, or LOW priority to tasks
- **Categories**: Tag tasks with categories for grouping (e.g., Work, Personal)
- **Search Tasks**: Find tasks by keyword in title or description (case-insensitive)
- **Filter Tasks**: Filter by status (pending/completed), priority, and category
- **Sort Tasks**: Sort by priority (HIGH→MEDIUM→LOW) or alphabetically (A→Z)

### Advanced Features
- **Due Dates**: Set optional due dates for tasks in YYYY-MM-DD format
- **Overdue Detection**: Tasks past their due date show `[OVERDUE]` indicator
- **Today Display**: Tasks due today show "TODAY" instead of the date
- **Recurring Tasks**: Set tasks to repeat daily, weekly, or monthly
- **Auto Next Occurrence**: When a recurring task is completed, the next occurrence is automatically created
- **Parent Task Tracking**: Recurring tasks maintain a link to their original task via `parent_task_id`

## Prerequisites

- Python 3.13 or higher
- UV package manager (optional, for dependency management)

## Installation

1. Clone repository:
   ```bash
   git clone <repository-url>
   cd todo-app
   ```

2. Install dependencies using UV (optional):
   ```bash
   uv sync
   ```

## Usage

### Running the Application

On Windows (using Python directly):
```powershell
cd "C:\Users\Office\Desktop\Phase-01\Advance Features\src"
python -m todo.main
```

Using UV (if configured):
```bash
uv run todo
```

### Menu Options

When you start the application, you'll see the main menu:

```
================================================================================
                         TODO APPLICATION - PHASE I
================================================================================

Please select an option:

  [1] Add Task
  [2] View Tasks
  [3] Update Task
  [4] Delete Task
  [5] Mark as Completed
  [6] Search Tasks
  [7] Filter Tasks
  [8] Sort Tasks
  [9] Exit

Enter your choice (1-9):
```

---

## Detailed Usage Guide

### Adding a Task

1. Select option `1` from the menu
2. Enter the following information:
   - **Title** (required, 1-100 characters)
   - **Description** (optional, up to 500 characters)
   - **Priority** (high/medium/low, default: medium)
   - **Category** (optional, up to 50 characters)
   - **Due Date** (optional, YYYY-MM-DD format)
   - **Recurrence** (none/daily/weekly/monthly, default: none)
3. The task will be created with a unique ID

**Example:**
```
Enter task title: Weekly team meeting
Enter description (optional, press Enter to skip): Discuss project progress
Enter priority (high/medium/low, default: medium): high
Enter category (optional, press Enter to skip): Work
Enter due date (YYYY-MM-DD, optional, press Enter to skip): 2026-01-06
Enter recurrence (none/daily/weekly/monthly, default: none): weekly
```

### Viewing Tasks

Select option `2` to see all tasks in a table format:

```
================================================================================
                              YOUR TASKS
================================================================================
ID     | Priority  | Category   | Due Date     | Status          | Title
--------------------------------------------------------------------
1      | HIGH      | Work       | 2026-01-06  | [pending...]     | Weekly team meeting
2      | MEDIUM    | Personal   | TODAY        | [pending...]     | Buy groceries
3      | LOW       | Work       | No due date   | [OK]            | Complete report
4      | MEDIUM    | Work       | 2025-12-20  | [OVERDUE]       | Submit timesheet
--------------------------------------------------------------------
Total: 4 tasks (1 completed, 3 pending, 1 overdue)
================================================================================
```

**Status indicators:**
- `[pending...]` = Pending task
- `[OK]` = Completed task
- `[OVERDUE]` = Past-due pending task (shows red in supported terminals)

**Due date displays:**
- `TODAY` = Task is due today
- `YYYY-MM-DD` = Task due date in calendar format
- `No due date` = Task has no due date set

### Updating a Task

1. Select option `3` from the menu
2. Enter the task ID to update
3. Review current task details
4. Enter new values for any fields you want to change (press Enter to keep current)
5. To clear a due date, press Enter at the prompt
6. The task will be updated

**Example:**
```
Current task details:
  ID:          1
  Title:       Weekly team meeting
  ...
  Due Date:     2026-01-06
  Recurrence:   WEEKLY

Current title: Weekly team meeting
New title (press Enter to keep current): Monthly team sync
New due date YYYY-MM-DD (press Enter to keep current, empty then Enter to clear): 2026-02-03
Current recurrence: weekly
New recurrence (press Enter to keep current): monthly
```

### Deleting a Task

1. Select option `4` from the menu
2. Enter the task ID to delete
3. Review the task details
4. Confirm deletion when prompted (`y` to delete, anything else to cancel)

### Marking Task as Completed

1. Select option `5` from the menu
2. Enter the task ID to toggle
3. For recurring tasks with a due date, the next occurrence will be automatically created

**Recurring Task Example:**
```
Task #1 marked as complete

============================================================
  Next occurrence created automatically!
============================================================
  New Task ID:       2
  Parent Task ID:    1
  Next Due Date:     2026-01-13
  Recurrence:        WEEKLY
============================================================
```

### Searching Tasks

1. Select option `6` from the menu
2. Enter a keyword to search
3. Tasks matching the keyword in title or description will be displayed
4. Search is case-insensitive

**Example:**
```
Enter keyword to search: meeting
```

### Filtering Tasks

1. Select option `7` from the menu
2. Choose a filter type:
   - `[1]` Filter by status (pending/completed/all)
   - `[2]` Filter by priority (high/medium/low/all)
   - `[3]` Filter by category (enter category name or 'all')
   - `[4]` Clear all filters
   - `[5]` Back to main menu
3. Multiple filters work together (AND logic)

**Example:**
```
Available filters:
  [1] By Status (pending/completed)
  [2] By Priority (high/medium/low)
  [3] By Category
  [4] Clear All Filters
  [5] Back to Main Menu

Active filters: status=pending, priority=high
Showing 2 tasks with current filters:
```

### Sorting Tasks

1. Select option `8` from the menu
2. Choose a sort option:
   - `[1]` Sort by priority (HIGH → MEDIUM → LOW, newest first)
   - `[2]` Sort alphabetically (A → Z, newest first)
   - `[3]` Default order (by ID)

### Exiting

Select option `9` and confirm to exit. Note that all tasks will be lost when you exit (in-memory storage).

---

## Advanced Features Explained

### Due Dates

Due dates help you track when tasks need to be completed:
- **Format**: YYYY-MM-DD (e.g., 2026-01-15)
- **Validation**: Invalid dates or formats are rejected with clear error messages
- **Leap Years**: Correctly handles February 29th for leap years (2024) and rejects for non-leap years (2025)

**Example dates:**
- `2026-01-31` - January 31st, valid
- `2026-02-28` - February 28th, valid
- `2024-02-29` - February 29th, valid (leap year)
- `2025-02-29` - Invalid (not a leap year)
- `12/31/2025` - Invalid format (must be YYYY-MM-DD)

### Overdue Detection

The application automatically identifies overdue tasks:
- **Condition**: Task is pending AND due date is in the past
- **Display**: Shows `[OVERDUE]` in status column
- **Summary**: Includes overdue count in task list summary
- **Color**: May appear red in supported terminal applications

### Recurring Tasks

Recurring tasks automatically create the next occurrence when completed:

**Recurrence Patterns:**
- `none` (default) - Task does not repeat
- `daily` - Creates next task one day after due date
- `weekly` - Creates next task one week after due date
- `monthly` - Creates next task one month after due date

**Requirements for auto-creation:**
1. Task must have a due date set
2. Task must have recurrence pattern other than `none`
3. Task is being marked as completed (going from pending → complete)

**Monthly Edge Cases:**
- January 31 → February 28 (or 29 in leap year)
- March 31 → April 30 (adjusts to end of month)
- Correctly handles months with different numbers of days

**Example Workflow:**
```
1. Create: Task "Pay rent" due: 2026-01-01, recurrence: monthly
2. Complete: Task #1 on 2026-01-01
3. Auto-create: Task #2 due: 2026-02-01, parent: 1
4. Complete: Task #2 on 2026-02-01
5. Auto-create: Task #3 due: 2026-03-01, parent: 1
```

### Parent Task Tracking

Recurring tasks maintain their relationship to the original task:
- `parent_task_id` is set on all auto-created occurrences
- First task in chain has no parent
- Subsequent tasks point back to original
- Helps track the origin of recurring task instances

---

## Task Priorities

- **HIGH**: Urgent tasks that need immediate attention
- **MEDIUM**: Normal priority tasks (default)
- **LOW**: Tasks that can be done later

## Categories

Categories help organize tasks by project or context. Examples:
- `Work` - Work-related tasks
- `Personal` - Personal tasks
- `Shopping` - Shopping lists
- `Health` - Health and fitness tasks
- `Finance` - Bill payments, budget tasks

Categories are optional and case-insensitive when filtering.

---

## Complete Example Session

```
================================================================================
          WELCOME TO TODO APPLICATION - PHASE I
          In-Memory Console Version
================================================================================

================================================================================
                         TODO APPLICATION - PHASE I
================================================================================

Please select an option:
  [1] Add Task
  [2] View Tasks
  [3] Update Task
  [4] Delete Task
  [5] Mark as Completed
  [6] Search Tasks
  [7] Filter Tasks
  [8] Sort Tasks
  [9] Exit

Enter your choice (1-9): 1

----------------------------------------
           ADD NEW TASK
----------------------------------------

Enter task title: Weekly standup meeting
Enter description (optional, press Enter to skip): Team progress sync
Enter priority (high/medium/low, default: medium): high
Enter category (optional, press Enter to skip): Work
Enter due date (YYYY-MM-DD, optional, press Enter to skip): 2026-01-06
Enter recurrence (none/daily/weekly/monthly, default: none): weekly

  SUCCESS: Task #1 created successfully!

  ID:          1
  Title:       Weekly standup meeting
  Description: Team progress sync
  Priority:     HIGH
  Category:     Work
  Due Date:     2026-01-06
  Recurrence:   WEEKLY
  Status:      Pending
  Created:     2025-12-30 14:30:00
```

---

## Project Structure

```
todo-app/
├── CONSTITUTION.md          # Project governance document
├── CLAUDE.md                # Claude Code instructions
├── README.md                # This file
├── pyproject.toml           # Project configuration
├── specs/
│   ├── 2-advanced-features/ # Advanced features specification
│   │   ├── spec.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── contracts/
│   │   ├── data-model.md
│   │   ├── quickstart.md
│   │   └── research.md
│   └── 1-intermediate-features/  # Intermediate features spec
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
└── src/
     └── todo/
        ├── __init__.py      # Package marker
        ├── __main__.py      # Package entry point
        ├── main.py          # Application entry point
        ├── models.py        # Task data model with enums and utilities
        ├── storage.py       # In-memory storage
        ├── services.py      # Business logic with validation
        └── cli.py           # CLI interface with menu handlers
```

## Constraints (Phase I)

- **In-memory storage only**: No database or file persistence
- **Single user**: No authentication or user management
- **Console interface**: No web or API interface
- **Standard library only**: No external dependencies beyond Python standard library

## Tips for Effective Use

1. **Use Categories**: Group related tasks (Work, Personal, etc.) for easier filtering
2. **Set Due Dates**: Keep track of deadlines with the overdue indicator
3. **Use Recurrence**: For repeating tasks (weekly meetings, monthly bills), set recurrence to auto-create next instances
4. **Set Priorities**: Use priorities to focus on what's most important
5. **Filter and Sort**: Use filters to focus on specific tasks, sort by priority when planning your day
6. **Regular Updates**: Update tasks as information changes (due dates, priorities)

## License

This project is part of the Evolution of Todo hackathon project.
