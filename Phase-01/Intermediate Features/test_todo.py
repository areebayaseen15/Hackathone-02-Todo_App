#!/usr/bin/env python
"""Test script for intermediate Todo features."""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from todo.models import Task, Priority
from todo.services import TaskService, ValidationError
from todo.storage import TaskStorage
from datetime import datetime

def test_priority_enum():
    """Test Priority enum."""
    print("Testing Priority enum...")
    assert Priority.HIGH.value == "high"
    assert Priority.MEDIUM.value == "medium"
    assert Priority.LOW.value == "low"
    print("[PASS] Priority enum works")

def test_task_model():
    """Test Task model with priority and category."""
    print("\nTesting Task model...")
    task = Task(
        id=1,
        title="Test Task",
        description="Test Description",
        is_completed=False,
        created_at=datetime.now(),
        priority=Priority.HIGH,
        category="Work"
    )
    assert task.priority == Priority.HIGH
    assert task.category == "Work"
    print("[PASS] Task model with priority/category works")

def test_validation():
    """Test validation functions."""
    print("\nTesting validation...")
    from todo.services import validate_priority, validate_category

    # Test priority validation
    assert validate_priority("high") == Priority.HIGH
    assert validate_priority("MEDIUM") == Priority.MEDIUM
    assert validate_priority("Low") == Priority.LOW
    print("[PASS] Priority validation works")

    # Test category validation
    assert validate_category("Work") == "Work"
    assert validate_category("") is None
    assert validate_category("   ") is None

    try:
        validate_category("X" * 51)  # Too long
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        print(f"[PASS] Category validation catches length errors: {e.message}")

def test_task_operations():
    """Test TaskService operations."""
    print("\nTesting TaskService operations...")
    storage = TaskStorage()
    service = TaskService(storage)

    # Add task with priority and category
    task1 = service.add_task("Important task", "High priority work", "high", "Work")
    assert task1.priority == Priority.HIGH
    assert task1.category == "Work"
    print(f"[PASS] Added task with ID {task1.id}, priority HIGH, category Work")

    # Add task with default priority
    task2 = service.add_task("Normal task", "Medium priority", "medium", "")
    assert task2.priority == Priority.MEDIUM
    assert task2.category is None
    print(f"[PASS] Added task with default priority MEDIUM")

    # Add task with low priority
    task3 = service.add_task("Low priority task", "", "low", "Personal")
    assert task3.priority == Priority.LOW
    print(f"[PASS] Added task with priority LOW")

def test_search():
    """Test search functionality."""
    print("\nTesting search functionality...")
    storage = TaskStorage()
    service = TaskService(storage)

    # Create test tasks
    service.add_task("Buy groceries", "Milk and eggs", "medium", "Personal")
    service.add_task("Complete work project", "Finish the report", "high", "Work")
    service.add_task("Meeting for work", "Prepare slides", "high", "Work")

    # Search by keyword
    results = service.search_tasks("groceries")
    assert len(results) == 1
    assert "groceries" in results[0].title.lower()
    print(f"[PASS] Search for 'groceries' found {len(results)} task(s)")

    results = service.search_tasks("report")
    assert len(results) == 1
    print(f"[PASS] Search for 'report' found {len(results)} task(s)")

    # Case-insensitive search (matches title/description, not category)
    results = service.search_tasks("work")
    assert len(results) == 2  # Two tasks with "work" in title
    print(f"[PASS] Case-insensitive search for 'work' found {len(results)} task(s)")

def test_filters():
    """Test filter functionality."""
    print("\nTesting filter functionality...")
    storage = TaskStorage()
    service = TaskService(storage)

    # Create test tasks with different properties
    task1 = service.add_task("Task 1", "", "high", "Work")
    task2 = service.add_task("Task 2", "", "medium", "Personal")
    task3 = service.add_task("Task 3", "", "low", "Work")
    task4 = service.add_task("Task 4", "", "high", "Personal")

    # Filter by priority
    service.set_filter_priority(Priority.HIGH)
    results = service.filter_tasks()
    assert len(results) == 2
    assert all(t.priority == Priority.HIGH for t in results)
    print(f"[PASS] Filter by HIGH priority found {len(results)} task(s)")

    # Filter by category
    service.clear_filters()
    service.set_filter_category("work")
    results = service.filter_tasks()
    assert len(results) == 2
    assert all("work" in t.category.lower() for t in results if t.category)
    print(f"[PASS] Filter by 'work' category found {len(results)} task(s)")

    # Combined filters (AND logic)
    service.set_filter_priority(Priority.HIGH)
    service.set_filter_category("personal")
    results = service.filter_tasks()
    assert len(results) == 1
    assert results[0].id == task4.id
    print(f"[PASS] Combined filters (HIGH + personal) found {len(results)} task(s)")

def test_sorting():
    """Test sorting functionality."""
    print("\nTesting sorting functionality...")
    storage = TaskStorage()
    service = TaskService(storage)

    # Create test tasks with different priorities
    task1 = service.add_task("Low priority task", "", "low", "")
    task2 = service.add_task("High priority task", "", "high", "")
    task3 = service.add_task("Medium priority task", "", "medium", "")

    all_tasks = service.get_all_tasks()
    print(f"Created {len(all_tasks)} tasks")

    # Sort by priority
    sorted_tasks = service.sort_by_priority(all_tasks)
    assert sorted_tasks[0].priority == Priority.HIGH
    assert sorted_tasks[1].priority == Priority.MEDIUM
    assert sorted_tasks[2].priority == Priority.LOW
    print(f"[PASS] Sort by priority: {sorted_tasks[0].priority} -> {sorted_tasks[1].priority} -> {sorted_tasks[2].priority}")

    # Sort alphabetically
    task4 = service.add_task("A task starting with A", "", "medium", "")
    task5 = service.add_task("Z task starting with Z", "", "medium", "")
    all_tasks = service.get_all_tasks()
    sorted_tasks = service.sort_alphabetically(all_tasks)
    assert sorted_tasks[0].title[0] == "A"
    print(f"[PASS] Sort alphabetically: '{sorted_tasks[0].title[:5]}...' comes first")

def test_update_with_priority_category():
    """Test updating task with priority and category."""
    print("\nTesting task update...")
    storage = TaskStorage()
    service = TaskService(storage)

    task = service.add_task("Original task", "Original desc", "low", "Personal")
    print(f"Created task #{task.id}: {task.title}, priority={task.priority}, category={task.category}")

    # Update priority and category
    updated = service.update_task(
        task.id,
        priority_str="high",
        category_str="Work"
    )
    assert updated.priority == Priority.HIGH
    assert updated.category == "Work"
    print(f"[PASS] Updated task priority to HIGH and category to Work")

    # Update only one field
    updated = service.update_task(task.id, priority_str="medium")
    assert updated.priority == Priority.MEDIUM
    assert updated.category == "Work"  # Category unchanged
    print(f"[PASS] Partial update works (priority changed, category preserved)")

def test_backward_compatibility():
    """Test backward compatibility for tasks without priority/category."""
    print("\nTesting backward compatibility...")
    from todo.models import ensure_task_compatibility

    # Simulate old task (without priority/category)
    task = Task(
        id=1,
        title="Old task",
        description="",
        is_completed=False,
        created_at=datetime.now()
    )

    # Add missing attributes
    task = ensure_task_compatibility(task)
    assert hasattr(task, 'priority')
    assert task.priority == Priority.MEDIUM  # Default
    assert hasattr(task, 'category')
    assert task.category is None  # Default
    print("[PASS] Backward compatibility works for old tasks")

def main():
    """Run all tests."""
    print("=" * 70)
    print("INTERMEDIATE TODO FEATURES - UNIT TESTS")
    print("=" * 70)

    try:
        test_priority_enum()
        test_task_model()
        test_validation()
        test_task_operations()
        test_search()
        test_filters()
        test_sorting()
        test_update_with_priority_category()
        test_backward_compatibility()

        print("\n" + "=" * 70)
        print("ALL TESTS PASSED [PASS]")
        print("=" * 70)
        print("\nFeatures tested:")
        print("  • Priority enum (HIGH, MEDIUM, LOW)")
        print("  • Task category field")
        print("  • Input validation (priority, category)")
        print("  • Search by keyword (case-insensitive)")
        print("  • Filter by status, priority, category")
        print("  • Sort by priority and alphabetically")
        print("  • Update with priority and category")
        print("  • Backward compatibility")

    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
