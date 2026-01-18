"""
Command parsing and execution utilities for the todo CLI.
"""

import re
from typing import List, Union
from ..services.todo_service import TodoService
from ..models.todo import Todo


class TodoCLI:
    """
    Command-line interface for the todo application.
    """

    def __init__(self, service: TodoService):
        self.service = service

    def handle_add(self, args: str) -> str:
        """
        Handle the 'add' command to add a new todo.

        Args:
            args (str): The todo description

        Returns:
            str: Success or error message
        """
        # Extract the todo description from the arguments
        if not args or args.strip() == "":
            return "Error: Please provide a description for the todo."

        # Remove leading/trailing quotes if present
        description = args.strip()
        if ((description.startswith('"') and description.endswith('"')) or \
           (description.startswith("'") and description.endswith("'"))):
            description = description[1:-1]

        try:
            todo = self.service.add_todo(description)
            return f"Todo added with ID: {todo.id}"
        except ValueError as e:
            return f"Error: {e}"

    def handle_view(self, args: str) -> str:
        """
        Handle the 'view' command to display all todos.

        Args:
            args (str): Additional arguments (currently unused)

        Returns:
            str: Formatted list of todos or message if no todos exist
        """
        todos = self.service.get_all_todos()

        if not todos:
            return "No todos found."

        # Create a formatted table
        result = "ID  | Title           | Status\n"
        result += "----|-----------------|--------\n"
        for todo in todos:
            status = "Complete" if todo.completed else "Pending"
            # Truncate long titles for display
            title = todo.title[:15] + "..." if len(todo.title) > 15 else todo.title
            result += f"{todo.id:<3} | {title:<15} | {status}\n"

        return result.rstrip()

    def handle_update(self, args: str) -> str:
        """
        Handle the 'update' command to update a todo.

        Args:
            args (str): Arguments in the format '<id> "new description"'

        Returns:
            str: Success or error message
        """
        # Parse the arguments to extract ID and new description
        if not args:
            return "Error: Please provide an ID and new description. Usage: update <id> \"new description\""

        # Use regex to match ID followed by a quoted description
        match = re.match(r'^(\d+)\s+(.*)', args.strip())
        if not match:
            return "Error: Invalid format. Usage: update <id> \"new description\""

        try:
            id_str, desc_part = match.groups()
            todo_id = int(id_str)

            # Extract the description from quotes if present
            description_match = re.search(r'"([^"]*)"', desc_part) or re.search(r"'([^']*)'", desc_part)
            if description_match:
                new_description = description_match.group(1)
            else:
                new_description = desc_part.strip()

            if not new_description:
                return "Error: New description cannot be empty."

            # Attempt to update the todo
            updated_todo = self.service.update_todo(todo_id, title=new_description)
            if updated_todo:
                return f"Todo {todo_id} updated successfully."
            else:
                return f"Error: Todo with ID {todo_id} not found."
        except ValueError:
            return "Error: Invalid ID. Please provide a numeric ID."
        except Exception as e:
            return f"Error: {e}"

    def handle_delete(self, args: str) -> str:
        """
        Handle the 'delete' command to delete a todo.

        Args:
            args (str): The ID of the todo to delete

        Returns:
            str: Success or error message
        """
        if not args:
            return "Error: Please provide an ID. Usage: delete <id>"

        try:
            todo_id = int(args.strip())
            deleted = self.service.delete_todo(todo_id)
            if deleted:
                return f"Todo {todo_id} deleted successfully."
            else:
                return f"Error: Todo with ID {todo_id} not found."
        except ValueError:
            return "Error: Invalid ID. Please provide a numeric ID."
        except Exception as e:
            return f"Error: {e}"

    def handle_complete(self, args: str) -> str:
        """
        Handle the 'complete' command to mark a todo as complete.

        Args:
            args (str): The ID of the todo to mark as complete

        Returns:
            str: Success or error message
        """
        if not args:
            return "Error: Please provide an ID. Usage: complete <id>"

        try:
            todo_id = int(args.strip())
            todo = self.service.mark_complete(todo_id)
            if todo:
                return f"Todo {todo_id} marked as complete."
            else:
                return f"Error: Todo with ID {todo_id} not found."
        except ValueError:
            return "Error: Invalid ID. Please provide a numeric ID."
        except Exception as e:
            return f"Error: {e}"

    def handle_incomplete(self, args: str) -> str:
        """
        Handle the 'incomplete' command to mark a todo as incomplete.

        Args:
            args (str): The ID of the todo to mark as incomplete

        Returns:
            str: Success or error message
        """
        if not args:
            return "Error: Please provide an ID. Usage: incomplete <id>"

        try:
            todo_id = int(args.strip())
            todo = self.service.mark_incomplete(todo_id)
            if todo:
                return f"Todo {todo_id} marked as incomplete."
            else:
                return f"Error: Todo with ID {todo_id} not found."
        except ValueError:
            return "Error: Invalid ID. Please provide a numeric ID."
        except Exception as e:
            return f"Error: {e}"