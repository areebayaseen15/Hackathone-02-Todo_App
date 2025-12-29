"""Business logic and validation for task operations."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from todo.models import Task, Priority, ensure_task_compatibility
from todo.storage import TaskStorage


class ValidationError(Exception):
    """Raised when input validation fails."""

    def __init__(self, message: str) -> None:
        """Initialize with error message.

        Args:
            message: Human-readable error description.
        """
        self.message = message
        super().__init__(self.message)


def validate_title(title: str) -> str:
    """Validate and clean task title.

    Args:
        title: The title to validate.

    Returns:
        Cleaned (trimmed) title.

    Raises:
        ValidationError: If title is empty or exceeds 100 characters.
    """
    cleaned = title.strip()
    if not cleaned:
        raise ValidationError("Title cannot be empty")
    if len(cleaned) > 100:
        raise ValidationError("Title must be 100 characters or less")
    return cleaned


def validate_description(description: str) -> str:
    """Validate and clean task description.

    Args:
        description: The description to validate.

    Returns:
        Cleaned (trimmed) description.

    Raises:
        ValidationError: If description exceeds 500 characters.
    """
    cleaned = description.strip()
    if len(cleaned) > 500:
        raise ValidationError("Description must be 500 characters or less")
    return cleaned


def validate_priority(priority_str: str) -> Priority:
    """Parse case-insensitive priority string to Priority enum.

    Args:
        priority_str: User-provided priority string

    Returns:
        Priority enum value

    Raises:
        ValidationError: If string doesn't match any priority value
    """
    cleaned = priority_str.strip().casefold()
    for priority in Priority:
        if priority.value == cleaned:
            return priority
    valid_values = ', '.join([p.value for p in Priority])
    raise ValidationError(
        f"Invalid priority '{priority_str}'. Must be one of: {valid_values}"
    )


def validate_category(category_str: str) -> Optional[str]:
    """Validate and clean category string.

    Args:
        category_str: User-provided category string

    Returns:
        Cleaned category string or None if empty

    Raises:
        ValidationError: If category exceeds 50 characters
    """
    cleaned = category_str.strip()

    if not cleaned:
        return None

    if len(cleaned) > 50:
        raise ValidationError(
            f"Category must be 50 characters or less. "
            f"Got {len(cleaned)} characters."
        )

    return cleaned


@dataclass
class FilterState:
    """Tracks active filter criteria for task list.

    Attributes:
        status: None=All, True=Completed, False=Pending
        priority: Priority value if filtering by priority
        category: Category string if filtering by category
    """
    status: Optional[bool] = None
    priority: Optional[Priority] = None
    category: Optional[str] = None

    def is_active(self) -> bool:
        """Check if any filters are currently active.

        Returns:
            True if at least one filter is active, False otherwise.
        """
        return any([
            self.status is not None,
            self.priority is not None,
            self.category is not None
        ])

    def clear(self) -> None:
        """Clear all active filters."""
        self.status = None
        self.priority = None
        self.category = None

    def display(self) -> str:
        """Get display string for active filters.

        Returns:
            String showing active filters or "None".
        """
        parts = []
        if self.status is not None:
            status_str = "completed" if self.status else "pending"
            parts.append(f"status={status_str}")
        if self.priority is not None:
            parts.append(f"priority={self.priority.value}")
        if self.category is not None:
            parts.append(f"category={self.category}")
        return ", ".join(parts) if parts else "None"


class TaskService:
    """Provides business logic for task operations.

    Handles validation, task creation, search, filtering, sorting,
    and coordinates with storage.
    """

    # Priority order for sorting (HIGH=3, MEDIUM=2, LOW=1)
    PRIORITY_ORDER = {
        Priority.HIGH: 3,
        Priority.MEDIUM: 2,
        Priority.LOW: 1
    }

    def __init__(self, storage: TaskStorage) -> None:
        """Initialize service with storage dependency and filter state.

        Args:
            storage: The TaskStorage instance to use.
        """
        self._storage = storage
        self._filters = FilterState()

    def has_tasks(self) -> bool:
        """Check if any tasks exist.

        Returns:
            True if at least one task exists, False otherwise.
        """
        return not self._storage.is_empty()

    def get_task_count(self) -> int:
        """Get total number of tasks.

        Returns:
            The number of tasks in storage.
        """
        return self._storage.count()

    def add_task(
        self,
        title: str,
        description: str = "",
        priority_str: str = "medium",
        category_str: str = ""
    ) -> Task:
        """Add a new task with priority and optional category.

        Args:
            title: The task title (1-100 characters, required).
            description: The task description (0-500 characters, optional).
            priority_str: Priority string (high/medium/low, default: "medium").
            category_str: Category string (0-50 characters, optional).

        Returns:
            The created task with auto-generated ID and timestamp.

        Raises:
            ValidationError: If validation fails for any field.
        """
        clean_title = validate_title(title)
        clean_description = validate_description(description)
        clean_priority = validate_priority(priority_str)
        clean_category = validate_category(category_str)

        task = Task(
            id=0,  # Will be assigned by storage
            title=clean_title,
            description=clean_description,
            is_completed=False,
            created_at=datetime.now(),
            priority=clean_priority,
            category=clean_category
        )

        return self._storage.add(task)

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks ordered by ID.

        Returns:
            List of all tasks in creation order.
        """
        tasks = self._storage.get_all()
        # Ensure backward compatibility for existing tasks
        for task in tasks:
            ensure_task_compatibility(task)
        return sorted(tasks, key=lambda t: t.id)

    def get_task(self, task_id: int) -> Task | None:
        """Get a task by ID.

        Args:
            task_id: The ID of task to retrieve.

        Returns:
            The task if found, None otherwise.
        """
        task = self._storage.get_by_id(task_id)
        if task:
            ensure_task_compatibility(task)
        return task

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        priority_str: str | None = None,
        category_str: str | None = None
    ) -> Task | None:
        """Update task title, description, priority, and/or category.

        Args:
            task_id: The ID of task to update.
            title: New title (None to keep current).
            description: New description (None to keep current).
            priority_str: New priority string (None to keep current).
            category_str: New category string (None to keep current).

        Returns:
            The updated task, or None if task not found.

        Raises:
            ValidationError: If new field validation fails.
        """
        task = self._storage.get_by_id(task_id)
        if task is None:
            return None

        # Ensure task has all fields (backward compatibility)
        ensure_task_compatibility(task)

        if title is not None:
            task.title = validate_title(title)

        if description is not None:
            task.description = validate_description(description)

        if priority_str is not None:
            task.priority = validate_priority(priority_str)

        if category_str is not None:
            task.category = validate_category(category_str)

        self._storage.update(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The ID of task to delete.

        Returns:
            True if task was deleted, False if not found.
        """
        return self._storage.delete(task_id)

    def toggle_task(self, task_id: int) -> Task | None:
        """Toggle task completion status.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            The updated task, or None if task not found.
        """
        task = self._storage.get_by_id(task_id)
        if task is None:
            return None

        ensure_task_compatibility(task)
        task.is_completed = not task.is_completed
        self._storage.update(task)
        return task

    def search_tasks(self, keyword: str) -> list[Task]:
        """Search tasks by keyword in title or description.

        Args:
            keyword: Search keyword (non-empty, case-insensitive)

        Returns:
            List of tasks matching keyword in title or description

        Raises:
            ValidationError: If keyword is empty after trim
        """
        cleaned = keyword.strip()
        if not cleaned:
            raise ValidationError("Keyword cannot be empty")

        keyword_lower = cleaned.casefold()

        results = []
        for task in self.get_all_tasks():
            ensure_task_compatibility(task)
            if (keyword_lower in task.title.casefold() or
                    keyword_lower in task.description.casefold()):
                results.append(task)

        return results

    def filter_tasks(self) -> list[Task]:
        """Filter tasks using active filter criteria (AND logic).

        Returns:
            List of tasks matching all active filters.
        """
        tasks = self.get_all_tasks()
        filtered = list(tasks)

        # Filter by status
        if self._filters.status is not None:
            filtered = [t for t in filtered if t.is_completed == self._filters.status]

        # Filter by priority
        if self._filters.priority is not None:
            filtered = [t for t in filtered if t.priority == self._filters.priority]

        # Filter by category (case-insensitive)
        if self._filters.category is not None:
            category_lower = self._filters.category.casefold()
            filtered = [
                t for t in filtered
                if t.category and category_lower in t.category.casefold()
            ]

        return filtered

    def set_filter_status(self, status: str) -> None:
        """Set status filter.

        Args:
            status: "pending", "completed", or "all" to clear
        """
        status_lower = status.strip().casefold()
        if status_lower == "all":
            self._filters.status = None
        elif status_lower == "pending":
            self._filters.status = False
        elif status_lower == "completed":
            self._filters.status = True

    def set_filter_priority(self, priority: Priority) -> None:
        """Set priority filter.

        Args:
            priority: Priority value to filter by
        """
        self._filters.priority = priority

    def set_filter_category(self, category: str) -> None:
        """Set category filter.

        Args:
            category: Category string to filter by
        """
        cleaned = category.strip()
        self._filters.category = cleaned if cleaned else None

    def clear_filters(self) -> None:
        """Clear all active filters."""
        self._filters.clear()

    def get_active_filters(self) -> FilterState:
        """Get current active filter state.

        Returns:
            The FilterState object with current filter criteria.
        """
        return self._filters

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority (HIGH → MEDIUM → LOW), secondary by created_at.

        Args:
            tasks: List of tasks to sort

        Returns:
            Sorted list of tasks
        """
        return sorted(
            tasks,
            key=lambda t: (
                self.PRIORITY_ORDER[t.priority],  # Primary: priority value
                t.created_at                        # Secondary: newest first
            ),
            reverse=True  # Descending
        )

    def sort_alphabetically(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks alphabetically by title, secondary by created_at.

        Args:
            tasks: List of tasks to sort

        Returns:
            Sorted list of tasks
        """
        return sorted(
            tasks,
            key=lambda t: (
                t.title.casefold(),  # Primary: A-Z
                t.created_at         # Secondary: newest first
            )
        )
