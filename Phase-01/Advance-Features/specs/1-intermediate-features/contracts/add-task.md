# Contract: Add Task with Priority and Category

**Feature**: Intermediate Todo Features
**Type**: CLI Command Specification
**Date**: 2025-12-29

## Command

`add_task` - Create a new task with title, description, priority, and optional category

## User Flow

1. System displays "ADD TASK" header
2. System prompts for task title (required)
3. User enters title
4. System validates title (1-100 chars, non-empty)
5. System prompts for task description (optional)
6. User enters description or presses Enter to skip
7. System validates description (0-500 chars)
8. System prompts for priority (high/medium/low, default: medium)
9. User enters priority or presses Enter for default
10. System validates priority (case-insensitive)
11. System prompts for category (optional)
12. User enters category or presses Enter to skip
13. System validates category (0-50 chars)
14. System creates Task object with auto-generated ID and timestamp
15. System displays confirmation with all task details
16. System pauses for user to press Enter
17. System returns to main menu

## Input Specification

### Inputs

| Step | Field | Type | Required | Validation | Default |
|-------|-------|------|-----------|-------------|----------|
| 1 | `title` | String | Yes | 1-100 chars, non-empty after trim | None |
| 2 | `description` | String | No | 0-500 chars | Empty string |
| 3 | `priority` | String | No | "high"/"medium"/"low" (case-insensitive) | "medium" |
| 4 | `category` | String | No | 0-50 chars | None |

### Validation Rules

**Title**:
- Cannot be empty or whitespace-only
- Must be 1-100 characters after trimming
- Leading/trailing whitespace is trimmed
- Error message: "Title cannot be empty" or "Title must be 100 characters or less"

**Description**:
- Can be empty (press Enter to skip)
- Maximum 500 characters
- Leading/trailing whitespace is trimmed
- Error message: "Description must be 500 characters or less"

**Priority**:
- Case-insensitive: "high", "HIGH", "High" all valid
- Accepts "high", "medium", "low"
- Default: "medium" if user presses Enter
- Error message: "Invalid priority '{input}'. Must be one of: high, medium, low"

**Category**:
- Can be empty (press Enter to skip)
- Maximum 50 characters
- Leading/trailing whitespace is trimmed
- Empty string after trim treated as None (no category)
- Error message: "Category must be 50 characters or less"

## Output Specification

### Confirmation Display

```
================================================================================
Task created successfully!
ID: {id}
Title: {title}
Description: {description or "None"}
Priority: {PRIORITY}  # Uppercase
Category: {category or "None"}
Status: [ ] pending
Created: {YYYY-MM-DD HH:MM:SS}
================================================================================
Press Enter to continue...
```

### Error Messages

| Condition | Error Message |
|-----------|---------------|
| Empty title | "Title cannot be empty" |
| Title > 100 chars | "Title must be 100 characters or less" |
| Description > 500 chars | "Description must be 500 characters or less" |
| Invalid priority | "Invalid priority '{value}'. Must be one of: high, medium, low" |
| Category > 50 chars | "Category must be 50 characters or less" |

## Function Signature

```python
def add_task(
    title: str,
    description: str = "",
    priority_str: str = "medium",
    category_str: str = ""
) -> Task:
    """Create a new task with the specified attributes.

    Args:
        title: Task title (1-100 characters, required)
        description: Task description (0-500 characters, optional)
        priority_str: Priority string ("high"/"medium"/"low", default: "medium")
        category_str: Category string (0-50 characters, optional)

    Returns:
        Created Task object

    Raises:
        ValueError: If validation fails for any field
    """
```

## Data Model

```python
Task(
    id=auto_generated_id(),
    title=title,
    description=description or "",
    is_completed=False,
    created_at=datetime.now(),
    priority=validate_priority(priority_str),
    category=validate_category(category_str) or None
)
```

## Success Criteria

- [ ] Task is created with valid ID
- [ ] All fields are validated according to rules
- [ ] Priority defaults to MEDIUM when not specified
- [ ] Category is None when not specified
- [ ] Confirmation displays all task details correctly
- [ ] Error messages are clear and user-friendly
- [ ] Invalid input prompts for re-entry

## Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| All fields provided | Task created with all values |
| Only title provided | Task created with default priority (MEDIUM) and no category |
| Description provided with Enter | Description stored as empty string |
| Priority blank (Enter) | Priority defaults to MEDIUM |
| Category blank (Enter) | Category set to None |
| Category whitespace-only | Category set to None after trim |
| Priority mixed case | Parsed correctly (case-insensitive) |
| Title exactly 100 chars | Accepted |
| Title 101 chars | Error displayed |
| Category exactly 50 chars | Accepted |
| Category 51 chars | Error displayed |

## Dependencies

- `validate_priority(priority_str: str) -> Priority`
- `validate_category(category_str: str) -> Optional[str]`
- `Task` dataclass with new fields
- Storage `add(task: Task)` method
- Storage `next_id()` method

## User Examples

**Example 1: All fields provided**
```
Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): Get milk, eggs, bread
Enter priority (high/medium/low, default: medium): high
Enter category (optional, press Enter to skip): shopping

================================================================================
Task created successfully!
ID: 5
Title: Buy groceries
Description: Get milk, eggs, bread
Priority: HIGH
Category: shopping
Status: [ ] pending
Created: 2025-12-29 12:30:00
================================================================================
```

**Example 2: Title only**
```
Enter task title: Call mom
Enter task description (optional, press Enter to skip): [Enter]
Enter priority (high/medium/low, default: medium): [Enter]
Enter category (optional, press Enter to skip): [Enter]

================================================================================
Task created successfully!
ID: 6
Title: Call mom
Description: None
Priority: MEDIUM
Category: None
Status: [ ] pending
Created: 2025-12-29 12:31:00
================================================================================
```

**Example 3: Invalid priority**
```
Enter task title: Urgent task
Enter task description (optional, press Enter to skip): [Enter]
Enter priority (high/medium/low, default: medium): urgent
Error: Invalid priority 'urgent'. Must be one of: high, medium, low
Enter priority (high/medium/low, default: medium): high
Enter category (optional, press Enter to skip): [Enter]
...
```

---

*This contract defines the Add Task command with priority and category support.*
