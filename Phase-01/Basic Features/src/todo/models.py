"""Task data model for the Todo application."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier for the task (auto-generated, positive integer)
        title: Short descriptive name of the task (1-100 characters)
        description: Detailed description of the task (0-500 characters)
        is_completed: Completion status of the task (default: False)
        created_at: Timestamp when task was created (auto-generated, immutable)
    """

    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
