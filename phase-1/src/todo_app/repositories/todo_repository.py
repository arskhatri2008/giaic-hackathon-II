"""
In-memory storage implementation for todos.
"""

from typing import List, Optional
from ..models.todo import Todo, TodoList


class TodoRepository:
    """
    Repository for managing Todo entities in memory.
    """

    def __init__(self):
        self._todo_list = TodoList()

    def add_todo(self, title: str) -> Todo:
        """
        Add a new todo with a unique ID.

        Args:
            title (str): The title of the todo

        Returns:
            Todo: The created todo object with a unique ID
        """
        next_id = self._todo_list.generate_next_id()
        todo = Todo(next_id, title)
        self._todo_list.add(todo)
        return todo

    def get_todo(self, id: int) -> Optional[Todo]:
        """
        Retrieve a todo by its ID.

        Args:
            id (int): The ID of the todo to retrieve

        Returns:
            Optional[Todo]: The todo if found, None otherwise
        """
        return self._todo_list.get(id)

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
        update_kwargs = {}
        if title is not None:
            update_kwargs['title'] = title
        if completed is not None:
            update_kwargs['completed'] = completed

        return self._todo_list.update(id, **update_kwargs)

    def delete_todo(self, id: int) -> bool:
        """
        Delete a todo by its ID.

        Args:
            id (int): The ID of the todo to delete

        Returns:
            bool: True if the todo was deleted, False if not found
        """
        return self._todo_list.remove(id)

    def get_all_todos(self) -> List[Todo]:
        """
        Get all todos.

        Returns:
            List[Todo]: A list of all todos
        """
        return self._todo_list.list_all()

    def get_completed_todos(self) -> List[Todo]:
        """
        Get all completed todos.

        Returns:
            List[Todo]: A list of completed todos
        """
        return self._todo_list.list_completed()

    def get_pending_todos(self) -> List[Todo]:
        """
        Get all pending todos.

        Returns:
            List[Todo]: A list of pending todos
        """
        return self._todo_list.list_pending()