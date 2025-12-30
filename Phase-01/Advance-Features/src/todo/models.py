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


class Recurrence(Enum):
    """Recurrence patterns for tasks.

    Values indicate how often a task repeats.
    """
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    def __str__(self) -> str:
        """Return uppercase recurrence for display."""
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
        due_date: Optional due date or deadline (YYYY-MM-DD format, optional)
        recurrence: Recurrence pattern (NONE/DAILY/WEEKLY/MONTHLY, default: NONE)
        parent_task_id: Optional reference to originating task ID (for recurring chains)
    """

    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    priority: Priority = Priority.MEDIUM
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    recurrence: Recurrence = Recurrence.NONE
    parent_task_id: Optional[int] = None


def format_due_date(due_date: Optional[datetime]) -> str:
    """Format due date for display.

    Args:
        due_date: Due date datetime or None

    Returns:
        Formatted string: "TODAY", "YYYY-MM-DD", or "No due date"
    """
    if due_date is None:
        return "No due date"

    today = datetime.now().date()
    task_date = due_date.date()

    if task_date == today:
        return "TODAY"

    return due_date.strftime("%Y-%m-%d")


def is_overdue(due_date: Optional[datetime]) -> bool:
    """Check if a task is overdue.

    Args:
        due_date: Due date of task (can be None)

    Returns:
        True if overdue, False otherwise
    """
    if due_date is None:
        return False
    today = datetime.now().date()
    return due_date.date() < today


def get_days_overdue(due_date: datetime) -> int:
    """Calculate days overdue for a task.

    Args:
        due_date: Due date of task

    Returns:
        Number of days overdue (positive if overdue, 0 if not overdue)
    """
    today = datetime.now().date()
    task_date = due_date.date()
    delta = today - task_date
    return max(0, delta.days)


def calculate_next_due_date(current_date: datetime, recurrence: 'Recurrence') -> datetime:
    """Calculate next due date based on recurrence pattern.

    Args:
        current_date: Current due date of task
        recurrence: Recurrence pattern

    Returns:
        Next due date

    Raises:
        ValueError: If recurrence is not recognized
    """
    from datetime import timedelta

    if recurrence == Recurrence.NONE:
        raise ValueError("Cannot calculate next date for non-recurring task")

    if recurrence == Recurrence.DAILY:
        return current_date + timedelta(days=1)

    if recurrence == Recurrence.WEEKLY:
        return current_date + timedelta(weeks=1)

    if recurrence == Recurrence.MONTHLY:
        # Handle month-end edge cases (e.g., Jan 31 -> Feb 28/29)
        year = current_date.year
        month = current_date.month + 1

        if month > 12:
            month = 1
            year += 1

        day = current_date.day

        # Get last day of target month
        last_day = (datetime(year, month + 1, 1) - timedelta(days=1)).day

        # Use min(day, last_day) to handle case where day doesn't exist in target month
        return datetime(year, month, min(day, last_day))

    raise ValueError(f"Unknown recurrence pattern: {recurrence}")


def ensure_task_compatibility(task: Task) -> Task:
    """Ensure task has all required attributes for backward compatibility.

    For tasks created before intermediate features, assign default values.

    Args:
        task: The task to check/update

    Returns:
        The task with all required attributes
    """
    # Intermediate phase attributes
    if not hasattr(task, 'priority'):
        task.priority = Priority.MEDIUM
    if not hasattr(task, 'category'):
        task.category = None

    # Advanced phase attributes
    if not hasattr(task, 'due_date'):
        task.due_date = None
    if not hasattr(task, 'recurrence'):
        task.recurrence = Recurrence.NONE
    if not hasattr(task, 'parent_task_id'):
        task.parent_task_id = None

    return task
