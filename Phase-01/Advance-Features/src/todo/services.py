"""Business logic and validation for task operations."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from todo.models import Task, Priority, Recurrence, ensure_task_compatibility, format_due_date, is_overdue
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


def validate_due_date(date_str: str) -> Optional[datetime]:
    """Parse and validate due date string.

    Args:
        date_str: User-provided date string in YYYY-MM-DD format

    Returns:
        datetime object with date component, time set to midnight, or None if empty

    Raises:
        ValueError: If format is invalid or date is not a valid calendar date
    """
    cleaned = date_str.strip()

    if not cleaned:
        return None

    # Validate format: YYYY-MM-DD
    if len(cleaned) != 10 or cleaned[4] != '-' or cleaned[7] != '-':
        raise ValueError(
            f"Invalid date format. Use YYYY-MM-DD. Got: '{date_str}'"
        )

    try:
        year = int(cleaned[0:4])
        month = int(cleaned[5:7])
        day = int(cleaned[8:10])

        # Validate ranges
        if month < 1 or month > 12:
            raise ValueError(f"Invalid month: {month}. Must be 01-12.")

        if day < 1 or day > 31:
            raise ValueError(f"Invalid day: {day}. Must be 01-31.")

        # Create datetime to catch invalid calendar dates (e.g., Feb 31)
        due_date = datetime(year, month, day)

        return due_date

    except ValueError as e:
        # Check if it's our custom error or datetime validation
        if "must be" in str(e):
            raise
        raise ValueError(
            f"Invalid date: '{date_str}'. {str(e)}"
        )


def validate_recurrence(recurrence_str: str) -> Recurrence:
    """Parse case-insensitive recurrence string to Recurrence enum.

    Args:
        recurrence_str: User-provided recurrence string

    Returns:
        Recurrence enum value

    Raises:
        ValueError: If string doesn't match any recurrence value
    """
    cleaned = recurrence_str.strip().casefold()
    for recurrence in Recurrence:
        if recurrence.value == cleaned:
            return recurrence
    valid_values = ', '.join([r.value for r in Recurrence])
    raise ValueError(
        f"Invalid recurrence '{recurrence_str}'. Must be one of: {valid_values}"
    )


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
    recurrence, and coordinates with storage.
    """
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
        category_str: str = "",
        due_date_str: str = "",
        recurrence_str: str = "none"
    ) -> Task:
        """Add a new task with priority, category, due date, and recurrence.

        Args:
            title: The task title (1-100 characters, required).
            description: The task description (0-500 characters, optional).
            priority_str: Priority string (high/medium/low, default: "medium").
            category_str: Category string (0-50 characters, optional).
            due_date_str: Due date string in YYYY-MM-DD format (optional).
            recurrence_str: Recurrence string (none/daily/weekly/monthly, default: "none").

        Returns:
            The created task with auto-generated ID and timestamp.

        Raises:
            ValidationError: If validation fails for any field.
        """
        clean_title = validate_title(title)
        clean_description = validate_description(description)
        clean_priority = validate_priority(priority_str)
        clean_category = validate_category(category_str)
        clean_due_date = validate_due_date(due_date_str)  # NEW
        clean_recurrence = validate_recurrence(recurrence_str)  # NEW

        task = Task(
            id=0,  # Will be assigned by storage
            title=clean_title,
            description=clean_description,
            is_completed=False,
            created_at=datetime.now(),
            priority=clean_priority,
            category=clean_category,
            due_date=clean_due_date,  # NEW
            recurrence=clean_recurrence,  # NEW
            parent_task_id=None
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
        category_str: str | None = None,
        due_date_str: str | None = None,
        recurrence_str: str | None = None
    ) -> Task | None:
        """Update task title, description, priority, category, due date, and/or recurrence.

        Args:
            task_id: The ID of task to update.
            title: New title (None to keep current).
            description: New description (None to keep current).
            priority_str: New priority string (None to keep current).
            category_str: New category string (None to keep current).
            due_date_str: New due date string YYYY-MM-DD or empty to clear (None to keep current).
            recurrence_str: New recurrence string (None to keep current).

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

        if due_date_str is not None:
            # Empty string means clear the due date
            if not due_date_str.strip():
                task.due_date = None
            else:
                task.due_date = validate_due_date(due_date_str)

        if recurrence_str is not None:
            task.recurrence = validate_recurrence(recurrence_str)

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

    def toggle_task(self, task_id: int) -> tuple[Task, Optional[Task]]:
        """Toggle task completion status.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            Tuple of (original_task, next_task_or_none).
            next_task is created if task has recurrence and due_date and is being completed.
        """
        task = self._storage.get_by_id(task_id)
        if task is None:
            return None, None

        ensure_task_compatibility(task)
        is_completing = not task.is_completed

        # Check if we need to create next occurrence BEFORE toggling
        next_task = None
        if (is_completing and
            task.recurrence != Recurrence.NONE and
            task.due_date is not None):
            # Calculate next due date using CURRENT due date
            next_due_date = calculate_next_due_date(task.due_date, task.recurrence)

            # Create next occurrence with same attributes
            next_task = Task(
                id=0,  # Will be assigned by storage
                title=task.title,
                description=task.description,
                is_completed=False,
                created_at=datetime.now(),
                priority=task.priority,
                category=task.category,
                due_date=next_due_date,
                recurrence=task.recurrence,
                parent_task_id=task.id
            )
            next_task = self._storage.add(next_task)

        # Toggle completion status AFTER creating next occurrence
        task.is_completed = not task.is_completed
        self._storage.update(task)

        return task, next_task

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
