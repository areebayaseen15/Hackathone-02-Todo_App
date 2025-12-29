"""Task data model for Todo application."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class Priority(Enum):
    """Priority levels for tasks.

    Values are ordered from highest to lowest urgency.
    """
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    def __str__(self) -> str:
        """Return uppercase priority for display."""
        return self.value.upper()


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier for task (auto-generated, positive integer)
        title: Short descriptive name of task (1-100 characters, required)
        description: Detailed description of task (0-500 characters, optional)
        is_completed: Completion status of task (default: False)
        created_at: Timestamp when task was created (auto-generated, immutable)
        priority: Priority level of task (HIGH/MEDIUM/LOW, default: MEDIUM)
        category: Optional category or tag for grouping (0-50 characters, optional)
    """

    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    priority: Priority = Priority.MEDIUM
    category: Optional[str] = None


def ensure_task_compatibility(task: Task) -> Task:
    """Ensure task has all required attributes for backward compatibility.

    For tasks created before intermediate features, assign default values.

    Args:
        task: The task to check/update

    Returns:
        The task with all required attributes
    """
    if not hasattr(task, 'priority'):
        task.priority = Priority.MEDIUM
    if not hasattr(task, 'category'):
        task.category = None
    return task
