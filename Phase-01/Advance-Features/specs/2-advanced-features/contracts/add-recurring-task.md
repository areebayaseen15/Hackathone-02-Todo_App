# Contract: Add Recurring Task

**Feature**: Advanced Todo Features
**Contract ID**: ADV-001
**Date**: 2025-12-30

## Purpose

Define the contract for adding tasks with due date and recurrence support to the Todo App.

## Actors

- **User**: Interacts with the CLI to create tasks
- **CLI**: Collects and validates user input
- **Service**: Contains business logic for task creation
- **Storage**: Manages in-memory task storage

## Pre-Conditions

1. Application is running
2. User has selected "Add Task" from main menu

## Input Specification

### Input Fields

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| `title` | String | Yes | N/A | 1-100 characters, non-empty after trim |
| `description` | String | No | Empty string | 0-500 characters |
| `priority` | String | No | "medium" | Case-insensitive: high/medium/low |
| `category` | String | No | None | 0-50 characters |
| `due_date` | String | No | None | YYYY-MM-DD format or empty |
| `recurrence` | String | No | "none" | Case-insensitive: none/daily/weekly/monthly |

### Input Flow

```
================================================================================
                              ADD TASK
================================================================================
Enter task title: [User input - required]
Enter task description (optional, press Enter to skip): [User input - optional]
Enter priority (high/medium/low, default: medium): [User input - optional]
Enter category (optional, press Enter to skip): [User input - optional]
Enter due date (YYYY-MM-DD, optional, press Enter to skip): [User input - optional]
Enter recurrence (none/daily/weekly/monthly, default: none): [User input - optional]
```

## Processing

### Step 1: Validate Title
- Trim whitespace
- Check if empty after trim → Error: "Title cannot be empty"
- Check if > 100 characters → Error: "Title must be 100 characters or less"
- Return cleaned title

### Step 2: Validate Description
- Trim whitespace
- Check if > 500 characters → Error: "Description must be 500 characters or less"
- Return cleaned description

### Step 3: Validate Priority
- Trim and convert to lowercase
- Match against: "high", "medium", "low"
- Invalid → Error: "Invalid priority '{value}'. Must be one of: high, medium, low"
- Return Priority enum value

### Step 4: Validate Category
- Trim whitespace
- Empty after trim → Return None
- Check if > 50 characters → Error: "Category must be 50 characters or less"
- Return cleaned category string

### Step 5: Validate Due Date
- Trim whitespace
- Empty after trim → Return None
- Check format: YYYY-MM-DD (regex: `^\d{4}-\d{2}-\d{2}$`)
  - Invalid → Error: "Invalid date format. Use YYYY-MM-DD. Got: '{value}'"
- Parse year, month, day
- Validate month (01-12)
  - Invalid → Error: "Invalid month: {month}. Must be 01-12."
- Validate day (01-31)
  - Invalid → Error: "Invalid day: {day}. Must be 01-31."
- Create datetime object to validate calendar date
  - Invalid (e.g., Feb 31) → Error: "Invalid date: '{value}'. day is out of range..."
- Return datetime object (time = 00:00:00)

### Step 6: Validate Recurrence
- Trim and convert to lowercase
- Match against: "none", "daily", "weekly", "monthly"
- Invalid → Error: "Invalid recurrence '{value}'. Must be one of: none, daily, weekly, monthly"
- Return Recurrence enum value

### Step 7: Create Task Object
```python
task = Task(
    id=0,  # Will be assigned by storage
    title=validated_title,
    description=validated_description,
    is_completed=False,
    created_at=datetime.now(),
    priority=validated_priority,
    category=validated_category,
    due_date=validated_due_date,
    recurrence=validated_recurrence,
    parent_task_id=None
)
```

### Step 8: Store Task
- Call `storage.add(task)`
- Storage assigns auto-generated ID
- Return task with assigned ID

## Output Specification

### Success Response

```
================================================================================
Task created successfully!
ID: {assigned_id}
Title: {title}
Description: {description or "No description"}
Priority: {PRIORITY}
Category: {category or "No category"}
Due Date: {YYYY-MM-DD or "No due date"}
Recurrence: {RECURRENCE}
Status: [ ] pending
Created: {YYYY-MM-DD HH:MM:SS}
================================================================================
Press Enter to continue...
```

### Error Response

```
================================================================================
Error: {error_message}
================================================================================
Press Enter to continue...
```

## Post-Conditions

1. Task is stored in memory with unique ID
2. All validated fields are set correctly
3. Default values applied for optional fields
4. Task is visible in task list

## Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| Invalid date format | Error message, prompt again |
| Invalid calendar date (Feb 31) | Error message, prompt again |
| Leap year date (Feb 29, 2024) | Accepted as valid |
| Non-leap year date (Feb 29, 2025) | Error message |
| Empty due date | Task created with due_date=None |
| Empty recurrence | Task created with recurrence=NONE |
| Recurrence without due date | Task created, but won't auto-create next occurrences |
| Very long title (>100 chars) | Error message, prompt again |
| Very long category (>50 chars) | Error message, prompt again |

## Examples

### Example 1: Task with Due Date and Weekly Recurrence

**Input**:
```
Title: Weekly team meeting
Description: Sync on project progress
Priority: medium
Category: work
Due Date: 2025-12-30
Recurrence: weekly
```

**Output**:
```
================================================================================
Task created successfully!
ID: 10
Title: Weekly team meeting
Description: Sync on project progress
Priority: MEDIUM
Category: work
Due Date: 2025-12-30
Recurrence: WEEKLY
Status: [ ] pending
Created: 2025-12-30 14:30:00
================================================================================
Press Enter to continue...
```

### Example 2: Task with Due Date Only (No Recurrence)

**Input**:
```
Title: Pay electricity bill
Description:
Priority: high
Category:
Due Date: 2025-12-30
Recurrence: [Enter - uses default "none"]
```

**Output**:
```
================================================================================
Task created successfully!
ID: 11
Title: Pay electricity bill
Description: No description
Priority: HIGH
Category: No category
Due Date: 2025-12-30
Recurrence: NONE
Status: [ ] pending
Created: 2025-12-30 14:35:00
================================================================================
Press Enter to continue...
```

### Example 3: Error - Invalid Date Format

**Input**:
```
Title: Submit report
...
Due Date: 12/30/2025
```

**Output**:
```
================================================================================
Error: Invalid date format. Use YYYY-MM-DD. Got: '12/30/2025'
================================================================================
Press Enter to continue...
```

### Example 4: Error - Invalid Calendar Date

**Input**:
```
Title: Task
...
Due Date: 2025-02-31
```

**Output**:
```
================================================================================
Error: Invalid date: '2025-02-31'. day is out of range for month
================================================================================
Press Enter to continue...
```

## Test Cases

### TC-001: Valid task with all fields
- **Input**: All fields valid
- **Expected**: Task created with all fields

### TC-002: Task with minimal fields (title only)
- **Input**: Only title, all other fields empty
- **Expected**: Task created with defaults

### TC-003: Invalid date format
- **Input**: "30-12-2025" instead of "2025-12-30"
- **Expected**: Error message, task not created

### TC-004: Invalid calendar date
- **Input**: "2025-02-30" (February 30th)
- **Expected**: Error message, task not created

### TC-005: Leap year date valid
- **Input**: "2024-02-29" (2024 is leap year)
- **Expected**: Task created successfully

### TC-006: Non-leap year date invalid
- **Input**: "2025-02-29" (2025 is not leap year)
- **Expected**: Error message, task not created

### TC-007: Case-insensitive recurrence
- **Input**: recurrence = "WEEKLY"
- **Expected**: Task created with Recurrence.WEEKLY

### TC-008: Recurrence without due date
- **Input**: recurrence = "daily", due_date empty
- **Expected**: Task created with recurrence stored but won't auto-create

### TC-009: Title too long
- **Input**: Title with 101 characters
- **Expected**: Error message, task not created

### TC-010: Category too long
- **Input**: Category with 51 characters
- **Expected**: Error message, task not created
