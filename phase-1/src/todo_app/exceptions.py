"""
Custom exception classes for error handling.
"""


class TodoException(Exception):
    """Base exception class for todo-related errors."""
    pass


class TodoNotFoundError(TodoException):
    """Raised when a requested todo is not found."""

    def __init__(self, todo_id: int):
        self.todo_id = todo_id
        super().__init__(f"Todo with ID {todo_id} not found")


class InvalidTodoError(TodoException):
    """Raised when a todo is invalid (e.g., empty title)."""

    def __init__(self, message: str = "Invalid todo"):
        super().__init__(message)


class DuplicateTodoError(TodoException):
    """Raised when attempting to create a duplicate todo."""

    def __init__(self, todo_id: int):
        self.todo_id = todo_id
        super().__init__(f"Todo with ID {todo_id} already exists")