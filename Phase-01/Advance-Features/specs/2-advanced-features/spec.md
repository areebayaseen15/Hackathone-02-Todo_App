# Feature Specification: Advanced Todo Features

**Feature Branch**: `2-advanced-features`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "The Todo App needs advanced features added:

1. Recurring Tasks (daily, weekly, monthly)
2. Due Dates & Deadlines with validation
3. Task Analytics (console-friendly)
4. Smart Task Views (Today's, Upcoming, Overdue)

This is for Phase I (in-memory Python console app). Do NOT suggest any UI or frontend.

Include:
- Updated task data structure
- Expected console inputs/outputs for each feature
- Edge cases
- Assumptions
- Acceptance criteria"

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Recurring Tasks (Priority: P1)

As a user, I want to set tasks to repeat (daily, weekly, monthly) so that I don't have to manually recreate repetitive tasks.

**Why this priority**: Recurring tasks are a powerful productivity feature that significantly reduces manual task entry for routine activities. This is the most impactful advanced feature.

**Independent Test**: Can be fully tested by creating a recurring task, marking it complete, and verifying the next occurrence is automatically created. Delivers immediate value by eliminating repetitive task creation.

**Acceptance Scenarios**:

1. **Given** a new task is being created, **When** user specifies recurrence (daily/weekly/monthly), **Then** the task is marked as recurring with the specified pattern
2. **Given** a recurring task has a due date, **When** the task is marked complete, **Then** a new occurrence is automatically created with the next due date based on recurrence pattern
3. **Given** a daily recurring task due on Monday, **When** completed, **Then** the next occurrence's due date is Tuesday
4. **Given** a weekly recurring task due on Monday, **When** completed, **Then** the next occurrence's due date is next Monday
5. **Given** a monthly recurring task due on the 15th, **When** completed, **Then** the next occurrence's due date is the 15th of next month
6. **Given** a recurring task is completed, **When** the new occurrence is created, **Then** it references the original task via parent_task_id
7. **Given** a recurring task has no due date, **When** it is marked complete, **Then** no new occurrence is created (recurrence requires due date)

---

### User Story 2 - Due Dates & Deadlines (Priority: P1)

As a user, I want to assign due dates to tasks so that I can track time-sensitive tasks and see overdue items.

**Why this priority**: Due dates are fundamental to time management and task prioritization. This feature works in tandem with analytics and smart views.

**Independent Test**: Can be fully tested by creating tasks with due dates, viewing tasks to see overdue indicators, and updating due dates. Delivers value by providing time-aware task management.

**Acceptance Scenarios**:

1. **Given** a new task is being created, **When** user enters a due date in YYYY-MM-DD format, **Then** the system validates and stores the date
2. **Given** the user enters an invalid date format, **When** creating or updating a task, **Then** the system displays an error and prompts again
3. **Given** tasks are being viewed, **When** a task is overdue (due date < today), **Then** the task displays an "OVERDUE" indicator
4. **Given** tasks are being viewed, **When** a task is due today, **Then** the task displays "TODAY" instead of the date
5. **Given** a task has no due date, **When** viewing the task list, **Then** it displays "No due date"
6. **Given** the user enters a date like "2025-02-31" (February 31st), **When** creating or updating, **Then** the system rejects the invalid calendar date
7. **Given** the user wants to update a due date, **When** modifying an existing task, **Then** they can enter a new date or press Enter to keep current

---

### User Story 3 - Task Analytics (Priority: P2)

As a user, I want to see task analytics so that I can understand my task patterns and overall progress.

**Why this priority**: Analytics provide insights into task management effectiveness but are not essential for basic functionality. Users can track progress manually.

**Independent Test**: Can be fully tested by viewing the analytics screen and verifying counts and breakdowns match the actual task data. Delivers value by providing visibility into task distribution.

**Acceptance Scenarios**:

1. **Given** the user views analytics, **When** analytics are displayed, **Then** total tasks count is shown
2. **Given** the user views analytics, **When** analytics are displayed, **Then** completed vs pending tasks are shown with percentages
3. **Given** the user views analytics, **When** analytics are displayed, **Then** overdue tasks count is shown
4. **Given** the user views analytics, **When** analytics are displayed, **Then** tasks are broken down by priority with overdue counts
5. **Given** the user views analytics, **When** analytics are displayed, **Then** tasks are broken down by category
6. **Given** some tasks have no category, **When** analytics show category breakdown, **Then** tasks without category are excluded from breakdown
7. **Given** there are no tasks, **When** analytics are viewed, **Then** all counts show 0

---

### User Story 4 - Smart Task Views (Priority: P2)

As a user, I want to see smart views (Today's, Upcoming, Overdue) so that I can focus on time-sensitive tasks without scanning the entire list.

**Why this priority**: Smart views improve task focus and productivity but are secondary to core functionality. Users can still find tasks by searching/filtering.

**Independent Test**: Can be fully tested by selecting each smart view and verifying the displayed tasks match the expected criteria. Delivers value by providing quick access to time-critical tasks.

**Acceptance Scenarios**:

1. **Given** the user selects "Today's Tasks", **When** tasks are displayed, **Then** only tasks due today or overdue are shown
2. **Given** the user selects "Upcoming Tasks", **When** tasks are displayed, **Then** only tasks with future due dates are shown
3. **Given** the user selects "Overdue Tasks", **When** tasks are displayed, **Then** only tasks past their due date are shown with days overdue
4. **Given** the user views Today's Tasks, **When** overdue tasks are included, **Then** they are clearly marked as OVERDUE
5. **Given** no tasks match the smart view criteria, **When** the view is displayed, **Then** a message indicates no tasks were found
6. **Given** tasks have no due date, **When** viewing any smart view, **Then** they are excluded from the results

---

## Edge Cases

- What happens when a user enters an invalid date format (e.g., "12/30/2025" or "today")? System displays error message requiring YYYY-MM-DD format.
- What happens when a user enters an impossible date (e.g., "2025-02-30")? System validates calendar date and rejects invalid dates.
- What happens when a recurring task has no due date? System stores recurrence but does not auto-create next occurrences.
- What happens when a recurring task is deleted? Parent and all child tasks in the chain remain independent (no cascade delete).
- What happens when today is January 31st and a monthly recurring task is completed? Next occurrence uses February 28th (or 29th in leap years).
- What happens when a leap year calculation is needed for February 29th? System correctly identifies leap years (divisible by 4, except centuries unless divisible by 400).
- What happens when a user toggles a completed recurring task back to incomplete? No change; next occurrence already created.
- What happens when viewing analytics with no tasks? All counts show 0 and percentage displays 0.0%.
- What happens when viewing overdue view and no tasks are overdue? System displays "No overdue tasks" message.
- What happens when a task is completed multiple times (toggle on/off multiple times)? Each toggle to complete creates a new occurrence if recurrence is set.
- What happens when parent_task_id references a deleted task? Child task remains functional; parent reference is informational only.
- What happens when a task is created with a past due date? System accepts the date and marks as overdue.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to specify a due date when creating a task (format: YYYY-MM-DD)
- **FR-002**: System MUST validate due date format as YYYY-MM-DD
- **FR-003**: System MUST validate calendar dates (reject Feb 31, Apr 31, etc.)
- **FR-004**: System MUST correctly handle leap years for February 29th
- **FR-005**: System MUST allow users to leave due date empty (optional field)
- **FR-006**: System MUST display overdue indicators for tasks with due_date < today
- **FR-007**: System MUST display "TODAY" for tasks due on current date
- **FR-008**: System MUST display "No due date" for tasks without due dates
- **FR-009**: System MUST allow users to update due dates on existing tasks
- **FR-010**: System MUST allow users to specify recurrence (none/daily/weekly/monthly)
- **FR-011**: System MUST accept recurrence values case-insensitively
- **FR-012**: System MUST default recurrence to "none" when not specified
- **FR-013**: System MUST automatically create next occurrence when a recurring task with due date is completed
- **FR-014**: System MUST calculate next due date based on recurrence pattern (daily=+1 day, weekly=+7 days, monthly=+1 month)
- **FR-015**: System MUST set parent_task_id on new occurrences to reference the completed task
- **FR-016**: System MUST NOT create next occurrence for recurring tasks without due dates
- **FR-017**: System MUST display task analytics showing total, completed, pending, and overdue counts
- **FR-018**: System MUST calculate and display completion percentage
- **FR-019**: System MUST break down tasks by priority in analytics
- **FR-020**: System MUST break down tasks by category in analytics
- **FR-021**: System MUST provide "Today's Tasks" view showing tasks due today or overdue
- **FR-022**: System MUST provide "Upcoming Tasks" view showing tasks with future due dates
- **FR-023**: System MUST provide "Overdue Tasks" view showing tasks past due date with days overdue
- **FR-024**: System MUST handle month-end edge cases for monthly recurrence (Jan 31 → Feb 28/29)

### Key Entities *(include if feature involves data)*

- **Task**: Extended with due_date (optional date), recurrence (enum: none/daily/weekly/monthly), and parent_task_id (optional reference to originating task). Due dates drive time-sensitive views and analytics. Recurrence enables automatic task regeneration. Parent_task_id tracks recurring task chains.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a task with due date in under 30 seconds
- **SC-002**: Users can set up a recurring task in under 40 seconds
- **SC-003**: 95% of users successfully create recurring tasks on first attempt without errors
- **SC-004**: Recurring task auto-creation occurs within 100ms of completion
- **SC-005**: Analytics screen displays all statistics within 1 second for lists up to 200 tasks
- **SC-006**: Smart views load within 500ms for lists up to 200 tasks
- **SC-007**: Users report 70% reduction in time spent managing recurring tasks
- **SC-008**: Date validation catches 100% of invalid calendar dates

---

## Assumptions

1. **Due Date Format**: Users must enter dates in YYYY-MM-DD format; no support for relative dates like "tomorrow" or "next week".
2. **Time Component**: Due dates are date-only (no time component); all times default to midnight.
3. **Recurrence Scope**: Recurrence creates next occurrence only; no scheduling of future occurrences beyond the next one.
4. **Recurrence Reset**: When completing a recurring task, the original task's is_completed status changes to True; only the new occurrence is pending.
5. **Parent Reference**: parent_task_id is informational only; deletion of parent does not affect child tasks.
6. **No Reminders**: System does not proactively notify users of upcoming or overdue tasks; users must view analytics or smart views to check.
7. **In-Memory Only**: All recurring task chains and analytics are lost on application exit (Phase I constraint).
8. **Existing Tasks**: Tasks created before this feature are assigned default values (due_date=None, recurrence=NONE, parent_task_id=None).
9. **Analytics Scope**: Analytics reflect current state only; no historical tracking or trends.
10. **Month Handling**: Monthly recurrence from 31st moves to last day of next month if no matching date (e.g., Jan 31 → Feb 28).

---

## Console Input/Output Examples

### Add Task with Due Date and Recurrence

```
================================================================================
                              ADD TASK
================================================================================
Enter task title: Weekly team meeting
Enter task description (optional, press Enter to skip): Sync on project progress
Enter priority (high/medium/low, default: medium): medium
Enter category (optional, press Enter to skip): work
Enter due date (YYYY-MM-DD, optional, press Enter to skip): 2025-12-30
Enter recurrence (none/daily/weekly/monthly, default: none): weekly

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

### View Tasks with Due Date and Overdue Display

```
================================================================================
                              YOUR TASKS
================================================================================
ID    | Priority | Due Date    | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | 2025-12-28  | [X] OVERDUE  | Pay electricity bill           | 2025-12-25 09:00:00
2     | MEDIUM   | 2025-12-30  | [ ]          | Submit report                  | 2025-12-28 11:45:00
3     | HIGH     | TODAY       | [ ]          | Call dentist                   | 2025-12-29 10:30:00
4     | LOW      | 2025-01-15  | [ ]          | Renew insurance                | 2025-12-30 08:00:00
5     | MEDIUM   | No due date | [X]          | Buy groceries                  | 2025-12-30 12:00:00
--------------------------------------------------------------------------------
Total: 5 tasks (1 completed, 4 pending, 1 overdue)
================================================================================
```

### Update Task Due Date and Recurrence

```
================================================================================
                              UPDATE TASK
================================================================================
Enter task ID to update: 2

Current Task:
ID: 2
Title: Submit report
Description: Finalize quarterly analysis
Priority: MEDIUM
Category: work
Due Date: 2025-12-30
Recurrence: none
Status: [ ] pending

Enter new title (or press Enter to keep current):
Enter new description (or press Enter to keep current):
Enter new due date (YYYY-MM-DD, or press Enter to keep current): 2025-01-02
Enter new priority (high/medium/low, or press Enter to keep current):
Enter new category (or press Enter to keep current):
Enter new recurrence (none/daily/weekly/monthly, or press Enter to keep current): weekly

================================================================================
Task updated successfully!
ID: 2
Title: Submit report
Due Date: 2025-01-02
Recurrence: WEEKLY
Status: [ ] pending
================================================================================
Press Enter to continue...
```

### Complete Recurring Task (Auto-Create Next)

```
================================================================================
                              TOGGLE TASK
================================================================================
Enter task ID to toggle status: 10

Task completed! Next occurrence created.
New task ID: 11
Next due date: 2025-01-06

Original Task:
ID: 10
Title: Weekly team meeting
Recurrence: WEEKLY
Due Date: 2025-12-30
Status: [X] completed

Next Occurrence:
ID: 11
Title: Weekly team meeting
Recurrence: WEEKLY
Due Date: 2025-01-06
Status: [ ] pending
Parent Task ID: 10
================================================================================
Press Enter to continue...
```

### View Task Analytics

```
================================================================================
                           TASK ANALYTICS
================================================================================
Total Tasks: 15
Completed: 6 tasks (40.0%)
Pending: 9 tasks (60.0%)
Overdue: 2 tasks

Breakdown by Priority:
  HIGH:   3 tasks (2 overdue)
  MEDIUM: 8 tasks (0 overdue)
  LOW:    4 tasks (0 overdue)

Breakdown by Category:
  work:      6 tasks
  personal:  5 tasks
  shopping:  2 tasks
  health:    2 tasks
================================================================================
Press Enter to continue...
```

### Smart View - Today's Tasks

```
================================================================================
                           TODAY'S TASKS
================================================================================
Showing tasks due today or overdue
================================================================================
ID    | Priority | Due Date    | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | 2025-12-28  | [X] OVERDUE  | Pay electricity bill           | 2025-12-25 09:00:00
3     | HIGH     | TODAY       | [ ]          | Call dentist                   | 2025-12-29 10:30:00
7     | MEDIUM   | TODAY       | [ ]          | Review pull request            | 2025-12-30 14:00:00
--------------------------------------------------------------------------------
Total: 3 tasks (1 completed, 2 pending, 1 overdue)
================================================================================
Press Enter to continue...
```

### Smart View - Upcoming Tasks

```
================================================================================
                          UPCOMING TASKS
================================================================================
Showing tasks with future due dates
================================================================================
ID    | Priority | Due Date    | Status      | Title                          | Created
--------------------------------------------------------------------------------
4     | LOW      | 2025-01-15  | [ ]          | Renew insurance                | 2025-12-30 08:00:00
8     | HIGH     | 2025-01-10  | [ ]          | Prepare presentation           | 2025-12-30 15:30:00
11    | MEDIUM   | 2025-01-13  | [ ]          | Weekly team meeting            | 2025-12-30 16:00:00
--------------------------------------------------------------------------------
Total: 3 tasks (all pending)
================================================================================
Press Enter to continue...
```

### Smart View - Overdue Tasks

```
================================================================================
                          OVERDUE TASKS
================================================================================
Showing tasks past their due date
================================================================================
ID    | Priority | Due Date    | Days Overdue | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | 2025-12-28  | 2            | Pay electricity bill           | 2025-12-25 09:00:00
5     | MEDIUM   | 2025-12-25  | 5            | Submit expense report          | 2025-12-20 11:00:00
--------------------------------------------------------------------------------
Total: 2 overdue tasks
================================================================================
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
| `due_date` | Optional[DateTime] | Optional, YYYY-MM-DD format | Due date or deadline for the task |
| `recurrence` | Enum | Optional, Values: none/daily/weekly/monthly, Default: none | Recurrence pattern for task |
| `parent_task_id` | Optional[Integer] | Optional, References valid task ID | ID of parent task (for recurring task chain) |

---

## Validation Rules

### Due Date Validation

**Format Requirements**:
- Must be in YYYY-MM-DD format (ISO 8601)
- Year: 4 digits (e.g., 2025)
- Month: 2 digits (01-12)
- Day: 2 digits (01-31, depending on month)
- Separators: Must use hyphens (-)

**Calendar Validity**:
- Days must be valid for the specified month
- February 31 is invalid (must be 28 or 29 in leap years)
- April 31 is invalid (April has 30 days)
- Leap years calculated correctly (divisible by 4, but not by 100 unless also divisible by 400)

**Edge Cases**:
- Empty string after trim = no due date
- Whitespace-only string = no due date
- Format other than YYYY-MM-DD = error
- Invalid calendar date = error

### Recurrence Validation

**Valid Values**:
- "none", "daily", "weekly", "monthly"
- Case-insensitive (NONE, None, none all valid)
- Default: "none"

**Recurrence Requirements**:
- To create next occurrences, a due_date must be present
- Without due_date, recurrence is stored but no auto-creation occurs

---

## Backward Compatibility

### Existing Task Migration

Tasks created before this feature will lack `due_date`, `recurrence`, and `parent_task_id` attributes.

**Migration Strategy** (Session-based, in-memory):
```python
# When loading existing tasks, check for missing attributes
def ensure_task_compatibility(task: Task) -> Task:
    """Ensure task has all required attributes."""
    if not hasattr(task, 'priority'):
        task.priority = Priority.MEDIUM
    if not hasattr(task, 'category'):
        task.category = None
    if not hasattr(task, 'due_date'):
        task.due_date = None
    if not hasattr(task, 'recurrence'):
        task.recurrence = Recurrence.NONE
    if not hasattr(task, 'parent_task_id'):
        task.parent_task_id = None
    return task
```

---

## CLI Command Additions

### New Main Menu Options

```
================================================================================
                          TODO APPLICATION
================================================================================
  [1] View All Tasks
  [2] Add Task
  [3] Update Task
  [4] Delete Task
  [5] Mark Task as Complete/Incomplete
  [6] Search Tasks
  [7] Filter Tasks
  [8] Sort Tasks
  [9] View Analytics              [NEW]
  [10] Today's Tasks              [NEW]
  [11] Upcoming Tasks            [NEW]
  [12] Overdue Tasks             [NEW]
  [0] Exit

Enter your choice:
```

---

*This specification adds advanced scheduling and analytics features to the Phase I Todo App while maintaining the in-memory, console-based constraints.*
