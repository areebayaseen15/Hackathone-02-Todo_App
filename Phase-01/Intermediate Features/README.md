# Todo Application - Phase I

An in-memory Python console application for managing personal tasks.

## Overview

This is Phase I of the "Evolution of Todo" project - a simple command-line todo application that stores tasks in memory. Tasks are lost when the application exits.

## Features

### Core Features
- **Add Task**: Create new tasks with title, optional description, priority, and category
- **View Tasks**: Display all tasks in a formatted table with status, priority, and category
- **Update Task**: Modify task title, description, priority, and/or category
- **Delete Task**: Remove tasks with confirmation prompt
- **Mark as Completed**: Toggle task completion status

### Intermediate Features
- **Priorities**: Assign HIGH, MEDIUM, or LOW priority to tasks
- **Categories**: Tag tasks with categories for grouping (e.g., Work, Personal)
- **Search Tasks**: Find tasks by keyword in title or description (case-insensitive)
- **Filter Tasks**: Filter by status (pending/completed), priority, and category
- **Sort Tasks**: Sort by priority (HIGH→MEDIUM→LOW) or alphabetically (A→Z)

## Prerequisites

- Python 3.13 or higher
- UV package manager

## Installation

1. Clone repository:
   ```bash
   git clone <repository-url>
   cd todo-app
   ```

2. Install dependencies using UV:
   ```bash
   uv sync
   ```

## Usage

### Running the Application

Using UV:
```bash
uv run todo
```

Or using Python directly (on Windows):
```powershell
$env:PYTHONPATH="src"
python -m todo
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

### Adding a Task

1. Select option `1` from the menu
2. Enter a task title (required, 1-100 characters)
3. Enter a description (optional, up to 500 characters)
4. Enter a priority (high/medium/low, default: medium)
5. Enter a category (optional, up to 50 characters)
6. The task will be created with a unique ID

### Viewing Tasks

Select option `2` to see all tasks in a table format:

```
================================================================================
                              YOUR TASKS
================================================================================
ID     | Priority | Category   | Status        | Title                          | Created
------------------------------------------------------------------------------------
1      | HIGH      | Work       | [pending...]   | Complete project report         | 2025-12-29 10:30:00
2      | MEDIUM    | Personal   | [OK]          | Buy groceries                  | 2025-12-29 09:15:00
------------------------------------------------------------------------------------
Total: 2 tasks (1 completed, 1 pending)
================================================================================
```

Status indicators:
- `[pending...]` = Pending
- `[OK]` = Completed

### Updating a Task

1. Select option `3` from the menu
2. Enter the task ID to update
3. Enter new title (or press Enter to keep current)
4. Enter new description (or press Enter to keep current)
5. Enter new priority (or press Enter to keep current)
6. Enter new category (or press Enter to keep current)

### Deleting a Task

1. Select option `4` from the menu
2. Enter the task ID to delete
3. Confirm deletion when prompted

### Marking Task as Completed

1. Select option `5` from the menu
2. Enter the task ID to toggle
3. The task status will switch between complete and incomplete

### Searching Tasks

1. Select option `6` from the menu
2. Enter a keyword to search
3. Tasks matching the keyword in title or description will be displayed
4. Search is case-insensitive

### Filtering Tasks

1. Select option `7` from the menu
2. Choose a filter type:
   - `[1]` Filter by status (pending/completed/all)
   - `[2]` Filter by priority (high/medium/low/all)
   - `[3]` Filter by category (enter category name or 'all')
   - `[4]` Clear all filters
   - `[5]` Back to main menu
3. Multiple filters work together (AND logic)

### Sorting Tasks

1. Select option `8` from the menu
2. Choose a sort option:
   - `[1]` Sort by priority (HIGH → MEDIUM → LOW, newest first)
   - `[2]` Sort alphabetically (A → Z, newest first)
   - `[3]` Default order (by ID)

### Exiting

Select option `9` and confirm to exit. Note that all tasks will be lost.

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

Categories are optional and case-insensitive when filtering.

## Project Structure

```
todo-app/
├── CONSTITUTION.md          # Project governance document
├── CLAUDE.md                # Claude Code instructions
├── README.md                # This file
├── pyproject.toml           # Project configuration
├── specs/
│   ├── PHASE-I-SPEC.md      # Phase I specification
│   ├── PHASE-I-PLAN.md      # Phase I technical plan
│   ├── PHASE-I-TASKS.md     # Phase I task breakdown
│   └── 1-intermediate-features/  # Intermediate features spec
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── contracts/
│       ├── data-model.md
│       └── quickstart.md
└── src/
    └── todo/
        ├── __init__.py      # Package marker
        ├── __main__.py      # Package entry point
        ├── main.py          # Application entry point
        ├── models.py        # Task data model
        ├── storage.py       # In-memory storage
        ├── services.py      # Business logic
        └── cli.py           # CLI interface
```

## Constraints (Phase I)

- **In-memory storage only**: No database or file persistence
- **Single user**: No authentication or user management
- **Console interface**: No web or API interface
- **Standard library only**: No external dependencies

## License

This project is part of the Evolution of Todo hackathon project.
