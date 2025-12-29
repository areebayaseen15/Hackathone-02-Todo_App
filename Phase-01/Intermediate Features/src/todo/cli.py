"""Command-line interface for Todo application."""

from todo.models import Task, Priority
from todo.services import TaskService, ValidationError


class CLI:
    """Handles user interaction through command line.

    Provides menu display, input collection, and output formatting.
    Routes user choices to appropriate handler methods.
    """

    # Updated menu with new options (6, 7, 8) and renumbered exit (9)
    MENU_OPTIONS = {
        1: "Add Task",
        2: "View Tasks",
        3: "Update Task",
        4: "Delete Task",
        5: "Mark as Completed",
        6: "Search Tasks",
        7: "Filter Tasks",
        8: "Sort Tasks",
        9: "Exit",
    }

    def __init__(self, service: TaskService) -> None:
        """Initialize CLI with service dependency.

        Args:
            service: The TaskService instance to use.
        """
        self._service = service

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
        """Display main menu options."""
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

    def truncate(self, text: str, max_len: int) -> str:
        """Truncate text to max_len with ellipsis if needed.

        Args:
            text: Text to truncate.
            max_len: Maximum length (including ellipsis).

        Returns:
            Truncated text with "..." if longer than max_len.
        """
        if len(text) <= max_len:
            return text.ljust(max_len)
        return text[:max_len - 3].ljust(max_len - 3) + "..."

    def display_task(self, task: Task) -> None:
        """Display a single task with all details.

        Args:
            task: The task to display.
        """
        status = "[OK]" if task.is_completed else "[pending...]"
        category_display = task.category or "None"
        print(f"  ID:          {task.id}")
        print(f"  Title:       {task.title}")
        print(f"  Description: {task.description or '(none)'}")
        print(f"  Priority:     {task.priority}")  # NEW: Display priority
        print(f"  Category:     {category_display}")  # NEW: Display category
        print(f"  Status:      {status} {'Completed' if task.is_completed else 'Pending'}")
        print(f"  Created:     {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    def display_task_list(self, tasks: list[Task]) -> None:
        """Display all tasks in a formatted table with priority and category.

        Args:
            tasks: List of tasks to display.
        """
        print("=" * 100)
        print("                              YOUR TASKS")
        print("=" * 100)
        # Updated table headers with Priority and Category columns
        print(f"{'ID':<6} | {'Priority':<9} | {'Category':<10} | {'Status':<15} | {'Title':<30} | {'Created'}")
        print("-" * 100)

        for task in tasks:
            status = "[OK]" if task.is_completed else "[pending...]"
            priority_display = f"{task.priority}"  # Uses Priority.__str__
            category_display = self.truncate(task.category or "", 10)
            title_display = self.truncate(task.title, 30)
            created = task.created_at.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{task.id:<6} | {priority_display:<9} | {category_display:<10} | {status:<12} | {title_display:<30} | {created}")

        print("-" * 100)
        completed = sum(1 for t in tasks if t.is_completed)
        pending = len(tasks) - completed
        print(f"Total: {len(tasks)} tasks ({completed} completed, {pending} pending)")
        print("=" * 100)

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
        """Get a valid menu choice from user.

        Returns:
            Integer between 1 and 9 representing user's choice.
        """
        while True:
            try:
                choice = input("Enter your choice (1-9): ").strip()
                num = int(choice)
                if 1 <= num <= 9:
                    return num
                self.display_error("Please enter a number between 1 and 9")
            except ValueError:
                self.display_error("Invalid input. Please enter a number between 1 and 9")

    def get_task_id(self, prompt: str) -> int:
        """Get a valid task ID from user.

        Args:
            prompt: The prompt to display.

        Returns:
            Positive integer representing task ID.
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
        """Get a yes/no confirmation from user.

        Args:
            prompt: The prompt to display.

        Returns:
            True if user confirms (y/Y), False otherwise.
        """
        response = input(prompt).strip().lower()
        return response == "y"

    def get_input(self, prompt: str, allow_empty: bool = False) -> str:
        """Get text input from user.

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
        """Handle Add Task operation with priority and category."""
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

                # NEW: Get priority (default: medium)
                priority_input = input("Enter priority (high/medium/low, default: medium): ").strip()
                priority_str = priority_input if priority_input else "medium"

                # NEW: Get category (optional)
                category_input = input("Enter category (optional, press Enter to skip): ").strip()
                category_str = category_input if category_input else ""

                task = self._service.add_task(title, description, priority_str, category_str)
                self.display_success(f"Task #{task.id} created successfully!")
                print()
                self.display_task(task)
                return
            except ValidationError as e:
                self.display_error(e.message)

    def handle_view(self) -> None:
        """Handle View Tasks operation with active filters/sort."""
        print()

        # Get tasks to display (respecting filters and sort)
        tasks = self._service.filter_tasks()
        filters = self._service.get_active_filters()

        if not tasks:
            # Check if it's because of filters or no tasks exist
            all_tasks = self._service.get_all_tasks()
            if filters.is_active():
                print("  No tasks match current filters")
            elif not all_tasks:
                print("  No tasks found. Add a task to get started!")
            print()
            return

        self.display_task_list(tasks)

    def handle_update(self) -> None:
        """Handle Update Task operation with priority and category."""
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

        # NEW: Get new priority (Enter to keep current)
        print(f"Current priority: {task.priority.value}")
        new_priority_input = input("New priority (press Enter to keep current): ").strip()
        new_priority = new_priority_input if new_priority_input else None

        # NEW: Get new category (Enter to keep current)
        current_category = task.category or "(none)"
        print(f"Current category: {current_category}")
        new_category_input = input("New category (press Enter to keep current): ").strip()
        new_category = new_category_input if new_category_input else None

        try:
            updated_task = self._service.update_task(
                task_id, new_title, new_description, new_priority, new_category
            )
            if updated_task:
                self.display_success(f"Task #{task_id} updated successfully!")
                print()
                self.display_task(updated_task)
        except ValidationError as e:
            self.display_error(e.message)

    def handle_delete(self) -> None:
        """Handle Delete Task operation."""
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
        """Handle Toggle Task Status operation."""
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

    # NEW: Search Tasks handler
    def handle_search(self) -> None:
        """Handle Search Tasks operation by keyword."""
        print()
        print("-" * 40)
        print("           SEARCH TASKS")
        print("-" * 40)
        print()

        # Check if tasks exist
        if not self._service.has_tasks():
            self.display_error("No tasks available to search")
            return

        # Get keyword
        while True:
            keyword = input("Enter keyword to search: ").strip()
            if keyword:
                break
            self.display_error("Keyword cannot be empty")

        try:
            results = self._service.search_tasks(keyword)

            print()
            print("=" * 100)
            if results:
                print(f"Search Results: {len(results)} task{'s' if len(results) != 1 else ''} found")
            else:
                print(f"No tasks found matching '{keyword}'")
            print("=" * 100)

            if results:
                self.display_task_list(results)
                print()

            input("Press Enter to continue...")

        except ValidationError as e:
            self.display_error(e.message)

    # NEW: Filter Tasks handler
    def handle_filter(self) -> None:
        """Handle Filter Tasks operation."""
        print()
        print("-" * 40)
        print("           FILTER TASKS")
        print("-" * 40)
        print()

        if not self._service.has_tasks():
            self.display_error("No tasks available to filter")
            return

        # Filter menu loop
        while True:
            filters = self._service.get_active_filters()

            # Display filter options
            print("\nAvailable filters:")
            print("  [1] By Status (pending/completed)")
            print("  [2] By Priority (high/medium/low)")
            print("  [3] By Category")
            print("  [4] Clear All Filters")
            print("  [5] Back to Main Menu")

            # Display active filters
            if filters.is_active():
                print(f"\nActive filters: {filters.display()}")
            else:
                print("\nActive filters: None")

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == "1":
                # Filter by status
                while True:
                    status_input = input("Enter status to filter (pending/completed, or 'all' to clear): ").strip()
                    status_lower = status_input.casefold()
                    if status_lower in ("pending", "completed", "all"):
                        self._service.set_filter_status(status_input)
                        print(f"\nStatus filter set to: {status_input}")
                        break
                    else:
                        self.display_error("Invalid status. Must be 'pending', 'completed', or 'all'")

            elif choice == "2":
                # Filter by priority
                while True:
                    priority_input = input("Enter priority to filter (high/medium/low, or 'all' to clear): ").strip()
                    if priority_input.casefold() == "all":
                        self._service.set_filter_priority(None)  # Clear priority filter
                        print("\nPriority filter cleared")
                        break
                    else:
                        # Map to Priority enum
                        priority_clean = priority_input.strip().casefold()
                        valid_priorities = ["high", "medium", "low"]
                        if priority_clean in valid_priorities:
                            if priority_clean == "high":
                                priority_enum = Priority.HIGH
                            elif priority_clean == "medium":
                                priority_enum = Priority.MEDIUM
                            else:  # low
                                priority_enum = Priority.LOW

                            self._service.set_filter_priority(priority_enum)
                            print(f"\nPriority filter set to: {priority_input}")
                            break
                        else:
                            self.display_error(f"Invalid priority. Must be one of: {', '.join(valid_priorities)}")

            elif choice == "3":
                # Filter by category
                category_input = input("Enter category to filter (or 'all' to clear): ").strip()
                if category_input.casefold() == "all":
                    self._service.set_filter_category("")  # Clear category filter
                    print("\nCategory filter cleared")
                else:
                    self._service.set_filter_category(category_input)
                    print(f"\nCategory filter set to: {category_input}")

            elif choice == "4":
                # Clear all filters
                self._service.clear_filters()
                print("\nAll filters cleared. Showing all tasks.")

            elif choice == "5":
                # Back to main menu
                break

            # Show current filter results after each action (except back)
            if choice != "5":
                filtered_tasks = self._service.filter_tasks()
                print()
                if filtered_tasks:
                    print(f"Showing {len(filtered_tasks)} task{'s' if len(filtered_tasks) != 1 else ''} with current filters:")
                    self.display_task_list(filtered_tasks)
                else:
                    print("No tasks match current filters")
                input("\nPress Enter to continue...")

    # NEW: Sort Tasks handler
    def handle_sort(self) -> None:
        """Handle Sort Tasks operation."""
        print()
        print("-" * 40)
        print("           SORT TASKS")
        print("-" * 40)
        print()

        if not self._service.has_tasks():
            self.display_error("No tasks to sort")
            return

        # Get tasks (respecting filters)
        tasks = self._service.filter_tasks()

        # Sort menu loop
        while True:
            print("\nAvailable sort options:")
            print("  [1] Sort by Priority (HIGH -> MEDIUM -> LOW)")
            print("  [2] Sort Alphabetically by Title (A -> Z)")
            print("  [3] Default Order (by ID)")
            print("  [4] Back to Main Menu")

            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == "1":
                # Sort by priority
                sorted_tasks = self._service.sort_by_priority(tasks)
                print("\nTasks sorted by priority")
                self.display_task_list(sorted_tasks)
                input("\nPress Enter to continue...")

            elif choice == "2":
                # Sort alphabetically
                sorted_tasks = self._service.sort_alphabetically(tasks)
                print("\nTasks sorted alphabetically (A-Z)")
                self.display_task_list(sorted_tasks)
                input("\nPress Enter to continue...")

            elif choice == "3":
                # Default order
                sorted_tasks = self._service.get_all_tasks()
                print("\nTasks in default order (by ID)")
                self.display_task_list(sorted_tasks)
                input("\nPress Enter to continue...")

            elif choice == "4":
                # Back to main menu
                break

    def handle_exit(self) -> None:
        """Handle Exit operation with confirmation."""
        print()
        print("WARNING: All tasks will be lost when you exit.")
        if self.get_confirmation("Are you sure you want to exit? (y/n): "):
            self.display_goodbye()
            return False  # Signal to exit loop
        else:
            print("\n  Returning to main menu...\n")
            return True  # Continue running

    # =========================================================================
    # Main Loop
    # =========================================================================

    def run(self) -> None:
        """Run the main application loop."""
        self.display_welcome()
        running = True

        while running:
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
            elif choice == 6:  # NEW
                self.handle_search()
            elif choice == 7:  # NEW
                self.handle_filter()
            elif choice == 8:  # NEW
                self.handle_sort()
            elif choice == 9:  # Renumbered from 6
                running = self.handle_exit() is not False
