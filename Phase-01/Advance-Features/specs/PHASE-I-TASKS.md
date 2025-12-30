# Phase I Implementation Tasks

> **Task Breakdown Document**
> Version: 1.0
> Phase: I
> Status: DRAFT - PENDING APPROVAL
> Plan Reference: specs/PHASE-I-PLAN.md v1.0
> Specification Reference: specs/PHASE-I-SPEC.md v1.0
> Constitution Reference: CONSTITUTION.md v1.0

---

## Task Overview

| Group | Description | Task Count |
|-------|-------------|------------|
| G1 | Project Setup | 3 |
| G2 | Data Model & Storage | 4 |
| G3 | Service Layer Foundation | 3 |
| G4 | CLI Foundation | 4 |
| G5 | Add Task Feature | 2 |
| G6 | View Tasks Feature | 2 |
| G7 | Update Task Feature | 2 |
| G8 | Delete Task Feature | 2 |
| G9 | Toggle Status Feature | 2 |
| G10 | Application Entry & Exit | 3 |
| G11 | Documentation | 2 |
| **Total** | | **29** |

---

## Group 1: Project Setup

### Task T1.1: Initialize UV Project

**Task ID**: T1.1
**Description**: Initialize the Python project using UV package manager with proper configuration.

**Preconditions**:
- UV is installed on the system
- Working directory is `todo-app/`

**Expected Output**:
- Valid `pyproject.toml` file with project metadata
- Python 3.13+ specified as minimum version
- Project name: `todo`
- No external dependencies (stdlib only)

**Artifacts**:
- CREATE: `pyproject.toml`

**References**:
- Spec Section 7: Technology Requirements
- Plan Section 8: Task Group 1

**Acceptance Criteria**:
- [ ] pyproject.toml exists and is valid
- [ ] Python version >= 3.13 specified
- [ ] No external dependencies listed
- [ ] Project metadata complete (name, version, description)

---

### Task T1.2: Create Directory Structure

**Task ID**: T1.2
**Description**: Create the project directory structure as defined in the specification.

**Preconditions**:
- T1.1 completed
- `pyproject.toml` exists

**Expected Output**:
- Complete directory structure matching specification
- All necessary directories created

**Artifacts**:
- CREATE: `src/` directory
- CREATE: `src/todo/` directory

**Directory Structure**:
```
todo-app/
├── CONSTITUTION.md      (exists)
├── pyproject.toml       (from T1.1)
├── specs/               (exists)
└── src/
    └── todo/
```

**References**:
- Spec Section 6: Project Structure
- Plan Section 8: Task Group 1

**Acceptance Criteria**:
- [ ] `src/` directory exists
- [ ] `src/todo/` directory exists

---

### Task T1.3: Create Package Init Files

**Task ID**: T1.3
**Description**: Create `__init__.py` files to make `todo` a proper Python package.

**Preconditions**:
- T1.2 completed
- Directory structure exists

**Expected Output**:
- Package marker file with version info

**Artifacts**:
- CREATE: `src/todo/__init__.py`

**File Content**:
```python
"""Todo Application - Phase I: In-Memory Console App"""

__version__ = "1.0.0"
```

**References**:
- Spec Section 6: Project Structure
- Plan Section 8: Task Group 1

**Acceptance Criteria**:
- [ ] `__init__.py` exists in `src/todo/`
- [ ] Package is importable
- [ ] Version string defined

---

## Group 2: Data Model & Storage

### Task T2.1: Implement Task Dataclass

**Task ID**: T2.1
**Description**: Create the Task data model as a Python dataclass with all required fields.

**Preconditions**:
- T1.3 completed
- Package structure exists

**Expected Output**:
- Task dataclass with 5 fields
- Proper type hints
- Immutable ID and created_at fields

**Artifacts**:
- CREATE: `src/todo/models.py`

**Implementation Details**:
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
```

**References**:
- Spec Section 2: Task Data Model
- Spec Section 2.1: Task Entity
- Plan Section 3.1: Task Model Implementation

**Acceptance Criteria**:
- [ ] Task dataclass created
- [ ] All 5 fields present: id, title, description, is_completed, created_at
- [ ] Correct type hints for each field
- [ ] Dataclass is importable

---

### Task T2.2: Implement TaskStorage Class - Core Structure

**Task ID**: T2.2
**Description**: Create the TaskStorage class with internal data structures for storing tasks.

**Preconditions**:
- T2.1 completed
- Task model exists

**Expected Output**:
- TaskStorage class with `_tasks` list and `_next_id` counter
- Constructor initializes empty storage

**Artifacts**:
- CREATE: `src/todo/storage.py`

**Implementation Details**:
```python
class TaskStorage:
    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """Generate next unique ID"""
        current_id = self._next_id
        self._next_id += 1
        return current_id
```

**References**:
- Spec Section 2.1: ID field (Unique, Auto-generated, Positive)
- Plan Section 3.2: Storage Implementation
- Plan Section 4: Task Identification Strategy

**Acceptance Criteria**:
- [ ] TaskStorage class created
- [ ] `_tasks` list initialized empty
- [ ] `_next_id` starts at 1
- [ ] `_generate_id()` returns sequential IDs

---

### Task T2.3: Implement TaskStorage - CRUD Operations

**Task ID**: T2.3
**Description**: Implement Create, Read, Update, Delete operations on TaskStorage.

**Preconditions**:
- T2.2 completed
- TaskStorage class exists

**Expected Output**:
- All CRUD methods implemented
- Methods return appropriate types

**Artifacts**:
- MODIFY: `src/todo/storage.py`

**Methods to Implement**:

| Method | Signature | Returns |
|--------|-----------|---------|
| add | `add(task: Task) -> Task` | Added task with ID |
| get_all | `get_all() -> list[Task]` | List of all tasks |
| get_by_id | `get_by_id(id: int) -> Task \| None` | Task or None |
| update | `update(task: Task) -> bool` | Success boolean |
| delete | `delete(id: int) -> bool` | Success boolean |

**References**:
- Plan Section 3.2: Storage Operations table
- Plan Section 6.3: storage.py specification

**Acceptance Criteria**:
- [ ] `add()` appends task and returns it with generated ID
- [ ] `get_all()` returns copy of all tasks
- [ ] `get_by_id()` returns task or None if not found
- [ ] `update()` modifies existing task, returns True/False
- [ ] `delete()` removes task by ID, returns True/False

---

### Task T2.4: Implement TaskStorage - Utility Methods

**Task ID**: T2.4
**Description**: Implement utility methods for TaskStorage.

**Preconditions**:
- T2.3 completed
- CRUD operations exist

**Expected Output**:
- Helper methods for checking storage state

**Artifacts**:
- MODIFY: `src/todo/storage.py`

**Methods to Implement**:

| Method | Signature | Returns |
|--------|-----------|---------|
| count | `count() -> int` | Number of tasks |
| is_empty | `is_empty() -> bool` | True if no tasks |

**References**:
- Plan Section 3.2: Storage Operations
- Plan Section 6.3: storage.py specification

**Acceptance Criteria**:
- [ ] `count()` returns number of tasks
- [ ] `is_empty()` returns True when no tasks exist
- [ ] `is_empty()` returns False when tasks exist

---

## Group 3: Service Layer Foundation

### Task T3.1: Implement ValidationError Exception

**Task ID**: T3.1
**Description**: Create custom exception class for validation errors.

**Preconditions**:
- T1.3 completed
- Package structure exists

**Expected Output**:
- Custom exception class with message attribute

**Artifacts**:
- CREATE: `src/todo/services.py`

**Implementation Details**:
```python
class ValidationError(Exception):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
```

**References**:
- Plan Section 7.3: ValidationError Design
- Plan Section 6.3: services.py specification

**Acceptance Criteria**:
- [ ] ValidationError class created
- [ ] Inherits from Exception
- [ ] Has `message` attribute
- [ ] Can be raised and caught

---

### Task T3.2: Implement Validation Functions

**Task ID**: T3.2
**Description**: Implement validation functions for title and description fields.

**Preconditions**:
- T3.1 completed
- ValidationError exists

**Expected Output**:
- Validation functions that raise ValidationError on invalid input
- Functions return cleaned (trimmed) input on success

**Artifacts**:
- MODIFY: `src/todo/services.py`

**Functions to Implement**:

```python
def validate_title(title: str) -> str:
    """Validate and clean title. Raises ValidationError if invalid."""

def validate_description(description: str) -> str:
    """Validate and clean description. Raises ValidationError if invalid."""
```

**Validation Rules (from Spec)**:

| Field | Rules |
|-------|-------|
| Title | Non-empty after trim, 1-100 chars |
| Description | 0-500 chars after trim |

**Error Messages (from Spec)**:
- Empty title: "Title cannot be empty"
- Title > 100 chars: "Title must be 100 characters or less"
- Description > 500 chars: "Description must be 500 characters or less"

**References**:
- Spec Section 2.2: Field Validation Rules
- Spec Section 3.1: Add Task Error Cases
- Plan Section 7.4: Error Messages

**Acceptance Criteria**:
- [ ] `validate_title()` trims whitespace
- [ ] `validate_title()` raises ValidationError for empty string
- [ ] `validate_title()` raises ValidationError for >100 chars
- [ ] `validate_description()` trims whitespace
- [ ] `validate_description()` raises ValidationError for >500 chars
- [ ] `validate_description()` allows empty string

---

### Task T3.3: Implement TaskService Class

**Task ID**: T3.3
**Description**: Create TaskService class with constructor accepting TaskStorage dependency.

**Preconditions**:
- T2.4 completed (storage complete)
- T3.2 completed (validation complete)

**Expected Output**:
- TaskService class initialized with storage
- Foundation for feature methods

**Artifacts**:
- MODIFY: `src/todo/services.py`

**Implementation Details**:
```python
class TaskService:
    def __init__(self, storage: TaskStorage):
        self._storage = storage

    def has_tasks(self) -> bool:
        """Check if any tasks exist"""
        return not self._storage.is_empty()

    def get_task_count(self) -> int:
        """Get total number of tasks"""
        return self._storage.count()
```

**References**:
- Plan Section 6.3: services.py specification
- Plan Section 2.2: Module Dependency Graph

**Acceptance Criteria**:
- [ ] TaskService class created
- [ ] Constructor accepts TaskStorage instance
- [ ] `has_tasks()` method works correctly
- [ ] `get_task_count()` method works correctly

---

## Group 4: CLI Foundation

### Task T4.1: Implement CLI Class Structure

**Task ID**: T4.1
**Description**: Create CLI class with constructor and constants for menu display.

**Preconditions**:
- T3.3 completed
- TaskService exists

**Expected Output**:
- CLI class with service dependency
- Menu text constants

**Artifacts**:
- CREATE: `src/todo/cli.py`

**Implementation Details**:
```python
class CLI:
    MENU_OPTIONS = {
        1: "Add Task",
        2: "View Tasks",
        3: "Update Task",
        4: "Delete Task",
        5: "Toggle Task Status",
        6: "Exit"
    }

    def __init__(self, service: TaskService):
        self._service = service
        self._running = False
```

**References**:
- Spec Section 4.1: Main Menu
- Plan Section 6.3: cli.py specification

**Acceptance Criteria**:
- [ ] CLI class created
- [ ] Constructor accepts TaskService
- [ ] Menu options defined
- [ ] `_running` flag initialized

---

### Task T4.2: Implement CLI Display Helpers

**Task ID**: T4.2
**Description**: Implement helper methods for displaying formatted output.

**Preconditions**:
- T4.1 completed
- CLI class exists

**Expected Output**:
- Methods for displaying banners, menus, tasks, messages

**Artifacts**:
- MODIFY: `src/todo/cli.py`

**Methods to Implement**:

| Method | Purpose |
|--------|---------|
| `display_welcome()` | Show welcome banner |
| `display_goodbye()` | Show goodbye message |
| `display_menu()` | Show main menu options |
| `display_task(task)` | Show single task details |
| `display_task_list(tasks)` | Show formatted task table |
| `display_error(msg)` | Show error message |
| `display_success(msg)` | Show success message |

**Display Formats (from Spec)**:
- Welcome banner (Spec Section 5.1)
- Main menu (Spec Section 4.1)
- Task list table (Spec Section 3.2)
- Goodbye message (Spec Section 5.2)

**References**:
- Spec Section 3.2: View Task List Display Format
- Spec Section 4.1: Main Menu
- Spec Section 5.1: Startup (Welcome Banner)
- Spec Section 5.2: Shutdown (Goodbye Message)
- Plan Section 6.3: cli.py Display helpers

**Acceptance Criteria**:
- [ ] Welcome banner displays correctly
- [ ] Main menu displays all 6 options
- [ ] Task list shows ID, status, title, created date
- [ ] Status indicators: `[ ]` for pending, `[X]` for completed
- [ ] Task count summary displayed
- [ ] Error messages clearly formatted
- [ ] Success messages clearly formatted

---

### Task T4.3: Implement CLI Input Helpers

**Task ID**: T4.3
**Description**: Implement helper methods for collecting and validating user input.

**Preconditions**:
- T4.2 completed
- Display helpers exist

**Expected Output**:
- Methods for getting menu choice, task ID, confirmation, text input

**Artifacts**:
- MODIFY: `src/todo/cli.py`

**Methods to Implement**:

| Method | Signature | Purpose |
|--------|-----------|---------|
| `get_menu_choice` | `() -> int` | Get valid menu selection (1-6) |
| `get_task_id` | `(prompt: str) -> int` | Get valid positive integer |
| `get_confirmation` | `(prompt: str) -> bool` | Get y/n response |
| `get_input` | `(prompt: str, allow_empty: bool = False) -> str` | Get text input |

**Input Rules (from Spec Section 4.4)**:
- Menu choice: Must be 1-6
- Task ID: Must be positive integer
- Confirmation: Case-insensitive y/n
- Text: Trim whitespace

**References**:
- Spec Section 4.4: Input Handling
- Plan Section 5.3: Input Collection Pattern
- Plan Section 5.4: User Input Handling

**Acceptance Criteria**:
- [ ] `get_menu_choice()` only accepts 1-6
- [ ] `get_menu_choice()` retries on invalid input
- [ ] `get_task_id()` validates positive integer
- [ ] `get_task_id()` shows error for non-numeric input
- [ ] `get_confirmation()` accepts y/Y/n/N
- [ ] `get_confirmation()` defaults to False on invalid
- [ ] `get_input()` trims whitespace
- [ ] `get_input()` respects allow_empty parameter

---

### Task T4.4: Implement Main Menu Loop

**Task ID**: T4.4
**Description**: Implement the main application loop that displays menu and routes to handlers.

**Preconditions**:
- T4.3 completed
- Input helpers exist

**Expected Output**:
- `run()` method that loops until exit
- Menu choice routing to handler methods (stubs for now)

**Artifacts**:
- MODIFY: `src/todo/cli.py`

**Implementation Details**:
```python
def run(self) -> None:
    """Main application loop"""
    self._running = True
    self.display_welcome()

    while self._running:
        self.display_menu()
        choice = self.get_menu_choice()

        if choice == 1:
            self.handle_add()
        elif choice == 2:
            self.handle_view()
        elif choice == 3:
            self.handle_update()
        elif choice == 4:
            self.handle_delete()
        elif choice == 5:
            self.handle_toggle()
        elif choice == 6:
            self.handle_exit()
```

**References**:
- Spec Section 4.2: Menu Navigation Rules
- Plan Section 5.1: Main Menu Loop flowchart
- Plan Section 5.2: Menu Handler Pattern

**Acceptance Criteria**:
- [ ] `run()` displays welcome on start
- [ ] Loop continues until exit
- [ ] Menu displays after each operation
- [ ] Correct routing for choices 1-6
- [ ] Exit sets `_running = False`

---

## Group 5: Add Task Feature

### Task T5.1: Implement TaskService.add_task()

**Task ID**: T5.1
**Description**: Implement the add_task method in TaskService.

**Preconditions**:
- T3.3 completed
- TaskService class exists

**Expected Output**:
- Method that validates input and creates task

**Artifacts**:
- MODIFY: `src/todo/services.py`

**Method Signature**:
```python
def add_task(self, title: str, description: str = "") -> Task:
    """Add a new task. Returns created task. Raises ValidationError if invalid."""
```

**Implementation Logic**:
1. Validate title (raise ValidationError if invalid)
2. Validate description (raise ValidationError if invalid)
3. Create Task object with auto-generated ID and timestamp
4. Add to storage
5. Return created task

**References**:
- Spec Section 3.1: Feature: Add Task
- Spec Section 3.1: Acceptance Criteria AC-1.1 through AC-1.7
- Plan Section 5.5: Add Task Flow
- Plan Section 6.3: TaskService methods

**Acceptance Criteria**:
- [ ] Validates title (1-100 chars, non-empty)
- [ ] Validates description (0-500 chars)
- [ ] Auto-generates unique ID
- [ ] Auto-generates created_at timestamp
- [ ] Sets is_completed to False
- [ ] Returns created Task
- [ ] Raises ValidationError for invalid input

---

### Task T5.2: Implement CLI.handle_add()

**Task ID**: T5.2
**Description**: Implement the Add Task menu handler in CLI.

**Preconditions**:
- T5.1 completed
- TaskService.add_task() exists
- T4.3 completed (input helpers)

**Expected Output**:
- Complete Add Task interaction flow

**Artifacts**:
- MODIFY: `src/todo/cli.py`

**Interaction Flow (from Spec)**:
1. Display header
2. Prompt for title
3. Validate title
4. Prompt for description (optional)
5. Validate description
6. Create task via service
7. Display confirmation with task ID

**References**:
- Spec Section 3.1: Add Task Interaction Flow
- Spec Section 3.1: Add Task Error Cases
- Plan Section 5.5: Add Task Flow

**Acceptance Criteria**:
- [ ] Prompts for title
- [ ] Shows error for empty title
- [ ] Shows error for title > 100 chars
- [ ] Prompts for description
- [ ] Allows empty description
- [ ] Shows error for description > 500 chars
- [ ] Displays success with task ID
- [ ] Returns to main menu

---

## Group 6: View Tasks Feature

### Task T6.1: Implement TaskService.get_all_tasks()

**Task ID**: T6.1
**Description**: Implement method to retrieve all tasks.

**Preconditions**:
- T3.3 completed
- TaskService class exists

**Expected Output**:
- Method that returns list of all tasks

**Artifacts**:
- MODIFY: `src/todo/services.py`

**Method Signature**:
```python
def get_all_tasks(self) -> list[Task]:
    """Get all tasks ordered by ID"""
```

**Implementation Logic**:
1. Get all tasks from storage
2. Return sorted by ID (creation order)

**References**:
- Spec Section 3.2: Feature: View Task List
- Spec Section 3.2: AC-2.1, AC-2.6
- Plan Section 6.3: TaskService methods

**Acceptance Criteria**:
- [ ] Returns all tasks in storage
- [ ] Tasks ordered by ID (ascending)
- [ ] Returns empty list if no tasks

---

### Task T6.2: Implement CLI.handle_view()

**Task ID**: T6.2
**Description**: Implement the View Tasks menu handler in CLI.

**Preconditions**:
- T6.1 completed
- TaskService.get_all_tasks() exists
- T4.2 completed (display_task_list)

**Expected Output**:
- Complete View Tasks interaction flow

**Artifacts**:
- MODIFY: `src/todo/cli.py`

**Display Format (from Spec Section 3.2)**:
```
================================================================================
                              YOUR TASKS
================================================================================
ID    | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | [ ]         | Buy groceries                  | 2025-12-29 10:30:00
--------------------------------------------------------------------------------
Total: 1 tasks (0 completed, 1 pending)
================================================================================
```

**References**:
- Spec Section 3.2: View Task List Interaction Flow
- Spec Section 3.2: Display Format
- Spec Section 3.2: AC-2.1 through AC-2.6
- Plan Section 5.5: View Tasks Flow

**Acceptance Criteria**:
- [ ] Shows "No tasks found" message when empty
- [ ] Displays all tasks in formatted table
- [ ] Shows correct status indicators
- [ ] Shows total count with breakdown
- [ ] Returns to main menu

---

## Group 7: Update Task Feature

### Task T7.1: Implement TaskService.update_task()

**Task ID**: T7.1
**Description**: Implement method to update task title and description.

**Preconditions**:
- T3.3 completed
- TaskService class exists

**Expected Output**:
- Method that updates task and returns updated Task

**Artifacts**:
- MODIFY: `src/todo/services.py`

**Method Signature**:
```python
def get_task(self, task_id: int) -> Task | None:
    """Get task by ID. Returns None if not found."""

def update_task(self, task_id: int, title: str | None, description: str | None) -> Task:
    """Update task. Returns updated task. Raises ValidationError if invalid."""
```

**Implementation Logic**:
1. Get task by ID (return None if not found)
2. If title provided, validate and update
3. If description provided, validate and update
4. Save to storage
5. Return updated task

**References**:
- Spec Section 3.3: Feature: Update Task
- Spec Section 3.3: AC-3.1 through AC-3.7
- Plan Section 5.5: Update Task Flow
- Plan Section 6.3: TaskService methods

**Acceptance Criteria**:
- [ ] `get_task()` returns task or None
- [ ] Only updates fields when new value provided
- [ ] Preserves field when None passed
- [ ] Validates new title if provided
- [ ] Validates new description if provided
- [ ] Does NOT modify id, is_completed, created_at
- [ ] Returns updated Task
- [ ] Raises ValidationError for invalid input

---

### Task T7.2: Implement CLI.handle_update()

**Task ID**: T7.2
**Description**: Implement the Update Task menu handler in CLI.

**Preconditions**:
- T7.1 completed
- TaskService.update_task() exists
- T4.3 completed (input helpers)

**Expected Output**:
- Complete Update Task interaction flow

**Artifacts**:
- MODIFY: `src/todo/cli.py`

**Interaction Flow (from Spec)**:
1. Check if tasks exist
2. Prompt for task ID
3. Validate ID and get task
4. Display current task details
5. Prompt for new title (Enter to keep)
6. Prompt for new description (Enter to keep)
7. Update via service
8. Display confirmation

**References**:
- Spec Section 3.3: Update Task Interaction Flow
- Spec Section 3.3: Update Task Error Cases
- Plan Section 5.5: Update Task Flow

**Acceptance Criteria**:
- [ ] Shows "No tasks available" if empty
- [ ] Prompts for task ID
- [ ] Shows error for invalid ID format
- [ ] Shows error for ID not found
- [ ] Displays current task details
- [ ] Enter keeps current value
- [ ] Validates new values
- [ ] Shows success message
- [ ] Returns to main menu

---

## Group 8: Delete Task Feature

### Task T8.1: Implement TaskService.delete_task()

**Task ID**: T8.1
**Description**: Implement method to delete a task by ID.

**Preconditions**:
- T3.3 completed
- TaskService class exists

**Expected Output**:
- Method that deletes task and returns success boolean

**Artifacts**:
- MODIFY: `src/todo/services.py`

**Method Signature**:
```python
def delete_task(self, task_id: int) -> bool:
    """Delete task by ID. Returns True if deleted, False if not found."""
```

**Implementation Logic**:
1. Delete from storage by ID
2. Return True if deleted, False if not found

**References**:
- Spec Section 3.4: Feature: Delete Task
- Spec Section 3.4: AC-4.4, AC-4.7
- Plan Section 5.5: Delete Task Flow
- Plan Section 6.3: TaskService methods

**Acceptance Criteria**:
- [ ] Deletes task from storage
- [ ] Returns True on success
- [ ] Returns False if task not found
- [ ] Deleted ID is not reused

---

### Task T8.2: Implement CLI.handle_delete()

**Task ID**: T8.2
**Description**: Implement the Delete Task menu handler in CLI.

**Preconditions**:
- T8.1 completed
- TaskService.delete_task() exists
- T4.3 completed (input helpers)

**Expected Output**:
- Complete Delete Task interaction flow with confirmation

**Artifacts**:
- MODIFY: `src/todo/cli.py`

**Interaction Flow (from Spec)**:
1. Check if tasks exist
2. Prompt for task ID
3. Validate ID and get task
4. Display task details
5. Ask for confirmation (y/n)
6. If confirmed: delete and show success
7. If not confirmed: show cancelled message

**References**:
- Spec Section 3.4: Delete Task Interaction Flow
- Spec Section 3.4: Delete Task Error Cases
- Plan Section 5.5: Delete Task Flow

**Acceptance Criteria**:
- [ ] Shows "No tasks available" if empty
- [ ] Prompts for task ID
- [ ] Shows error for invalid ID format
- [ ] Shows error for ID not found
- [ ] Displays task before deletion
- [ ] Requires confirmation
- [ ] Deletes on 'y' confirmation
- [ ] Cancels on 'n' or other input
- [ ] Shows appropriate message
- [ ] Returns to main menu

---

## Group 9: Toggle Status Feature

### Task T9.1: Implement TaskService.toggle_task()

**Task ID**: T9.1
**Description**: Implement method to toggle task completion status.

**Preconditions**:
- T3.3 completed
- TaskService class exists

**Expected Output**:
- Method that toggles is_completed and returns updated Task

**Artifacts**:
- MODIFY: `src/todo/services.py`

**Method Signature**:
```python
def toggle_task(self, task_id: int) -> Task | None:
    """Toggle task completion status. Returns updated task or None if not found."""
```

**Implementation Logic**:
1. Get task by ID
2. If not found, return None
3. Toggle is_completed (True → False, False → True)
4. Update in storage
5. Return updated task

**References**:
- Spec Section 3.5: Feature: Mark Task Complete/Incomplete
- Spec Section 3.5: AC-5.1 through AC-5.5
- Plan Section 5.5: Toggle Status Flow
- Plan Section 6.3: TaskService methods

**Acceptance Criteria**:
- [ ] Returns None if task not found
- [ ] Toggles False → True
- [ ] Toggles True → False
- [ ] Persists change to storage
- [ ] Returns updated Task

---

### Task T9.2: Implement CLI.handle_toggle()

**Task ID**: T9.2
**Description**: Implement the Toggle Status menu handler in CLI.

**Preconditions**:
- T9.1 completed
- TaskService.toggle_task() exists
- T4.3 completed (input helpers)

**Expected Output**:
- Complete Toggle Status interaction flow

**Artifacts**:
- MODIFY: `src/todo/cli.py`

**Interaction Flow (from Spec)**:
1. Check if tasks exist
2. Prompt for task ID
3. Validate ID
4. Toggle via service
5. Display confirmation with new status

**Status Messages**:
- "Task #{id} marked as complete"
- "Task #{id} marked as incomplete"

**References**:
- Spec Section 3.5: Toggle Status Interaction Flow
- Spec Section 3.5: Toggle Status Error Cases
- Plan Section 5.5: Toggle Status Flow

**Acceptance Criteria**:
- [ ] Shows "No tasks available" if empty
- [ ] Prompts for task ID
- [ ] Shows error for invalid ID format
- [ ] Shows error for ID not found
- [ ] Displays correct new status message
- [ ] Returns to main menu

---

## Group 10: Application Entry & Exit

### Task T10.1: Implement CLI.handle_exit()

**Task ID**: T10.1
**Description**: Implement the Exit menu handler with confirmation.

**Preconditions**:
- T4.3 completed (get_confirmation)
- T4.2 completed (display_goodbye)

**Expected Output**:
- Exit handler with data loss warning and confirmation

**Artifacts**:
- MODIFY: `src/todo/cli.py`

**Exit Confirmation Message (from Spec)**:
```
WARNING: All tasks will be lost when you exit.
Are you sure you want to exit? (y/n):
```

**Interaction Flow**:
1. Display warning about data loss
2. Ask for confirmation
3. If confirmed: display goodbye, set `_running = False`
4. If not confirmed: return to menu

**References**:
- Spec Section 4.3: Exit Flow
- Spec Section 5.2: Shutdown
- Plan Section 5.5: Exit Flow

**Acceptance Criteria**:
- [ ] Displays data loss warning
- [ ] Asks for confirmation
- [ ] On 'y': displays goodbye message
- [ ] On 'y': sets `_running = False`
- [ ] On 'n': returns to menu
- [ ] Application terminates after goodbye

---

### Task T10.2: Implement main.py Entry Point

**Task ID**: T10.2
**Description**: Create main.py with application initialization and entry point.

**Preconditions**:
- T4.4 completed (CLI.run exists)
- All service and storage classes exist

**Expected Output**:
- main.py that initializes all components and starts CLI

**Artifacts**:
- CREATE: `src/todo/main.py`

**Implementation Details**:
```python
from todo.storage import TaskStorage
from todo.services import TaskService
from todo.cli import CLI

def main() -> None:
    """Application entry point"""
    storage = TaskStorage()
    service = TaskService(storage)
    cli = CLI(service)
    cli.run()

if __name__ == "__main__":
    main()
```

**References**:
- Plan Section 2.3: Application Entry Flow
- Plan Section 6.3: main.py specification
- Spec Section 5.1: Startup

**Acceptance Criteria**:
- [ ] Initializes TaskStorage
- [ ] Initializes TaskService with storage
- [ ] Initializes CLI with service
- [ ] Calls cli.run()
- [ ] Can be run with `python -m todo.main`

---

### Task T10.3: Configure Package Entry Point

**Task ID**: T10.3
**Description**: Update pyproject.toml and __init__.py for proper package execution.

**Preconditions**:
- T10.2 completed
- main.py exists

**Expected Output**:
- Package can be run with `python -m todo`

**Artifacts**:
- MODIFY: `pyproject.toml` (add scripts entry)
- MODIFY: `src/todo/__init__.py` (export main)

**pyproject.toml addition**:
```toml
[project.scripts]
todo = "todo.main:main"
```

**References**:
- Spec Section 7: Technology Requirements
- Spec Section 6: Project Structure

**Acceptance Criteria**:
- [ ] Can run with `uv run todo`
- [ ] Can run with `python -m todo`
- [ ] Application starts correctly

---

## Group 11: Documentation

### Task T11.1: Create README.md

**Task ID**: T11.1
**Description**: Create README with setup and usage instructions.

**Preconditions**:
- All implementation tasks completed
- Application is functional

**Expected Output**:
- Complete README.md with all required sections

**Artifacts**:
- CREATE: `README.md`

**Required Sections**:
1. Project title and description
2. Features list
3. Prerequisites (Python 3.13+, UV)
4. Installation instructions
5. Usage instructions
6. Menu options description
7. Project structure

**References**:
- Spec Section 8.1: Documentation deliverables
- Spec Section 6: Project Structure

**Acceptance Criteria**:
- [ ] Clear project description
- [ ] All 5 features documented
- [ ] Setup instructions complete
- [ ] Usage examples provided
- [ ] Prerequisites listed

---

### Task T11.2: Create CLAUDE.md

**Task ID**: T11.2
**Description**: Create Claude Code instructions file.

**Preconditions**:
- T11.1 completed

**Expected Output**:
- CLAUDE.md with development instructions

**Artifacts**:
- CREATE: `CLAUDE.md`

**Required Content**:
1. Project overview
2. Constitution reference
3. Spec-driven development reminder
4. Code organization
5. Phase I constraints
6. Commands for running/testing

**References**:
- Spec Section 8.1: Documentation deliverables
- Constitution Article I & II

**Acceptance Criteria**:
- [ ] References Constitution
- [ ] Explains spec-driven workflow
- [ ] Lists Phase I constraints
- [ ] Provides development commands

---

## Task Dependency Graph

```
T1.1 ──► T1.2 ──► T1.3 ──┬──► T2.1 ──► T2.2 ──► T2.3 ──► T2.4 ──┐
                         │                                        │
                         │                                        ▼
                         └──► T3.1 ──► T3.2 ──────────────────► T3.3
                                                                  │
                                                                  ▼
                              T4.1 ──► T4.2 ──► T4.3 ──► T4.4 ◄───┘
                                                  │
                    ┌─────────────────────────────┼─────────────────────────────┐
                    │              │              │              │              │
                    ▼              ▼              ▼              ▼              ▼
                  T5.1           T6.1           T7.1           T8.1           T9.1
                    │              │              │              │              │
                    ▼              ▼              ▼              ▼              ▼
                  T5.2           T6.2           T7.2           T8.2           T9.2
                    │              │              │              │              │
                    └──────────────┴──────────────┴──────────────┴──────────────┘
                                                  │
                                                  ▼
                              T10.1 ◄─────────────┘
                                │
                                ▼
                              T10.2 ──► T10.3
                                          │
                                          ▼
                              T11.1 ──► T11.2
```

---

## Execution Order (Sequential)

| Order | Task ID | Description |
|-------|---------|-------------|
| 1 | T1.1 | Initialize UV project |
| 2 | T1.2 | Create directory structure |
| 3 | T1.3 | Create package init files |
| 4 | T2.1 | Implement Task dataclass |
| 5 | T2.2 | Implement TaskStorage core |
| 6 | T2.3 | Implement TaskStorage CRUD |
| 7 | T2.4 | Implement TaskStorage utilities |
| 8 | T3.1 | Implement ValidationError |
| 9 | T3.2 | Implement validation functions |
| 10 | T3.3 | Implement TaskService class |
| 11 | T4.1 | Implement CLI class structure |
| 12 | T4.2 | Implement CLI display helpers |
| 13 | T4.3 | Implement CLI input helpers |
| 14 | T4.4 | Implement main menu loop |
| 15 | T5.1 | Implement TaskService.add_task |
| 16 | T5.2 | Implement CLI.handle_add |
| 17 | T6.1 | Implement TaskService.get_all_tasks |
| 18 | T6.2 | Implement CLI.handle_view |
| 19 | T7.1 | Implement TaskService.update_task |
| 20 | T7.2 | Implement CLI.handle_update |
| 21 | T8.1 | Implement TaskService.delete_task |
| 22 | T8.2 | Implement CLI.handle_delete |
| 23 | T9.1 | Implement TaskService.toggle_task |
| 24 | T9.2 | Implement CLI.handle_toggle |
| 25 | T10.1 | Implement CLI.handle_exit |
| 26 | T10.2 | Implement main.py |
| 27 | T10.3 | Configure package entry point |
| 28 | T11.1 | Create README.md |
| 29 | T11.2 | Create CLAUDE.md |

---

## Compliance Verification

### Specification Coverage

| Spec Requirement | Covered By Tasks |
|------------------|------------------|
| Add Task | T5.1, T5.2 |
| View Tasks | T6.1, T6.2 |
| Update Task | T7.1, T7.2 |
| Delete Task | T8.1, T8.2 |
| Toggle Status | T9.1, T9.2 |
| Task Model | T2.1 |
| In-Memory Storage | T2.2, T2.3, T2.4 |
| Menu-Based CLI | T4.1-T4.4 |
| Input Validation | T3.1, T3.2, T4.3 |
| Error Handling | T3.1, T3.2, all handlers |
| Startup/Exit | T10.1, T10.2 |
| Documentation | T11.1, T11.2 |

### New Features Check
- [ ] **VERIFIED**: No new features introduced beyond specification

### Future Phase Check
- [ ] **VERIFIED**: No Phase II-V concepts included

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-29 | Claude Code | Initial task breakdown |

---

## Approval

**Task Breakdown Status**: DRAFT - PENDING APPROVAL

**Approval Required Before**:
- Implementation begins

**Dependencies**:
- CONSTITUTION.md v1.0 (approved)
- PHASE-I-SPEC.md v1.0 (approved)
- PHASE-I-PLAN.md v1.0 (approved)

---

*These tasks fully implement Phase I requirements. No implementation shall begin until this task breakdown is approved.*
