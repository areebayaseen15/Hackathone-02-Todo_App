# Contract: Search Tasks by Keyword

**Feature**: Intermediate Todo Features
**Type**: CLI Command Specification
**Date**: 2025-12-29

## Command

`search_tasks` - Search for tasks by keyword in title or description

## User Flow

1. System displays "SEARCH TASKS" header
2. System prompts for keyword
3. User enters search keyword
4. System validates keyword (non-empty after trim)
5. System searches all tasks (title and description)
6. System displays matching tasks in table format
7. System displays count of matching tasks
8. System pauses for user to press Enter
9. System returns to main menu

## Input Specification

### Input

| Field | Type | Required | Validation |
|-------|------|-----------|-------------|
| `keyword` | String | Yes | Non-empty after trim, case-insensitive |

### Validation Rules

**Keyword**:
- Cannot be empty or whitespace-only
- Leading/trailing whitespace is trimmed
- Case-insensitive matching
- Searches both `title` and `description` fields
- Matches if keyword appears in either field
- Error message: "Keyword cannot be empty"

## Output Specification

### Search Display

```
================================================================================
                              SEARCH TASKS
================================================================================
Enter keyword to search: {keyword}

================================================================================
Search Results: {count} task{plural} found
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
{id}   | {PRIORITY} | {category or " "} | {[X] or [ ]} | {title}               | {created_at}
...
--------------------------------------------------------------------------------
Press Enter to continue...
```

### No Results Display

```
================================================================================
                              SEARCH TASKS
================================================================================
Enter keyword to search: {keyword}

================================================================================
No tasks found matching '{keyword}'
================================================================================
Press Enter to continue...
```

### Empty Task List Display

```
================================================================================
                              SEARCH TASKS
================================================================================
Enter keyword to search: {keyword}

================================================================================
No tasks available to search
================================================================================
Press Enter to continue...
```

## Function Signature

```python
def search_tasks(
    keyword: str,
    tasks: List[Task]
) -> List[Task]:
    """Search tasks by keyword in title or description.

    Args:
        keyword: Search keyword (non-empty)
        tasks: List of tasks to search

    Returns:
        List of tasks matching keyword (in title or description)

    Raises:
        ValueError: If keyword is empty after trim
    """
```

## Search Logic

```python
def search_tasks(keyword: str, tasks: List[Task]) -> List[Task]:
    # Validate input
    cleaned_keyword = keyword.strip()
    if not cleaned_keyword:
        raise ValueError("Keyword cannot be empty")

    # Case-insensitive matching
    keyword_lower = cleaned_keyword.casefold()

    # Search both title and description
    results = [
        task for task in tasks
        if keyword_lower in task.title.casefold()
        or keyword_lower in task.description.casefold()
    ]

    return results
```

## Success Criteria

- [ ] Keyword validation accepts non-empty strings
- [ ] Keyword validation rejects empty/whitespace strings
- [ ] Search matches tasks with keyword in title
- [ ] Search matches tasks with keyword in description
- [ ] Search is case-insensitive
- [ ] Results are displayed in table format
- [ ] "No results found" message shown when no matches
- [ ] "No tasks available" message shown when task list is empty
- [ ] Correct count of matching tasks displayed

## Edge Cases

| Scenario | Expected Behavior |
|----------|------------------|
| Keyword found in title | Task included in results |
| Keyword found in description | Task included in results |
| Keyword found in both title and description | Task included once (no duplicates) |
| Keyword not found | Empty results, "No tasks found" message |
| Empty task list | "No tasks available to search" message |
| Keyword empty string | Error: "Keyword cannot be empty" |
| Keyword whitespace-only | Error: "Keyword cannot be empty" |
| Mixed case keyword | Correctly matches (case-insensitive) |
| Partial word match | Included (substring matching) |
| Keyword with special characters | Included if substring matches |

## Dependencies

- `Task` dataclass with `title` and `description` fields
- List of tasks from storage

## User Examples

**Example 1: Found in title**
```
================================================================================
                              SEARCH TASKS
================================================================================
Enter keyword to search: report

================================================================================
Search Results: 1 task found
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | work     | [ ]         | Finish report                  | 2025-12-29 11:45:00
--------------------------------------------------------------------------------
Press Enter to continue...
```

**Example 2: Found in description**
```
================================================================================
                              SEARCH TASKS
================================================================================
Enter keyword to search: milk

================================================================================
Search Results: 1 task found
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
5     | HIGH     | shopping | [ ]         | Buy groceries                  | 2025-12-29 12:30:00
--------------------------------------------------------------------------------
Press Enter to continue...
```

**Example 3: Multiple results**
```
================================================================================
                              SEARCH TASKS
================================================================================
Enter keyword to search: task

================================================================================
Search Results: 3 tasks found
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | work     | [ ]         | Finish task report            | 2025-12-29 11:45:00
2     | MEDIUM   |         | [X]         | Complete daily tasks           | 2025-12-29 09:15:00
3     | LOW      | personal | [ ]         | New task entry                 | 2025-12-29 10:30:00
--------------------------------------------------------------------------------
Press Enter to continue...
```

**Example 4: No results**
```
================================================================================
                              SEARCH TASKS
================================================================================
Enter keyword to search: vacation

================================================================================
No tasks found matching 'vacation'
================================================================================
Press Enter to continue...
```

**Example 5: Empty keyword**
```
================================================================================
                              SEARCH TASKS
================================================================================
Enter keyword to search:

Error: Keyword cannot be empty
Enter keyword to search:
```

**Example 6: Case-insensitive matching**
```
================================================================================
                              SEARCH TASKS
================================================================================
Enter keyword to search: BUY

# Matches: "Buy groceries" (case-insensitive)
================================================================================
```

---

*This contract defines the Search Tasks command with keyword matching.*
