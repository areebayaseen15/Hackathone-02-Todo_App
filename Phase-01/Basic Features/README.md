# Todo Application - Phase I

An in-memory Python console application for managing personal tasks.

## Overview

This is Phase I of the "Evolution of Todo" project - a simple command-line todo application that stores tasks in memory. Tasks are lost when the application exits.

## Features

- **Add Task**: Create new tasks with title and optional description
- **View Tasks**: Display all tasks in a formatted table with status indicators
- **Update Task**: Modify task title and/or description
- **Delete Task**: Remove tasks with confirmation prompt
- **Toggle Status**: Mark tasks as complete or incomplete

## Prerequisites

- Python 3.13 or higher
- UV package manager

## Installation

1. Clone the repository:
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

Or using Python directly:
```bash
uv run python -m todo
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
  [5] Toggle Task Status
  [6] Exit

Enter your choice (1-6):
```

### Adding a Task

1. Select option `1` from the menu
2. Enter a task title (required, 1-100 characters)
3. Enter a description (optional, up to 500 characters)
4. The task will be created with a unique ID

### Viewing Tasks

Select option `2` to see all tasks in a table format:

```
================================================================================
                              YOUR TASKS
================================================================================
ID    | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | [ ]         | Buy groceries                  | 2025-12-29 10:30:00
2     | [X]         | Call dentist                   | 2025-12-29 09:15:00
--------------------------------------------------------------------------------
Total: 2 tasks (1 completed, 1 pending)
================================================================================
```

Status indicators:
- `[ ]` = Pending
- `[X]` = Completed

### Updating a Task

1. Select option `3` from the menu
2. Enter the task ID to update
3. Enter new title (or press Enter to keep current)
4. Enter new description (or press Enter to keep current)

### Deleting a Task

1. Select option `4` from the menu
2. Enter the task ID to delete
3. Confirm deletion when prompted

### Toggling Task Status

1. Select option `5` from the menu
2. Enter the task ID to toggle
3. The task status will switch between complete and incomplete

### Exiting

Select option `6` and confirm to exit. Note that all tasks will be lost.

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
│   └── PHASE-I-TASKS.md     # Phase I task breakdown
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
