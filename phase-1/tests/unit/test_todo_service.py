"""
Unit tests for TodoService add functionality.
"""

import pytest
from todo_app.services.todo_service import TodoService
from todo_app.repositories.todo_repository import TodoRepository


class TestTodoServiceAdd:
    def test_add_valid_todo(self):
        """Test adding a valid todo."""
        service = TodoService()
        result = service.add_todo("Test todo")

        assert result is not None
        assert result.id == 1
        assert result.title == "Test todo"
        assert result.completed is False

    def test_add_multiple_todos(self):
        """Test adding multiple todos with unique IDs."""
        service = TodoService()

        todo1 = service.add_todo("First todo")
        todo2 = service.add_todo("Second todo")

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo1.title == "First todo"
        assert todo2.title == "Second todo"

    def test_add_empty_title_raises_error(self):
        """Test that adding a todo with empty title raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError):
            service.add_todo("")

    def test_add_whitespace_only_title_raises_error(self):
        """Test that adding a todo with whitespace-only title raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError):
            service.add_todo("   ")

    def test_added_todo_is_retrievable(self):
        """Test that an added todo can be retrieved."""
        service = TodoService()
        added_todo = service.add_todo("Test todo")

        retrieved_todo = service.get_todo(added_todo.id)

        assert retrieved_todo is not None
        assert retrieved_todo.id == added_todo.id
        assert retrieved_todo.title == added_todo.title
        assert retrieved_todo.completed == added_todo.completed

    def test_add_todo_with_custom_repository(self):
        """Test adding todo works with custom repository."""
        repository = TodoRepository()
        service = TodoService(repository)

        todo = service.add_todo("Test todo")

        assert todo is not None
        assert todo.id == 1
        assert todo.title == "Test todo"