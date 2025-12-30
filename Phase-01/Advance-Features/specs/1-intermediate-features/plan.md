# Implementation Plan: Intermediate Todo Features

**Branch**: `1-intermediate-features` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-intermediate-features/spec.md`

## Summary

This plan adds intermediate organization features to the Phase I Todo App: task priorities (high/medium/low), optional categories/Tags, keyword search, filtering (by status/priority/category), and sorting (by priority/alphabetically). All changes maintain in-memory storage and console-based interface constraints. Implementation follows existing code structure with layered architecture (models → storage → services → CLI).

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Standard library only (Phase I constraint)
**Storage**: In-memory list (no persistence)
**Testing**: Manual testing via CLI (Phase I constraint)
**Target Platform**: Command-line terminal/console
**Project Type**: Single console application
**Performance Goals**: Task list display within 1 second for lists up to 200 tasks (SC-006)
**Constraints**: In-memory only, no external packages, no file/database operations, no network requests
**Scale/Scope**: Single user, session-bound data, 200+ tasks per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Article | Check | Status | Notes |
|---------|-------|--------|-------|
| Article I: Spec-Driven Development | ✅ PASS | Plan derived from approved specification |
| Article II: Agent Behavior | ✅ PASS | No feature invention, adheres to spec exactly |
| Article III: Phase Governance | ✅ PASS | Maintains Phase I scope (in-memory, console-only) |
| Article IV: Technology Constraints | ✅ PASS | Uses Python 3.13+, UV, no external packages |
| Article V: Quality Principles | ✅ PASS | Maintains layered architecture, separation of concerns |

**Gate Status**: ✅ PASSED - Proceed to Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/1-intermediate-features/
├── spec.md              # Feature specification (already created)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI command specifications)
│   ├── add-task.md
│   ├── search-tasks.md
│   ├── filter-tasks.md
│   └── sort-tasks.md
└── tasks.md             # Phase 2 output (created by /sp.tasks command)
```

### Source Code (repository root)

```text
src/todo/
├── __init__.py      # Package marker
├── __main__.py      # Python -m todo entry
├── main.py          # Application entry point (no changes expected)
├── models.py        # Task dataclass (MODIFY: add priority, category fields)
├── storage.py       # In-memory storage (MODIFY: add search/filter/sort methods)
├── services.py      # Business logic (MODIFY: add validation, operations)
└── cli.py           # CLI interface (MODIFY: add menus, display formatting)
```

**Structure Decision**: Option 1 (Single project) selected. Feature extends existing Phase I structure without reorganization. All modifications are additive to existing modules, preserving clean architecture and separation of concerns.

## Complexity Tracking

> No Constitution violations detected. This section intentionally left blank.

---

## Phase 0: Outline & Research

### Research Scope

No NEEDS CLARIFICATION markers exist in the specification. Research focuses on:

1. **Enum implementation for Priority** - Standard Python `enum.Enum` vs string constants
2. **Case-insensitive comparison patterns** - For priority, search, categories
3. **Filter state management** - How to track active filters across menu navigation
4. **Sort key functions** - Python `sorted()` with multi-level keys
5. **CLI display formatting** - Table formatting with new columns (priority, category)

### Research Findings

#### 1. Priority Enum Implementation
**Decision**: Use Python `enum.Enum` class from standard library

**Rationale**:
- Built-in type safety and validation
- Clear, self-documenting code
- Easy to iterate over all values
- No external dependency (standard library)
- Natural fit for discrete set of valid values

**Alternatives considered**:
- String constants (`HIGH = "high"`) - No type safety, prone to typos
- Integer mapping (`HIGH = 3`) - Less readable, harder to display
- Plain strings - No validation, requires manual checking

#### 2. Case-Insensitive Comparison Pattern
**Decision**: Use `str.lower()` or `str.casefold()` for comparisons

**Rationale**:
- `str.casefold()` handles Unicode edge cases better than `lower()`
- Simple, standard library approach
- Works for priority values, search keywords, categories
- No external dependencies

**Alternatives considered**:
- Regular expressions (`re.IGNORECASE`) - Overkill for simple case matching
- Third-party libraries - Violates Phase I constraint
- User-enforced casing - Poor UX

#### 3. Filter State Management
**Decision**: Track active filters as mutable state in services layer

**Rationale**:
- Filters are session-scoped (in-memory)
- Services layer is appropriate for business logic state
- CLI layer queries services, services apply filters
- Clear separation: CLI handles user input, services handle data logic

**Alternatives considered**:
- CLI layer state - Violates separation of concerns
- Global variables - Poor design, hard to test
- Pass filter criteria per call - More complex API, no benefit

#### 4. Sort Key Functions
**Decision**: Use Python `sorted()` with tuple key and custom function

**Rationale**:
- `sorted()` is stable sort (important for secondary sort)
- Tuple keys allow multi-level sorting: `(primary, secondary)`
- Custom function for priority mapping (HIGH > MEDIUM > LOW)
- `created_at` as secondary key for tie-breaking
- Clean Pythonic approach

**Alternatives considered**:
- In-place `list.sort()` - Modifies storage, less functional
- Custom comparator - Deprecated in Python 3
- Multiple passes - Less efficient

#### 5. CLI Display Formatting
**Decision**: Extend existing table format with new columns

**Rationale**:
- Maintain consistency with existing display
- Use fixed-width formatting with f-strings
- Add Priority column (8 chars), Category column (10 chars)
- Truncate long categories with ellipsis
- Preserve existing "ID", "Status", "Title", "Created" columns

**Alternatives considered**:
- Third-party table libraries - Violates Phase I constraint
- CSV output - Less readable in console
- Separate views per feature - Inconsistent UX

### Phase 0 Output: research.md

(Consolidated findings documented above will be written to `research.md`)

---

## Phase 1: Design & Contracts

### 1. Data Model Updates

#### Modified Task Entity

**File**: `src/todo/models.py`

**Changes**:
- Add `Priority` enum class with values: HIGH, MEDIUM, LOW
- Add `priority` field to `Task` dataclass (type: `Priority`)
- Add `category` field to `Task` dataclass (type: `Optional[str]`, default: `None`)
- Update docstring to document new fields

**Field Details**:
```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    priority: Priority  # NEW: HIGH, MEDIUM, LOW
    category: Optional[str] = None  # NEW: Optional, max 50 chars
```

**Validation Rules**:
- Priority: Must be valid enum value
- Category: Optional, 0-50 characters, None treated as empty

### 2. Service Layer Updates

**File**: `src/todo/services.py`

**New Methods**:
- `validate_priority(priority_str: str) -> Priority` - Parse case-insensitive string to enum
- `validate_category(category_str: str) -> Optional[str]` - Trim, validate length, return None if empty
- `search_tasks(keyword: str, tasks: List[Task]) -> List[Task]` - Filter by keyword in title/description
- `filter_tasks(tasks: List[Task], status: Optional[bool], priority: Optional[Priority], category: Optional[str]) -> List[Task]` - Apply filters with AND logic
- `sort_by_priority(tasks: List[Task]) -> List[Task]` - Sort HIGH → MEDIUM → LOW, secondary by created_at
- `sort_alphabetically(tasks: List[Task]) -> List[Task]` - Sort A-Z by title, secondary by created_at

**Modified Methods**:
- `create_task()` - Add priority and category parameters
- `update_task()` - Add priority and category to updatable fields

### 3. Storage Layer Updates

**File**: `src/todo/storage.py`

**New Methods**:
- `search(keyword: str) -> List[Task]` - Delegate to services.search_tasks
- `filter_by_status(status: bool) -> List[Task]` - Filter by completion status
- `filter_by_priority(priority: Priority) -> List[Task]` - Filter by priority level
- `filter_by_category(category: str) -> List[Task]` - Filter by category
- `sort_by(criteria: str) -> List[Task]` - Sort by specified criteria

**Note**: Storage methods are thin wrappers around services for clean architecture.

### 4. CLI Layer Updates

**File**: `src/todo/cli.py`

**New Menu Options**:
- `[6] Search Tasks` - Search by keyword
- `[7] Filter Tasks` - Apply status/priority/category filters
- `[8] Sort Tasks` - Sort by priority or alphabetically
- `[9] Exit` - Renumbered from `[6]`

**New Screens**:
- `display_search_menu()` - Search input and results display
- `display_filter_menu()` - Filter selection and application
- `display_sort_menu()` - Sort option selection
- `display_filtered_tasks(title: str, tasks: List[Task])` - Show filtered results with header

**Modified Screens**:
- `display_add_task()` - Add prompts for priority and category
- `display_update_task()` - Add prompts for priority and category updates
- `display_tasks()` - Add Priority and Category columns to table
- `display_main_menu()` - Update with new menu options

**Display Format Changes**:

**Enhanced Task List View**:
```
ID    | Priority | Category | Status      | Title                          | Created
--------------------------------------------------------------------------------
1     | HIGH     | work     | [ ]         | Finish report                  | 2025-12-29 11:45:00
2     | MEDIUM   | personal | [X]         | Call dentist                   | 2025-12-29 09:15:00
```

**Column Widths**:
- ID: 5 chars
- Priority: 9 chars
- Category: 10 chars (truncated with ... if longer)
- Status: 12 chars
- Title: 30 chars (truncated with ... if longer)
- Created: 19 chars (YYYY-MM-DD HH:MM:SS)

### 5. Implementation Phases

#### Phase 1A: Data Model Foundation
1. Add `Priority` enum to `models.py`
2. Add `priority` and `category` fields to `Task` dataclass
3. Update model docstrings

#### Phase 1B: Service Logic
1. Add `validate_priority()` function
2. Add `validate_category()` function
3. Add `search_tasks()` function
4. Add `filter_tasks()` function
5. Add `sort_by_priority()` function
6. Add `sort_alphabetically()` function
7. Modify `create_task()` to accept priority/category
8. Modify `update_task()` to update priority/category

#### Phase 1C: Storage Layer
1. Add `search()` wrapper method
2. Add `filter_by_status()` wrapper method
3. Add `filter_by_priority()` wrapper method
4. Add `filter_by_category()` wrapper method
5. Add `sort_by()` wrapper method

#### Phase 1D: CLI Presentation
1. Update `display_main_menu()` with new options
2. Modify `display_add_task()` for priority/category prompts
3. Modify `display_update_task()` for priority/category updates
4. Modify `display_tasks()` table format
5. Add `display_search_menu()` screen
6. Add `display_filter_menu()` screen
7. Add `display_sort_menu()` screen
8. Add `display_filtered_tasks()` screen

#### Phase 1E: Error Handling
1. Add validation errors for invalid priority values
2. Add validation errors for category length > 50
3. Add empty search keyword validation
4. Add "no results found" messages for search/filter
5. Add "no tasks available" for empty task list

### 6. Edge Cases Handling

| Edge Case | Handling |
|-----------|----------|
| Invalid priority value ("urgent") | Display error, prompt again |
| Empty priority input (Enter) | Default to MEDIUM |
| Empty category input (Enter) | Set to None |
| Category > 50 characters | Display error, truncate or reject |
| Empty search keyword | Display error, prompt again |
| No search results | Display "No tasks found matching '{keyword}'" |
| No filtered results | Display "No tasks match current filters" |
| Sort with empty task list | Display "No tasks to sort" |
| Case variations in input | Convert to lowercase for validation |
| Whitespace-only input | Trim and treat as empty |

### 7. Backward Compatibility

**Existing Task Handling**:
- Tasks created before this feature will have `priority=MEDIUM` (default)
- Tasks created before will have `category=None`
- Migration: When app starts with existing tasks, assign defaults

**Approach**:
- Check if task has `priority` attribute during loading
- If missing, assign `Priority.MEDIUM` and `category=None`
- Only applies to in-memory session (no persistence in Phase I)

### 8. Risks and Constraints

#### Risks

1. **Display Width Overflow** - New columns may exceed terminal width on narrow screens
   - **Mitigation**: Use fixed widths, truncate long fields with "..."

2. **Complex Filter Logic** - Multiple filters with AND logic may confuse users
   - **Mitigation**: Clear display of active filters, easy "Clear All" option

3. **Performance with Large Lists** - Sorting/filtering 200+ tasks may be slow
   - **Mitigation**: Python's O(n log n) sort is sufficient for 200 tasks (spec requirement)

4. **Category Name Collisions** - Users may create inconsistent category names
   - **Acceptable**: Phase I scope allows manual entry; no validation/enforcement needed

#### Constraints

1. **Phase I Scope** - Cannot add persistence, web UI, or external libraries
2. **In-Memory Only** - All data lost on exit (existing constraint)
3. **Standard Library** - No external packages allowed
4. **Console-Based** - No UI framework or graphical interface

### 9. Testing Strategy

**Manual Test Scenarios**:

1. **Priority Assignment**
   - Create task with HIGH priority
   - Create task without priority (should default to MEDIUM)
   - Create task with invalid priority (should error)
   - Update task priority from HIGH to LOW

2. **Category Assignment**
   - Create task with category "work"
   - Create task without category (Enter)
   - Create task with 51-char category (should error)
   - Update task category from "work" to "personal"

3. **Search**
   - Search for keyword in title
   - Search for keyword in description
   - Search with no matches
   - Search with empty keyword (should error)
   - Case-insensitive search

4. **Filters**
   - Filter by status (pending/completed)
   - Filter by priority (high/medium/low)
   - Filter by category
   - Combine filters (status + priority)
   - Clear all filters

5. **Sorting**
   - Sort by priority (HIGH → MEDIUM → LOW)
   - Sort alphabetically (A → Z)
   - Sort with empty task list
   - Return to default sort order

6. **Edge Cases**
   - All validation errors tested
   - "No results" messages displayed correctly
   - Task list formatting with long titles/categories

---

## Phase 2: Task Breakup

**Note**: This section will be populated by `/sp.tasks` command, which generates atomic implementation tasks from this plan.

**Expected Task Categories**:
- Data model updates (enum, new fields)
- Service layer functions (validation, search, filter, sort)
- Storage layer wrappers
- CLI menu updates and display formatting
- Error handling improvements
- Testing/validation

---

## Quickstart Guide

**For Developers**:

1. **Modify `src/todo/models.py`**
   - Add `Priority` enum class
   - Update `Task` dataclass with `priority` and `category` fields

2. **Modify `src/todo/services.py`**
   - Add validation functions for priority and category
   - Add search, filter, and sort functions
   - Update `create_task()` and `update_task()` signatures

3. **Modify `src/todo/storage.py`**
   - Add wrapper methods for search/filter/sort operations

4. **Modify `src/todo/cli.py`**
   - Update main menu with new options (6, 7, 8)
   - Add new screens: search, filter, sort
   - Update task display table format
   - Update add/update task prompts

5. **Test Manually**
   - Run `uv run todo`
   - Test all new features
   - Verify edge cases
   - Ensure backward compatibility

---

## Implementation Order (Data → Logic → Output)

```
Phase 1A: Data Model Foundation
  └─> models.py (enum, fields)

Phase 1B: Service Logic
  └─> services.py (validation, search, filter, sort, update/create)

Phase 1C: Storage Layer
  └─> storage.py (wrapper methods)

Phase 1D: CLI Presentation
  └─> cli.py (menus, screens, display formatting)

Phase 1E: Error Handling
  └─> All layers (validation errors, user messages)
```

**Rationale**: This order ensures data structure is defined before logic uses it, logic is ready before presentation displays it, and errors are handled throughout. This minimizes integration issues and allows incremental testing.

---

*This implementation plan adds intermediate features while maintaining Phase I constraints and clean architecture principles.*
