---
id: 001
title: intermediate-todo-features
stage: spec
date: 2025-12-29T12:00:00Z
surface: cli
model: claude-sonnet-4-5
feature: intermediate-features
branch: 1-intermediate-features
user: N/A
command: sp.specify
labels: [spec, feature]
links:
  spec: specs/1-intermediate-features/spec.md
  ticket:
  adr:
  pr:
files:
  - specs/1-intermediate-features/spec.md
  - specs/1-intermediate-features/checklists/requirements.md
tests:
summary:
---

## Prompt

The Todo App needs intermediate features added:

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
- Assumptions

## Response snapshot

Created a comprehensive specification for intermediate Todo App features including:

1. **Task Priorities** - Users can assign high/medium/low priority levels (defaults to medium)
2. **Categories/Tags** - Optional category field up to 50 characters
3. **Search** - Keyword search in title and description (case-insensitive)
4. **Filters** - Filter by status, priority, or category (multiple filters use AND logic)
5. **Sorting** - Sort by priority (high→medium→low) or alphabetically by title

The specification includes:
- 5 prioritized user stories (P1-P5)
- Detailed acceptance scenarios for each feature
- Comprehensive edge case handling
- 21 functional requirements
- 7 measurable success criteria
- Updated task data structure table
- Complete console input/output examples
- Assumptions about defaults, limits, and behavior

Quality validation checklist passed all items - specification is ready for `/sp.clarify` or `/sp.plan`.

## Outcome

- ✅ Impact: Created complete specification for intermediate features that adds priority, category, search, filter, and sort capabilities to the Phase I Todo App
- 🧪 Tests: Specification includes acceptance scenarios for all 5 features
- 📁 Files: Created spec.md and requirements.md checklist
- 🔁 Next prompts: Ready for /sp.clarify or /sp.plan
- 🧠 Reflection: Specification maintains Phase I constraints (in-memory, console-only) while adding significant organizational capabilities

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All quality checklist items PASSED
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
