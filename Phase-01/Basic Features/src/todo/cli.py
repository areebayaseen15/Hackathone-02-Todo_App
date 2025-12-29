"""Command-line interface for the Todo application."""

from todo.models import Task
from todo.services import TaskService, ValidationError


class CLI:
    """Handles user interaction through the command line.

    Provides menu display, input collection, and output formatting.
    Routes user choices to appropriate handler methods.
    """

    MENU_OPTIONS = {
        1: "Add Task",
        2: "View Tasks",
        3: "Update Task",
        4: "Delete Task",
        5: "Toggle Task Status",
        6: "Exit",
    }

    def __init__(self, service: TaskService) -> None:
        """Initialize CLI with service dependency.

        Args:
            service: The TaskService instance to use.
        """
        self._service = service
        self._running = False

    # =========================================================================
    # Display Helpers
    # =========================================================================

    def display_welcome(self) -> None:
        """Display welcome banner on application startup."""
        print("=" * 80)
        print("          WELCOME TO TODO APPLICATION - PHASE I")
        print("          In-Memory Console Version")
        print("=" * 80)
        print()

    def display_goodbye(self) -> None:
        """Display goodbye message on application exit."""
        print()
        print("=" * 80)
        print("Thank you for using Todo Application!")
        print("Goodbye!")
        print("=" * 80)

    def display_menu(self) -> None:
        """Display the main menu options."""
        print()
        print("=" * 80)
        print("                         TODO APPLICATION - PHASE I")
        print("=" * 80)
        print()
        print("Please select an option:")
        print()
        for num, label in self.MENU_OPTIONS.items():
            print(f"  [{num}] {label}")
        print()

    def display_task(self, task: Task) -> None:
        """Display a single task with all details.

        Args:
            task: The task to display.
        """
        status = "[X]" if task.is_completed else "[ ]"
        print(f"  ID:          {task.id}")
        print(f"  Title:       {task.title}")
        print(f"  Description: {task.description or '(none)'}")
        print(f"  Status:      {status} {'Completed' if task.is_completed else 'Pending'}")
        print(f"  Created:     {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    def display_task_list(self, tasks: list[Task]) -> None:
        """Display all tasks in a formatted table.

        Args:
            tasks: List of tasks to display.
        """
        print("=" * 80)
        print("                              YOUR TASKS")
        print("=" * 80)
        print(f"{'ID':<6}| {'Status':<12}| {'Title':<32}| {'Created'}")
        print("-" * 80)

        for task in tasks:
            status = "[X]" if task.is_completed else "[ ]"
            title = task.title[:30] + ".." if len(task.title) > 32 else task.title
            created = task.created_at.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{task.id:<6}| {status:<12}| {title:<32}| {created}")

        print("-" * 80)

        completed = sum(1 for t in tasks if t.is_completed)
        pending = len(tasks) - completed
        print(f"Total: {len(tasks)} tasks ({completed} completed, {pending} pending)")
        print("=" * 80)

    def display_error(self, message: str) -> None:
        """Display an error message.

        Args:
            message: The error message to display.
        """
        print(f"\n  ERROR: {message}\n")

    def display_success(self, message: str) -> None:
        """Display a success message.

        Args:
            message: The success message to display.
        """
        print(f"\n  SUCCESS: {message}\n")

    # =========================================================================
    # Input Helpers
    # =========================================================================

    def get_menu_choice(self) -> int:
        """Get a valid menu choice from the user.

        Returns:
            Integer between 1 and 6 representing the user's choice.
        """
        while True:
            try:
                choice = input("Enter your choice (1-6): ").strip()
                num = int(choice)
                if 1 <= num <= 6:
                    return num
                self.display_error("Please enter a number between 1 and 6")
            except ValueError:
                self.display_error("Invalid input. Please enter a number between 1 and 6")

    def get_task_id(self, prompt: str) -> int:
        """Get a valid task ID from the user.

        Args:
            prompt: The prompt to display.

        Returns:
            Positive integer representing the task ID.
        """
        while True:
            try:
                value = input(prompt).strip()
                num = int(value)
                if num > 0:
                    return num
                self.display_error("Invalid ID. Please enter a positive number")
            except ValueError:
                self.display_error("Invalid ID. Please enter a number")

    def get_confirmation(self, prompt: str) -> bool:
        """Get a yes/no confirmation from the user.

        Args:
            prompt: The prompt to display.

        Returns:
            True if user confirms (y/Y), False otherwise.
        """
        response = input(prompt).strip().lower()
        return response == "y"

    def get_input(self, prompt: str, allow_empty: bool = False) -> str:
        """Get text input from the user.

        Args:
            prompt: The prompt to display.
            allow_empty: Whether to accept empty input.

        Returns:
            The user's input (trimmed).
        """
        while True:
            value = input(prompt).strip()
            if value or allow_empty:
                return value
            self.display_error("Input cannot be empty")

    # =========================================================================
    # Feature Handlers
    # =========================================================================

    def handle_add(self) -> None:
        """Handle the Add Task operation."""
        print()
        print("-" * 40)
        print("           ADD NEW TASK")
        print("-" * 40)
        print()

        # Get title with validation loop
        while True:
            title = input("Enter task title: ").strip()
            try:
                # Get description (optional)
                description = input("Enter description (optional, press Enter to skip): ").strip()

                task = self._service.add_task(title, description)
                self.display_success(f"Task #{task.id} created successfully!")
                print()
                self.display_task(task)
                return
            except ValidationError as e:
                self.display_error(e.message)

    def handle_view(self) -> None:
        """Handle the View Tasks operation."""
        print()
        tasks = self._service.get_all_tasks()

        if not tasks:
            print()
            print("  No tasks found. Add a task to get started!")
            print()
            return

        self.display_task_list(tasks)

    def handle_update(self) -> None:
        """Handle the Update Task operation."""
        print()
        print("-" * 40)
        print("           UPDATE TASK")
        print("-" * 40)
        print()

        if not self._service.has_tasks():
            self.display_error("No tasks available to update")
            return

        task_id = self.get_task_id("Enter task ID to update: ")
        task = self._service.get_task(task_id)

        if task is None:
            self.display_error(f"Task with ID {task_id} not found")
            return

        print()
        print("Current task details:")
        self.display_task(task)
        print()

        # Get new title (Enter to keep current)
        print(f"Current title: {task.title}")
        new_title_input = input("New title (press Enter to keep current): ").strip()
        new_title = new_title_input if new_title_input else None

        # Get new description (Enter to keep current)
        print(f"Current description: {task.description or '(none)'}")
        new_desc_input = input("New description (press Enter to keep current): ").strip()
        new_description = new_desc_input if new_desc_input else None

        try:
            updated_task = self._service.update_task(task_id, new_title, new_description)
            if updated_task:
                self.display_success(f"Task #{task_id} updated successfully!")
                print()
                self.display_task(updated_task)
        except ValidationError as e:
            self.display_error(e.message)

    def handle_delete(self) -> None:
        """Handle the Delete Task operation."""
        print()
        print("-" * 40)
        print("           DELETE TASK")
        print("-" * 40)
        print()

        if not self._service.has_tasks():
            self.display_error("No tasks available to delete")
            return

        task_id = self.get_task_id("Enter task ID to delete: ")
        task = self._service.get_task(task_id)

        if task is None:
            self.display_error(f"Task with ID {task_id} not found")
            return

        print()
        print("Task to be deleted:")
        self.display_task(task)
        print()

        if self.get_confirmation("Are you sure you want to delete this task? (y/n): "):
            if self._service.delete_task(task_id):
                self.display_success(f"Task #{task_id} deleted successfully!")
            else:
                self.display_error("Failed to delete task")
        else:
            print("\n  Deletion cancelled.\n")

    def handle_toggle(self) -> None:
        """Handle the Toggle Task Status operation."""
        print()
        print("-" * 40)
        print("        TOGGLE TASK STATUS")
        print("-" * 40)
        print()

        if not self._service.has_tasks():
            self.display_error("No tasks available")
            return

        task_id = self.get_task_id("Enter task ID to toggle: ")
        task = self._service.toggle_task(task_id)

        if task is None:
            self.display_error(f"Task with ID {task_id} not found")
            return

        status = "complete" if task.is_completed else "incomplete"
        self.display_success(f"Task #{task_id} marked as {status}")

    def handle_exit(self) -> None:
        """Handle the Exit operation with confirmation."""
        print()
        print("WARNING: All tasks will be lost when you exit.")
        if self.get_confirmation("Are you sure you want to exit? (y/n): "):
            self.display_goodbye()
            self._running = False
        else:
            print("\n  Returning to main menu...\n")

    # =========================================================================
    # Main Loop
    # =========================================================================

    def run(self) -> None:
        """Run the main application loop."""
        self._running = True
        self.display_welcome()

        while self._running:
            self.display_menu()
            choice = self.get_menu_choice()

            if choice == 1:
                self.handle_add()
            elif choice == 2:
                self.handle_view()
            elif choice == 3:
                self.handle_update()
            elif choice == 4:
                self.handle_delete()
            elif choice == 5:
                self.handle_toggle()
            elif choice == 6:
                self.handle_exit()
