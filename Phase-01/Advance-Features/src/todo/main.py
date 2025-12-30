"""Application entry point for the Todo application."""

from todo.cli import CLI
from todo.services import TaskService
from todo.storage import TaskStorage


def main() -> None:
    """Initialize and run the Todo application."""
    # Initialize storage (in-memory)
    storage = TaskStorage()

    # Initialize service layer with storage
    service = TaskService(storage)

    # Initialize CLI with service
    cli = CLI(service)

    # Run the application
    cli.run()


if __name__ == "__main__":
    main()
