# Feature Specification: Intermediate Todo Features

**Feature Branch**: `1-intermediate-features`
**Created**: 2025-12-29
**Status**: Draft
**Input**: User description: "The Todo App needs intermediate features added:

1. Priorities (high/medium/low)
2. Categories/tags
3. Search by keyword
4. Filter by status, priority, and category
5. Sort tasks by priority and alphabetically

This is for Phase I (in-memory Python console app). Do NOT suggest any UI or frontend.

Include:
- Updated task data structure
- Expected console inputs/outputs for each feature
- Edge cases
- Assumptions"

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Task Priorities (Priority: P1)

As a user, I want to assign priority levels (high, medium, low) to my tasks so that I can focus on the most important tasks first.

**Why this priority**: Priorities are fundamental to task management and enable all subsequent filtering and sorting capabilities. This is the most impactful enhancement for organizing tasks.

**Independent Test**: Can be fully tested by creating tasks with different priority levels, updating priorities, and viewing tasks to confirm priority is displayed correctly. Delivers immediate value by allowing users to distinguish urgent tasks from less important ones.

**Acceptance Scenarios**:

1. **Given** a new task is being created, **When** user is prompted for priority, **Then** the system accepts high/medium/low (case-insensitive) and sets the task priority accordingly
2. **Given** an existing task, **When** user updates the priority, **Then** the task's priority is updated to the new value
3. **Given** tasks are being viewed, **When** the task list is displayed, **Then** each task shows its priority level in the display
4. **Given** the user is creating a task, **When** they provide an invalid priority, **Then** the system displays an error and prompts again

---

### User Story 2 - Task Categories and Tags (Priority: P2)

As a user, I want to assign categories or tags to my tasks so that I can group related tasks together (e.g., work, personal, shopping, health).

**Why this priority**: Categories help users organize tasks by context or project type, which is a common need for personal task management. This is secondary to priorities but still highly valuable for task organization.

**Independent Test**: Can be fully tested by creating tasks with categories, viewing tasks filtered by category, and updating task categories. Delivers value by allowing users to find all related tasks quickly.

**Acceptance Scenarios**:

1. **Given** a new task is being created, **When** user enters a category, **Then** the system stores the category with the task
2. **Given** a new task is being created, **When** user leaves category blank, **Then** the system stores the task with no category
3. **Given** an existing task, **When** user updates its category, **Then** the task's category is updated to the new value
4. **Given** tasks are being filtered, **When** user selects a category to filter by, **Then** only tasks matching that category are displayed

---

### User Story 3 - Search Tasks by Keyword (Priority: P3)

As a user, I want to search for tasks by keyword so that I can quickly find specific tasks without scrolling through a long list.

**Why this priority**: Search improves usability as the number of tasks grows, but is less fundamental than priorities and categories. Users can still find tasks by viewing the full list.

**Independent Test**: Can be fully tested by entering various keywords and verifying matching tasks are displayed while non-matching tasks are excluded. Delivers value by improving task retrieval efficiency.

**Acceptance Scenarios**:

1. **Given** the user selects search option, **When** user enters a keyword, **Then** the system displays all tasks with that keyword in title or description
2. **Given** the user searches for "buy", **When** tasks include "Buy groceries" and "Call dentist", **Then** only "Buy groceries" is displayed
3. **Given** the user searches for a keyword, **When** no tasks match, **Then** the system displays a "no results found" message
4. **Given** the user searches with an empty keyword, **When** search is executed, **Then** the system displays an error or prompts for a keyword

---

### User Story 4 - Filter Tasks by Status, Priority, and Category (Priority: P4)

As a user, I want to filter my task list by status, priority, or category so that I can focus on specific subsets of tasks.

**Why this priority**: Filtering builds upon priorities and categories, allowing users to view specific task subsets. This is useful but not as critical as the base features.

**Independent Test**: Can be fully tested by applying each filter type individually and in combination, verifying only matching tasks are displayed. Delivers value by enabling focused task views.

**Acceptance Scenarios**:

1. **Given** the user selects to filter by status, **When** they choose "pending", **Then** only incomplete tasks are displayed
2. **Given** the user selects to filter by status, **When** they choose "completed", **Then** only completed tasks are displayed
3. **Given** the user selects to filter by priority, **When** they choose "high", **Then** only high-priority tasks are displayed
4. **Given** the user selects to filter by category, **When** they choose "work", **Then** only tasks in the "work" category are displayed
5. **Given** the user applies multiple filters, **When** they filter by both priority and status, **Then** only tasks matching ALL criteria are displayed
6. **Given** filters are active, **When** the user clears filters, **Then** all tasks are displayed again

---

### User Story 5 - Sort Tasks by Priority and Alphabetically (Priority: P5)

As a user, I want to sort my task list by priority or alphabetically so that I can view tasks in a meaningful order.

**Why this priority**: Sorting improves task list organization but is the least critical feature. Users can still work with unsorted lists.

**Independent Test**: Can be fully tested by applying different sort options and verifying tasks are displayed in the correct order. Delivers value by providing multiple viewing perspectives.

**Acceptance Scenarios**:

1. **Given** the user selects sort by priority, **When** the task list is displayed, **Then** tasks are ordered: high first, then medium, then low
2. **Given** the user selects sort by priority, **When** multiple tasks have the same priority, **Then** those tasks are ordered by creation date (newest first)
3. **Given** the user selects sort alphabetically, **When** the task list is displayed, **Then** tasks are ordered A-Z by title
4. **Given** the user selects sort alphabetically, **When** multiple tasks have the same title, **Then** those tasks are ordered by creation date (newest first)
5. **Given** the user has an active sort, **When** they clear the sort, **Then** tasks return to default order (by ID/creation date)

---

### Edge Cases

- What happens when a user enters an invalid priority value (e.g., "urgent" instead of "high/medium/low")? System displays error message and prompts again.
- What happens when a user creates a task without specifying a priority? System uses "medium" as the default priority.
- What happens when a user enters an empty category string? System treats this as no category (category field is empty/None).
- What happens when a user searches for an empty string or just whitespace? System displays error message asking for a non-empty keyword.
- What happens when all tasks are filtered out (no tasks match criteria)? System displays "No tasks match the current filters" message.
- What happens when searching for a keyword with mixed case? Search is case-insensitive (e.g., "BUY" matches "Buy groceries").
- What happens when categories contain special characters? System accepts any printable characters in category names.
- What happens when user enters a very long category name (over 50 characters)? System displays error or truncates to maximum length (50 characters assumed).
- What happens when sorting with no tasks? System displays "No tasks found" message rather than error.
- What happens when multiple filters conflict (e.g., status=pending AND status=completed)? System displays no tasks or error depending on implementation.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to specify a priority when creating a task (options: high, medium, low)
- **FR-002**: System MUST accept priority values case-insensitively (HIGH, high, High are all valid)
- **FR-003**: System MUST default task priority to "medium" when not specified
- **FR-004**: System MUST allow users to update the priority of existing tasks
- **FR-005**: System MUST validate priority values and reject invalid entries
- **FR-006**: System MUST display priority in the task list view
- **FR-007**: System MUST allow users to assign a category/tag to tasks when creating them
- **FR-008**: System MUST allow users to leave category empty (optional field)
- **FR-009**: System MUST allow users to update the category of existing tasks
- **FR-010**: System MUST limit category names to a maximum of 50 characters
- **FR-011**: System MUST allow users to search tasks by keyword matching title or description fields
- **FR-012**: System MUST perform keyword search case-insensitively
- **FR-013**: System MUST allow users to filter tasks by status (pending/completed)
- **FR-014**: System MUST allow users to filter tasks by priority (high/medium/low)
- **FR-015**: System MUST allow users to filter tasks by category
- **FR-016**: System MUST allow users to apply multiple filters simultaneously (AND logic)
- **FR-017**: System MUST allow users to clear all filters and return to unfiltered view
- **FR-018**: System MUST allow users to sort tasks by priority (high → medium → low)
- **FR-019**: System MUST allow users to sort tasks alphabetically by title (A → Z)
- **FR-020**: System MUST allow users to return to default sort order (by ID/creation date)
- **FR-021**: System MUST maintain secondary sort order by creation date within primary sort groups

### Key Entities *(include if feature involves data)*

- **Task**: A todo item with enhanced attributes including priority, category, and existing fields (id, title, description, is_completed, created_at). Priority indicates urgency (high/medium/low). Category provides optional grouping capability. Search, filter, and sort operations operate on task collections.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a task with specified priority in under 30 seconds
- **SC-002**: Users can search and find a specific task within 5 seconds in a list of 100+ tasks
- **SC-003**: 95% of users successfully apply filters on first attempt without errors
- **SC-004**: Users can change task priority in 3 or fewer steps
- **SC-005**: Users can apply combined filters (status + priority) in under 15 seconds
- **SC-006**: Task list displays correctly ordered tasks within 1 second for lists up to 200 tasks
- **SC-007**: Users report 80% improvement in task finding efficiency compared to unsorted list

---

## Assumptions

1. **Priority Default**: When users do not specify a priority, the system defaults to "medium" as a balanced choice.
2. **Category Format**: Categories are simple text strings without hierarchical structure (no subcategories).
3. **Search Scope**: Keyword search only searches task title and description fields, not other metadata.
4. **Filter Behavior**: Multiple filters use AND logic (task must match all active filters to be displayed).
5. **Sort Stability**: Within equal priority/title groups, tasks are sorted by creation date (newest first).
6. **Category Limits**: Category names are limited to 50 characters to maintain display readability.
7. **Case Insensitivity**: All text matching (priority, search, categories) is case-insensitive for user convenience.
8. **Existing Tasks**: The system must handle existing tasks (created before these features) by assigning default values (priority=medium, category=none).
9. **In-Memory Storage**: All data remains in-memory per Phase I constraints; no persistence of priorities, categories, or search history.

---

## Console Input/Output Examples

### Add Task with Priority and Category

```
================================================================================
                              ADD TASK
================================================================================
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
Press Enter to continue...
```

### View Tasks with Enhanced Display

```
================================================================================
                              YOUR TASKS
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | work     | [ ]         | Finish report                  | 2025-12-29 11:45:00
2     | MEDIUM   | personal | [X]         | Call dentist                   | 2025-12-29 09:15:00
3     | LOW      |         | [ ]         | Buy groceries                  | 2025-12-29 10:30:00
4     | HIGH     | work     | [ ]         | Prepare presentation           | 2025-12-29 12:00:00
--------------------------------------------------------------------------------
Total: 4 tasks (1 completed, 3 pending)
================================================================================
```

### Search by Keyword

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

### Filter Tasks

```
================================================================================
                            FILTER TASKS
================================================================================
Available filters:
  [1] By Status (pending/completed)
  [2] By Priority (high/medium/low)
  [3] By Category
  [4] Clear All Filters
  [5] Back to Main Menu

Enter your choice: 2
Enter priority to filter (high/medium/low): high

================================================================================
Filtered Tasks: 2 tasks (priority: HIGH)
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | work     | [ ]         | Finish report                  | 2025-12-29 11:45:00
4     | HIGH     | work     | [ ]         | Prepare presentation           | 2025-12-29 12:00:00
--------------------------------------------------------------------------------
Press Enter to continue...
```

### Sort Tasks

```
================================================================================
                            SORT TASKS
================================================================================
Available sort options:
  [1] Sort by Priority (HIGH → MEDIUM → LOW)
  [2] Sort Alphabetically by Title (A → Z)
  [3] Default Order (by ID)
  [4] Back to Main Menu

Enter your choice: 1

================================================================================
Tasks sorted by priority
================================================================================
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | work     | [ ]         | Finish report                  | 2025-12-29 11:45:00
4     | HIGH     | work     | [ ]         | Prepare presentation           | 2025-12-29 12:00:00
3     | LOW      |         | [ ]         | Buy groceries                  | 2025-12-29 10:30:00
2     | MEDIUM   | personal | [X]         | Call dentist                   | 2025-12-29 09:15:00
--------------------------------------------------------------------------------
Press Enter to continue...
```

---

## Updated Task Data Structure

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Unique, Auto-generated, Positive | Unique identifier for the task |
| `title` | String | Required, 1-100 characters | Short descriptive name of the task |
| `description` | String | Optional, 0-500 characters | Detailed description of the task |
| `is_completed` | Boolean | Default: False | Completion status of the task |
| `created_at` | DateTime | Auto-generated, Immutable | Timestamp when task was created |
| `priority` | Enum | Required, Values: high/medium/low, Default: medium | Priority level of the task |
| `category` | String | Optional, 0-50 characters | Category or tag for grouping |

---

*This specification adds intermediate organization features to the Phase I Todo App while maintaining the in-memory, console-based constraints.*
