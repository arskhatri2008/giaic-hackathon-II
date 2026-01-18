"""
Todo entity and TodoList collection implementation.
"""

from typing import Dict, List, Optional


class Todo:
    """
    Represents a single todo item.

    Attributes:
        id (int): Unique identifier for the todo item, auto-generated and immutable
        title (str): The text description of the todo item, required field
        completed (bool): Boolean indicating whether the todo is completed, defaults to False
    """

    def __init__(self, id: int, title: str, completed: bool = False):
        if not title or title.strip() == "":
            raise ValueError("Todo title cannot be empty or contain only whitespace")

        self._id = id
        self._title = title.strip()
        self._completed = completed

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or value.strip() == "":
            raise ValueError("Todo title cannot be empty or contain only whitespace")
        self._title = value.strip()

    @property
    def completed(self) -> bool:
        return self._completed

    @completed.setter
    def completed(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Completed status must be a boolean")
        self._completed = value

    def __repr__(self) -> str:
        return f"Todo(id={self.id}, title='{self.title}', completed={self.completed})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Todo):
            return False
        return self.id == other.id and self.title == other.title and self.completed == other.completed


class TodoList:
    """
    Collection of todos stored in memory during application runtime.

    Attributes:
        todos (Dict[int, Todo]): Dictionary mapping todo IDs to Todo objects for O(1) lookup
        next_id (int): Counter for generating unique IDs, starts at 1 and increments
    """

    def __init__(self):
        self.todos: Dict[int, Todo] = {}
        self.next_id = 1

    def add(self, todo: Todo) -> Todo:
        """Add a new todo to the collection with a unique ID."""
        if todo.id in self.todos:
            raise ValueError(f"Todo with ID {todo.id} already exists")
        self.todos[todo.id] = todo
        return todo

    def get(self, id: int) -> Optional[Todo]:
        """Retrieve a todo by its ID."""
        return self.todos.get(id)

    def update(self, id: int, **kwargs) -> Optional[Todo]:
        """Update properties of an existing todo."""
        if id not in self.todos:
            return None

        todo = self.todos[id]

        if 'title' in kwargs:
            todo.title = kwargs['title']
        if 'completed' in kwargs:
            todo.completed = kwargs['completed']

        return todo

    def remove(self, id: int) -> bool:
        """Remove a todo from the collection."""
        if id in self.todos:
            del self.todos[id]
            return True
        return False

    def list_all(self) -> List[Todo]:
        """Return all todos in the collection."""
        return list(self.todos.values())

    def list_completed(self) -> List[Todo]:
        """Return only completed todos."""
        return [todo for todo in self.todos.values() if todo.completed]

    def list_pending(self) -> List[Todo]:
        """Return only pending todos."""
        return [todo for todo in self.todos.values() if not todo.completed]

    def generate_next_id(self) -> int:
        """Generate and return the next unique ID."""
        current_id = self.next_id
        self.next_id += 1
        return current_id