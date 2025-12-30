---
id: 002
title: intermediate-features-plan
stage: plan
date: 2025-12-29T12:30:00Z
surface: cli
model: claude-sonnet-4-5
feature: intermediate-features
branch: 1-intermediate-features
user: N/A
command: sp.plan
labels: [plan, design, architecture]
links:
  spec: specs/1-intermediate-features/spec.md
  plan: specs/1-intermediate-features/plan.md
  ticket:
  adr:
  pr:
files:
  - specs/1-intermediate-features/plan.md
  - specs/1-intermediate-features/research.md
  - specs/1-intermediate-features/data-model.md
  - specs/1-intermediate-features/quickstart.md
  - specs/1-intermediate-features/contracts/add-task.md
  - specs/1-intermediate-features/contracts/search-tasks.md
  - specs/1-intermediate-features/contracts/filter-tasks.md
  - specs/1-intermediate-features/contracts/sort-tasks.md
  - CLAUDE.md (updated)
summary: Created complete implementation plan with research, data model, and CLI contracts
---

## Prompt

Based on the approved specification, outline a high-level plan to add the intermediate features to the existing console-based Todo App.

Include:

Implementation phases

Order of changes (data → logic → output)

Risks or constraints

Keep it concise and do not write code.

## Response snapshot

Created comprehensive implementation plan for intermediate Todo features:

### Plan Document (`specs/1-intermediate-features/plan.md`)

**Summary**: Plan adds priorities (high/medium/low), categories, search, filters, and sorting to Phase I Todo App while maintaining in-memory, console-only constraints.

**Constitution Check**: ✅ PASSED - All articles verified compliant

**Implementation Phases**:
- Phase 1A: Data Model Foundation (Priority enum, Task fields)
- Phase 1B: Service Logic (validation, search, filter, sort)
- Phase 1C: Storage Layer (wrapper methods)
- Phase 1D: CLI Presentation (menus, screens, table formatting)
- Phase 1E: Error Handling (validation errors, user messages)

**Order**: Data → Logic → Output (prevents integration issues)

**Risks**: Display width overflow, complex filter logic, performance with large lists (200+ tasks)

### Research Document (`specs/1-intermediate-features/research.md`)

Researched 5 key technical decisions:
1. **Priority Enum**: Use Python `enum.Enum` (type-safe, no dependencies)
2. **Case-Insensitive Comparison**: Use `str.casefold()` (Unicode support, standard library)
3. **Filter State Management**: Track in services layer (session-scoped, clean separation)
4. **Sort Key Functions**: Use `sorted()` with tuple keys (stable sort, Pythonic)
5. **CLI Display Formatting**: Extend fixed-width table with new columns

### Data Model (`specs/1-intermediate-features/data-model.md`)

**Modified Task Entity**:
- Added `Priority` enum (HIGH, MEDIUM, LOW)
- Added `priority` field (type: Priority, default: MEDIUM)
- Added `category` field (type: Optional[str], default: None, max 50 chars)

**Validation Functions**:
- `validate_priority()` - Case-insensitive parsing to enum
- `validate_category()` - Length validation, whitespace handling

**Backward Compatibility**: Existing tasks get priority=MEDIUM, category=None

### Quickstart Guide (`specs/1-intermediate-features/quickstart.md`)

Step-by-step implementation checklist organized by phase:
- Phase 1A: Data Model (5 tasks)
- Phase 1B: Service Logic (8 tasks)
- Phase 1C: Storage Layer (5 tasks)
- Phase 1D: CLI Presentation (8 tasks)
- Phase 1E: Error Handling (5 tasks)

Includes testing guide with 5 test categories and common issue solutions.

### CLI Contracts (`specs/1-intermediate-features/contracts/`)

Four detailed command specifications:

1. **add-task.md**: Add task with priority and category
   - Input validation for title (1-100), description (0-500), priority (high/medium/low), category (0-50)
   - Default priority: MEDIUM
   - Clear error messages

2. **search-tasks.md**: Search by keyword
   - Searches title and description
   - Case-insensitive matching
   - "No results found" handling

3. **filter-tasks.md**: Filter by status/priority/category
   - AND logic for multiple filters
   - FilterState tracking
   - Clear all filters option

4. **sort-tasks.md**: Sort by priority or alphabetically
   - Priority sort: HIGH → MEDIUM → LOW, secondary by created_at
   - Alphabetical sort: A → Z, secondary by created_at
   - Default order by ID

### Agent Context Update (`CLAUDE.md`)

Added new section "Current Feature: Intermediate Todo Features" with:
- Feature overview and links to spec/plan
- New features list (priorities, categories, search, filters, sorting)
- Implementation resources links (data-model, research, quickstart, contracts)

## Outcome

- ✅ Impact: Created complete technical blueprint for implementing intermediate features with ~285 lines of code changes across 4 files
- 🧪 Tests: Quickstart includes comprehensive testing guide with edge cases
- 📁 Files: 9 new planning artifacts created (plan, research, data-model, quickstart, 4 contracts)
- 🔁 Next prompts: Ready for `/sp.tasks` to generate implementation tasks
- 🧠 Reflection: Plan maintains Phase I constraints (in-memory, standard library) while adding significant organizational capabilities. Implementation order (data→logic→output) minimizes integration risk.

## Evaluation notes (flywheel)

- Failure modes observed: Agent context update script used wrong plan file (used specs/main/plan.md instead of specs/1-intermediate-features/plan.md), manually corrected CLAUDE.md
- Graders run and results (PASS/FAIL): All Constitution checks PASSED
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
