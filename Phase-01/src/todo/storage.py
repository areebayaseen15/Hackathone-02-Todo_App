"""In-memory storage manager for tasks."""

from todo.models import Task


class TaskStorage:
    """Manages in-memory storage of tasks.

    Provides CRUD operations and utility methods for task management.
    Tasks are stored in a list and IDs are generated sequentially.
    """

    def __init__(self) -> None:
        """Initialize empty storage with ID counter starting at 1."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """Generate next unique ID.

        Returns:
            The next sequential ID (never reused within a session).
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add(self, task: Task) -> Task:
        """Add a task to storage.

        Args:
            task: The task to add (ID will be assigned by storage).

        Returns:
            The task with assigned ID.
        """
        task.id = self._generate_id()
        self._tasks.append(task)
        return task

    def get_all(self) -> list[Task]:
        """Get all tasks from storage.

        Returns:
            List of all tasks, ordered by ID (creation order).
        """
        return list(self._tasks)

    def get_by_id(self, task_id: int) -> Task | None:
        """Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The task if found, None otherwise.
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update(self, task: Task) -> bool:
        """Update an existing task in storage.

        Args:
            task: The task with updated values (must have valid ID).

        Returns:
            True if task was found and updated, False otherwise.
        """
        for i, existing_task in enumerate(self._tasks):
            if existing_task.id == task.id:
                self._tasks[i] = task
                return True
        return False

    def delete(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if task was found and deleted, False otherwise.
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                self._tasks.pop(i)
                return True
        return False

    def count(self) -> int:
        """Get the total number of tasks.

        Returns:
            The number of tasks in storage.
        """
        return len(self._tasks)

    def is_empty(self) -> bool:
        """Check if storage is empty.

        Returns:
            True if no tasks exist, False otherwise.
        """
        return len(self._tasks) == 0
