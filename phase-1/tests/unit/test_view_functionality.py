"""
Unit tests for view functionality in TodoService.
"""

import pytest
from todo_app.services.todo_service import TodoService


class TestViewFunctionality:
    def test_get_all_todos_empty_list(self):
        """Test getting all todos when list is empty."""
        service = TodoService()

        result = service.get_all_todos()

        assert result == []
        assert len(result) == 0

    def test_get_all_todos_with_items(self):
        """Test getting all todos when list has items."""
        service = TodoService()

        # Add some todos
        service.add_todo("First todo")
        service.add_todo("Second todo")
        service.add_todo("Third todo")

        result = service.get_all_todos()

        assert len(result) == 3
        titles = [todo.title for todo in result]
        assert "First todo" in titles
        assert "Second todo" in titles
        assert "Third todo" in titles

    def test_get_completed_todos_empty_list(self):
        """Test getting completed todos when list is empty."""
        service = TodoService()

        result = service.get_completed_todos()

        assert result == []
        assert len(result) == 0

    def test_get_completed_todos_with_mixed_status(self):
        """Test getting completed todos from mixed status todos."""
        service = TodoService()

        # Add todos with different completion statuses
        service.add_todo("Pending todo 1")
        service.add_todo("Pending todo 2")
        completed_todo = service.add_todo("Completed todo")
        service.mark_complete(completed_todo.id)

        result = service.get_completed_todos()

        assert len(result) == 1
        assert result[0].title == "Completed todo"
        assert result[0].completed is True

    def test_get_pending_todos_empty_list(self):
        """Test getting pending todos when list is empty."""
        service = TodoService()

        result = service.get_pending_todos()

        assert result == []
        assert len(result) == 0

    def test_get_pending_todos_with_mixed_status(self):
        """Test getting pending todos from mixed status todos."""
        service = TodoService()

        # Add todos with different completion statuses
        pending_todo1 = service.add_todo("Pending todo 1")
        pending_todo2 = service.add_todo("Pending todo 2")
        completed_todo = service.add_todo("Completed todo")
        service.mark_complete(completed_todo.id)

        result = service.get_pending_todos()

        assert len(result) == 2
        titles = [todo.title for todo in result]
        assert "Pending todo 1" in titles
        assert "Pending todo 2" in titles
        assert "Completed todo" not in titles

    def test_get_pending_todos_all_completed(self):
        """Test getting pending todos when all are completed."""
        service = TodoService()

        # Add todos and mark them all as complete
        todo1 = service.add_todo("Completed todo 1")
        todo2 = service.add_todo("Completed todo 2")
        service.mark_complete(todo1.id)
        service.mark_complete(todo2.id)

        result = service.get_pending_todos()

        assert result == []
        assert len(result) == 0

    def test_get_completed_todos_all_pending(self):
        """Test getting completed todos when all are pending."""
        service = TodoService()

        # Add todos without marking them as complete
        service.add_todo("Pending todo 1")
        service.add_todo("Pending todo 2")

        result = service.get_completed_todos()

        assert result == []
        assert len(result) == 0

    def test_get_todo_by_id(self):
        """Test getting a specific todo by its ID."""
        service = TodoService()

        # Add a todo
        added_todo = service.add_todo("Test todo")

        # Retrieve it by ID
        retrieved_todo = service.get_todo(added_todo.id)

        assert retrieved_todo is not None
        assert retrieved_todo.id == added_todo.id
        assert retrieved_todo.title == added_todo.title
        assert retrieved_todo.completed == added_todo.completed

    def test_get_todo_by_nonexistent_id(self):
        """Test getting a todo by a nonexistent ID."""
        service = TodoService()

        # Try to retrieve a todo with a nonexistent ID
        retrieved_todo = service.get_todo(999)

        assert retrieved_todo is None