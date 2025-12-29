"""Business logic and validation for task operations."""

from datetime import datetime

from todo.models import Task
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


class TaskService:
    """Provides business logic for task operations.

    Handles validation, task creation, and coordinates with storage.
    """

    def __init__(self, storage: TaskStorage) -> None:
        """Initialize service with storage dependency.

        Args:
            storage: The TaskStorage instance to use.
        """
        self._storage = storage

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

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task.

        Args:
            title: The task title (1-100 characters, required).
            description: The task description (0-500 characters, optional).

        Returns:
            The created task with auto-generated ID and timestamp.

        Raises:
            ValidationError: If title or description validation fails.
        """
        clean_title = validate_title(title)
        clean_description = validate_description(description)

        task = Task(
            id=0,  # Will be assigned by storage
            title=clean_title,
            description=clean_description,
            is_completed=False,
            created_at=datetime.now(),
        )

        return self._storage.add(task)

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks ordered by ID.

        Returns:
            List of all tasks in creation order.
        """
        tasks = self._storage.get_all()
        return sorted(tasks, key=lambda t: t.id)

    def get_task(self, task_id: int) -> Task | None:
        """Get a task by ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The task if found, None otherwise.
        """
        return self._storage.get_by_id(task_id)

    def update_task(
        self, task_id: int, title: str | None, description: str | None
    ) -> Task | None:
        """Update task title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: New title (None to keep current).
            description: New description (None to keep current).

        Returns:
            The updated task, or None if task not found.

        Raises:
            ValidationError: If new title or description validation fails.
        """
        task = self._storage.get_by_id(task_id)
        if task is None:
            return None

        if title is not None:
            task.title = validate_title(title)

        if description is not None:
            task.description = validate_description(description)

        self._storage.update(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete.

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

        task.is_completed = not task.is_completed
        self._storage.update(task)
        return task
