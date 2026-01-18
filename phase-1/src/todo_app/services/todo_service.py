"""
Business logic layer for todo operations.
"""

from typing import List, Optional
from ..models.todo import Todo
from ..repositories.todo_repository import TodoRepository


class TodoService:
    """
    Service class for business logic related to todo operations.
    """

    def __init__(self, repository: TodoRepository = None):
        self.repository = repository or TodoRepository()

    def add_todo(self, title: str) -> Todo:
        """
        Add a new todo.

        Args:
            title (str): The title of the todo

        Returns:
            Todo: The created todo object

        Raises:
            ValueError: If the title is empty or contains only whitespace
        """
        if not title or title.strip() == "":
            raise ValueError("Todo title cannot be empty or contain only whitespace")

        return self.repository.add_todo(title)

    def get_todo(self, id: int) -> Optional[Todo]:
        """
        Get a todo by its ID.

        Args:
            id (int): The ID of the todo to retrieve

        Returns:
            Optional[Todo]: The todo if found, None otherwise
        """
        return self.repository.get_todo(id)

    def get_all_todos(self) -> List[Todo]:
        """
        Get all todos.

        Returns:
            List[Todo]: A list of all todos
        """
        return self.repository.get_all_todos()

    def get_completed_todos(self) -> List[Todo]:
        """
        Get all completed todos.

        Returns:
            List[Todo]: A list of completed todos
        """
        return self.repository.get_completed_todos()

    def get_pending_todos(self) -> List[Todo]:
        """
        Get all pending todos.

        Returns:
            List[Todo]: A list of pending todos
        """
        return self.repository.get_pending_todos()

    def update_todo(self, id: int, title: str = None, completed: bool = None) -> Optional[Todo]:
        """
        Update an existing todo.

        Args:
            id (int): The ID of the todo to update
            title (str, optional): New title for the todo
            completed (bool, optional): New completion status for the todo

        Returns:
            Optional[Todo]: The updated todo if found, None otherwise
        """
        # If title is provided, validate it
        if title is not None and (not title or title.strip() == ""):
            raise ValueError("Todo title cannot be empty or contain only whitespace")

        return self.repository.update_todo(id, title, completed)

    def delete_todo(self, id: int) -> bool:
        """
        Delete a todo by its ID.

        Args:
            id (int): The ID of the todo to delete

        Returns:
            bool: True if the todo was deleted, False if not found
        """
        return self.repository.delete_todo(id)

    def mark_complete(self, id: int) -> Optional[Todo]:
        """
        Mark a todo as complete.

        Args:
            id (int): The ID of the todo to mark as complete

        Returns:
            Optional[Todo]: The updated todo if found, None otherwise
        """
        return self.repository.update_todo(id, completed=True)

    def mark_incomplete(self, id: int) -> Optional[Todo]:
        """
        Mark a todo as incomplete.

        Args:
            id (int): The ID of the todo to mark as incomplete

        Returns:
            Optional[Todo]: The updated todo if found, None otherwise
        """
        return self.repository.update_todo(id, completed=False)