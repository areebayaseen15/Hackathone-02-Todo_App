# Phase I Technical Plan: Implementation Strategy

> **Technical Plan Document**
> Version: 1.0
> Phase: I
> Status: DRAFT - PENDING APPROVAL
> Specification Reference: specs/PHASE-I-SPEC.md v1.0
> Constitution Reference: CONSTITUTION.md v1.0

---

## 1. Plan Overview

### 1.1 Purpose
This document describes HOW the Phase I specification requirements will be implemented. It provides technical decisions, architectural patterns, and implementation strategies while strictly adhering to the approved specification.

### 1.2 Scope
- Implementation approach for 5 features
- In-memory data structure design
- Module architecture and responsibilities
- Control flow and error handling strategies

### 1.3 Compliance Statement
This plan:
- Implements ONLY features defined in PHASE-I-SPEC.md
- Introduces NO new features or capabilities
- Adheres to Constitution Article III (Phase Isolation)
- Uses ONLY approved technology stack

---

## 2. High-Level Application Structure

### 2.1 Architecture Pattern
**Pattern**: Layered Architecture (3-tier for console application)

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│                        (cli.py)                              │
│   - Menu display and navigation                              │
│   - User input collection                                    │
│   - Output formatting                                        │
│   - Input validation (format only)                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                      │
│                      (services.py)                           │
│   - Task operations (add, update, delete, toggle)           │
│   - Business validation (rules, constraints)                │
│   - Operation orchestration                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│              (models.py + storage.py)                        │
│   - Task data structure                                      │
│   - In-memory storage                                        │
│   - CRUD operations on storage                               │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Module Dependency Graph

```
main.py
    │
    ├──► cli.py (imports)
    │       │
    │       └──► services.py (imports)
    │               │
    │               ├──► storage.py (imports)
    │               │
    │               └──► models.py (imports)
    │
    └──► storage.py (initializes)
```

### 2.3 Application Entry Flow

```
main.py
    │
    ├── 1. Initialize storage (empty TaskStorage instance)
    ├── 2. Create service layer (TaskService with storage)
    ├── 3. Create CLI handler (CLI with service)
    ├── 4. Display welcome banner
    ├── 5. Start main menu loop
    └── 6. Handle exit (cleanup and goodbye)
```

---

## 3. In-Memory Data Structures

### 3.1 Task Model Implementation

**File**: `src/todo/models.py`

**Approach**: Python `dataclass` for clean, type-safe data structure

```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
```

**Design Decisions**:
- Use `dataclass` for automatic `__init__`, `__repr__`, `__eq__`
- All fields are instance attributes (no class-level state)
- `created_at` uses `datetime` from standard library
- No methods on Task class (pure data container)

### 3.2 Storage Implementation

**File**: `src/todo/storage.py`

**Approach**: Class-based storage manager with Python `list`

```python
class TaskStorage:
    _tasks: list[Task]      # Task storage
    _next_id: int           # ID counter
```

**Data Structure Choice**: `list[Task]`

| Alternative | Reason Not Chosen |
|-------------|-------------------|
| `dict[int, Task]` | List is simpler; iteration order preserved; ID lookup is O(n) but acceptable for in-memory scale |
| `collections.OrderedDict` | Overkill for Phase I requirements |
| Plain `list[dict]` | Loses type safety; dataclass is cleaner |

**Storage Operations**:

| Operation | Method | Complexity |
|-----------|--------|------------|
| Add | `add(task: Task) -> Task` | O(1) append |
| Get All | `get_all() -> list[Task]` | O(1) return copy |
| Get By ID | `get_by_id(id: int) -> Task \| None` | O(n) linear search |
| Update | `update(task: Task) -> bool` | O(n) find + update |
| Delete | `delete(id: int) -> bool` | O(n) find + remove |
| Count | `count() -> int` | O(1) len |

---

## 4. Task Identification Strategy

### 4.1 ID Generation Approach

**Strategy**: Sequential Integer Counter

```
Initial State: _next_id = 1

Add Task 1 → ID = 1, _next_id = 2
Add Task 2 → ID = 2, _next_id = 3
Delete Task 1 → _next_id unchanged (still 3)
Add Task 3 → ID = 3, _next_id = 4
```

**Implementation**:
```python
class TaskStorage:
    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def _generate_id(self) -> int:
        current_id = self._next_id
        self._next_id += 1
        return current_id
```

### 4.2 ID Guarantees

| Property | Guarantee |
|----------|-----------|
| Uniqueness | Yes - IDs are never reused within a session |
| Sequential | Yes - IDs increment by 1 |
| Positive | Yes - Starting from 1 |
| Immutable | Yes - Task ID never changes after creation |
| Gaps Allowed | Yes - Deleted IDs leave gaps |

### 4.3 ID Validation

Validation occurs at two levels:

1. **CLI Layer** (format validation):
   - Input is numeric
   - Input is positive integer

2. **Service Layer** (existence validation):
   - Task with ID exists in storage

---

## 5. CLI Control Flow

### 5.1 Main Menu Loop

**Pattern**: Infinite loop with explicit exit condition

```
┌─────────────────────────────────────────┐
│           DISPLAY MAIN MENU             │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         GET USER INPUT (1-6)            │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         VALIDATE INPUT FORMAT           │
│      (is it a number 1-6?)              │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │ Invalid               │ Valid
        ▼                       ▼
┌───────────────┐    ┌─────────────────────┐
│ DISPLAY ERROR │    │   ROUTE TO HANDLER  │
│ (try again)   │    │                     │
└───────────────┘    │  1 → handle_add()   │
        │            │  2 → handle_view()  │
        │            │  3 → handle_update()│
        │            │  4 → handle_delete()│
        │            │  5 → handle_toggle()│
        │            │  6 → handle_exit()  │
        │            └─────────────────────┘
        │                       │
        │                       ▼
        │            ┌─────────────────────┐
        │            │  EXECUTE OPERATION  │
        │            └─────────────────────┘
        │                       │
        │                       ▼
        │            ┌─────────────────────┐
        │            │  DISPLAY RESULT     │
        │            └─────────────────────┘
        │                       │
        └───────────────────────┘
                    │
                    ▼
              [LOOP BACK TO MENU]
              (unless exit confirmed)
```

### 5.2 Menu Handler Pattern

Each menu option follows a consistent pattern:

```
HANDLER PATTERN:
1. Display operation header
2. Check preconditions (e.g., tasks exist)
3. Collect required input with validation loop
4. Call service layer method
5. Display result (success or error)
6. Return to menu
```

### 5.3 Input Collection Pattern

**Pattern**: Validation loop with retry

```
COLLECT INPUT:
    LOOP:
        Display prompt
        Read input
        Trim whitespace

        IF validation passes:
            RETURN input
        ELSE:
            Display error message
            CONTINUE loop
```

### 5.4 User Input Handling

| Input Type | Handling |
|------------|----------|
| Menu choice | Must be 1-6; retry on invalid |
| Task ID | Must be positive integer; retry on invalid |
| Title | Trim whitespace; reject if empty |
| Description | Trim whitespace; allow empty |
| Confirmation (y/n) | Case-insensitive; default to 'n' on invalid |

### 5.5 Control Flow for Each Feature

#### Add Task Flow
```
1. Prompt: "Enter task title"
2. Validate: Non-empty, ≤100 chars
3. Prompt: "Enter description (optional)"
4. Validate: ≤500 chars
5. Call: service.add_task(title, description)
6. Display: "Task #{id} created successfully"
```

#### View Tasks Flow
```
1. Call: service.get_all_tasks()
2. IF empty:
     Display: "No tasks found"
   ELSE:
     Display: Formatted task table
     Display: Summary counts
```

#### Update Task Flow
```
1. Check: Tasks exist (else show error, return)
2. Prompt: "Enter task ID"
3. Validate: Numeric, task exists
4. Display: Current task details
5. Prompt: "New title (Enter to keep)"
6. Prompt: "New description (Enter to keep)"
7. Call: service.update_task(id, title, description)
8. Display: "Task #{id} updated successfully"
```

#### Delete Task Flow
```
1. Check: Tasks exist (else show error, return)
2. Prompt: "Enter task ID"
3. Validate: Numeric, task exists
4. Display: Task to be deleted
5. Prompt: "Confirm delete? (y/n)"
6. IF confirmed:
     Call: service.delete_task(id)
     Display: "Task #{id} deleted"
   ELSE:
     Display: "Deletion cancelled"
```

#### Toggle Status Flow
```
1. Check: Tasks exist (else show error, return)
2. Prompt: "Enter task ID"
3. Validate: Numeric, task exists
4. Call: service.toggle_task(id)
5. Display: "Task #{id} marked as [complete/incomplete]"
```

#### Exit Flow
```
1. Display: Warning about data loss
2. Prompt: "Confirm exit? (y/n)"
3. IF confirmed:
     Display: Goodbye message
     EXIT application
   ELSE:
     RETURN to menu
```

---

## 6. Separation of Responsibilities

### 6.1 Module Responsibility Matrix

| Responsibility | models.py | storage.py | services.py | cli.py | main.py |
|----------------|:---------:|:----------:|:-----------:|:------:|:-------:|
| Task data structure | ✓ | | | | |
| ID generation | | ✓ | | | |
| Task storage (list) | | ✓ | | | |
| CRUD on storage | | ✓ | | | |
| Business validation | | | ✓ | | |
| Task operations | | | ✓ | | |
| Input format validation | | | | ✓ | |
| Menu display | | | | ✓ | |
| User interaction | | | | ✓ | |
| Output formatting | | | | ✓ | |
| Application init | | | | | ✓ |
| Dependency wiring | | | | | ✓ |

### 6.2 Layer Communication Rules

```
┌─────────┐     ┌──────────┐     ┌─────────┐     ┌────────┐
│ cli.py  │────►│services.py│────►│storage.py│────►│models.py│
└─────────┘     └──────────┘     └─────────┘     └────────┘
     │                │                │               │
     │                │                │               │
   Calls           Calls            Uses           Defines
  service         storage           Task            Task
  methods         methods          objects         dataclass
```

**Rules**:
1. CLI never directly accesses storage
2. CLI only communicates with services
3. Services handle all business logic
4. Storage handles all data management
5. Models are shared across all layers

### 6.3 Detailed Module Specifications

#### models.py
```
PURPOSE: Define Task data structure

CONTAINS:
- Task dataclass

DEPENDENCIES:
- datetime (standard library)

EXPORTS:
- Task
```

#### storage.py
```
PURPOSE: Manage in-memory task collection

CONTAINS:
- TaskStorage class
  - _tasks: list[Task]
  - _next_id: int
  - add(task) -> Task
  - get_all() -> list[Task]
  - get_by_id(id) -> Task | None
  - update(task) -> bool
  - delete(id) -> bool
  - count() -> int
  - is_empty() -> bool

DEPENDENCIES:
- models.Task

EXPORTS:
- TaskStorage
```

#### services.py
```
PURPOSE: Business logic and validation

CONTAINS:
- TaskService class
  - __init__(storage: TaskStorage)
  - add_task(title, description) -> Task
  - get_all_tasks() -> list[Task]
  - get_task(id) -> Task | None
  - update_task(id, title, description) -> Task
  - delete_task(id) -> bool
  - toggle_task(id) -> Task
  - get_task_count() -> int
  - has_tasks() -> bool

- ValidationError (exception class)

- Validation functions:
  - validate_title(title) -> str
  - validate_description(desc) -> str

DEPENDENCIES:
- models.Task
- storage.TaskStorage
- datetime

EXPORTS:
- TaskService
- ValidationError
```

#### cli.py
```
PURPOSE: User interface and interaction

CONTAINS:
- CLI class
  - __init__(service: TaskService)
  - run() -> None (main loop)
  - display_menu() -> None
  - handle_add() -> None
  - handle_view() -> None
  - handle_update() -> None
  - handle_delete() -> None
  - handle_toggle() -> None
  - handle_exit() -> bool

- Input helpers:
  - get_menu_choice() -> int
  - get_task_id() -> int
  - get_confirmation(prompt) -> bool
  - get_input(prompt, allow_empty) -> str

- Display helpers:
  - display_welcome() -> None
  - display_goodbye() -> None
  - display_task(task) -> None
  - display_task_list(tasks) -> None
  - display_error(message) -> None
  - display_success(message) -> None

DEPENDENCIES:
- services.TaskService
- services.ValidationError
- models.Task

EXPORTS:
- CLI
```

#### main.py
```
PURPOSE: Application entry point

CONTAINS:
- main() function
  - Initialize TaskStorage
  - Initialize TaskService with storage
  - Initialize CLI with service
  - Run CLI

- if __name__ == "__main__" block

DEPENDENCIES:
- storage.TaskStorage
- services.TaskService
- cli.CLI

EXPORTS:
- main (for testing)
```

---

## 7. Error Handling Strategy

### 7.1 Error Categories

| Category | Layer | Handling |
|----------|-------|----------|
| Input Format Errors | CLI | Retry loop with message |
| Validation Errors | Service | Raise ValidationError, CLI catches and displays |
| Not Found Errors | Service | Return None or raise, CLI displays message |
| System Errors | Any | Catch, display generic message, continue |

### 7.2 Error Handling by Layer

#### CLI Layer
```
TRY:
    Call service method
EXCEPT ValidationError as e:
    Display error message from exception
    Prompt to retry or return to menu
EXCEPT Exception:
    Display "An unexpected error occurred"
    Return to menu
```

#### Service Layer
```
Validate inputs
IF validation fails:
    RAISE ValidationError with specific message

Perform operation
IF operation fails (e.g., not found):
    RETURN None or False (depending on operation)

RETURN result
```

#### Storage Layer
```
No exceptions raised
Return None for not found
Return False for failed operations
Return True/object for success
```

### 7.3 ValidationError Design

```python
class ValidationError(Exception):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
```

### 7.4 Error Messages (from Specification)

| Error Condition | Message |
|-----------------|---------|
| Empty title | "Title cannot be empty" |
| Title too long | "Title must be 100 characters or less" |
| Description too long | "Description must be 500 characters or less" |
| Invalid ID format | "Invalid ID. Please enter a number" |
| Task not found | "Task with ID {id} not found" |
| No tasks (for operations) | "No tasks available to [update/delete]" |
| No tasks (for view) | "No tasks found. Add a task to get started!" |

### 7.5 Error Recovery Strategy

```
ON ERROR:
    1. Display user-friendly error message
    2. Do NOT show stack trace
    3. Do NOT crash application
    4. Either:
       a. Prompt to retry input, OR
       b. Return to main menu
    5. Preserve all existing data
```

---

## 8. Implementation Tasks

Based on this plan, the following tasks will be created:

### Task Group 1: Project Setup
- [ ] T1.1: Initialize UV project with pyproject.toml
- [ ] T1.2: Create project directory structure
- [ ] T1.3: Create package __init__.py files

### Task Group 2: Data Layer
- [ ] T2.1: Implement Task dataclass in models.py
- [ ] T2.2: Implement TaskStorage class in storage.py

### Task Group 3: Service Layer
- [ ] T3.1: Implement ValidationError exception
- [ ] T3.2: Implement validation functions
- [ ] T3.3: Implement TaskService class

### Task Group 4: Presentation Layer
- [ ] T4.1: Implement CLI display helpers
- [ ] T4.2: Implement CLI input helpers
- [ ] T4.3: Implement menu handler methods
- [ ] T4.4: Implement main menu loop

### Task Group 5: Integration
- [ ] T5.1: Implement main.py entry point
- [ ] T5.2: Integration testing of all features

### Task Group 6: Documentation
- [ ] T6.1: Create README.md with setup instructions
- [ ] T6.2: Create CLAUDE.md with Claude Code instructions

---

## 9. Constraints Verification

### 9.1 Specification Compliance Check

| Spec Requirement | Plan Coverage |
|------------------|---------------|
| Add Task | Section 5.5, Task T3.3, T4.3 |
| View Tasks | Section 5.5, Task T3.3, T4.3 |
| Update Task | Section 5.5, Task T3.3, T4.3 |
| Delete Task | Section 5.5, Task T3.3, T4.3 |
| Toggle Status | Section 5.5, Task T3.3, T4.3 |
| Task Model | Section 3.1, Task T2.1 |
| In-Memory Storage | Section 3.2, Task T2.2 |
| Menu-Based CLI | Section 5, Task T4.x |
| Error Handling | Section 7, all layers |

### 9.2 Prohibited Elements Verification

| Prohibited Element | Status |
|--------------------|--------|
| Database connections | NOT PRESENT ✓ |
| File operations | NOT PRESENT ✓ |
| Network requests | NOT PRESENT ✓ |
| Authentication | NOT PRESENT ✓ |
| External packages | NOT PRESENT ✓ |
| Web frameworks | NOT PRESENT ✓ |
| Future phase concepts | NOT PRESENT ✓ |

### 9.3 Constitution Compliance

| Article | Compliance |
|---------|------------|
| Article I (Spec-Driven) | Plan derived from approved spec ✓ |
| Article II (Agent Rules) | No feature invention ✓ |
| Article III (Phase Governance) | Phase I scope only ✓ |
| Article IV (Technology) | Python 3.13+, UV, stdlib only ✓ |
| Article V (Quality) | Layered architecture, separation of concerns ✓ |

---

## 10. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-29 | Claude Code | Initial plan |

---

## 11. Approval

**Plan Status**: DRAFT - PENDING APPROVAL

**Approval Required Before**:
- Task breakdown
- Implementation

**Dependencies**:
- CONSTITUTION.md v1.0 (approved)
- PHASE-I-SPEC.md v1.0 (must be approved)

---

*This plan describes HOW to implement Phase I requirements. No implementation shall begin until this plan is approved.*
