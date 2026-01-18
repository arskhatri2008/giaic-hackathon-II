"""
Unit tests for mark_complete functionality in TodoService.
"""

import pytest
from todo_app.services.todo_service import TodoService
from todo_app.exceptions import TodoNotFoundError


class TestMarkCompleteFunctionality:
    def test_mark_complete_success(self):
        """Test successfully marking a todo as complete."""
        service = TodoService()

        # Add a todo
        todo = service.add_todo("Test todo")

        # Mark it as complete
        result = service.mark_complete(todo.id)

        # Verify the result
        assert result is not None
        assert result.id == todo.id
        assert result.title == todo.title
        assert result.completed is True

    def test_mark_complete_nonexistent_todo(self):
        """Test marking a nonexistent todo as complete."""
        service = TodoService()

        # Try to mark a nonexistent todo as complete
        result = service.mark_complete(999)

        # Verify the result
        assert result is None

    def test_mark_already_complete_todo(self):
        """Test marking an already complete todo."""
        service = TodoService()

        # Add a todo and mark it as complete
        todo = service.add_todo("Test todo")
        service.mark_complete(todo.id)

        # Try to mark it as complete again
        result = service.mark_complete(todo.id)

        # Verify it's still complete
        assert result is not None
        assert result.completed is True

    def test_mark_complete_persists_change(self):
        """Test that marking complete persists the change."""
        service = TodoService()

        # Add a todo
        todo = service.add_todo("Test todo")

        # Verify it starts as incomplete
        assert todo.completed is False

        # Mark it as complete
        service.mark_complete(todo.id)

        # Get the todo again and verify it's complete
        retrieved_todo = service.get_todo(todo.id)
        assert retrieved_todo is not None
        assert retrieved_todo.completed is True

    def test_mark_incomplete_functionality(self):
        """Test marking a todo as incomplete."""
        service = TodoService()

        # Add a todo and mark it as complete
        todo = service.add_todo("Test todo")
        service.mark_complete(todo.id)

        # Verify it's complete
        retrieved_todo = service.get_todo(todo.id)
        assert retrieved_todo is not None
        assert retrieved_todo.completed is True

        # Mark it as incomplete
        result = service.mark_incomplete(todo.id)

        # Verify the result
        assert result is not None
        assert result.completed is False

    def test_mark_incomplete_nonexistent_todo(self):
        """Test marking a nonexistent todo as incomplete."""
        service = TodoService()

        # Try to mark a nonexistent todo as incomplete
        result = service.mark_incomplete(999)

        # Verify the result
        assert result is None

    def test_mark_complete_then_incomplete_workflow(self):
        """Test marking a todo complete then incomplete."""
        service = TodoService()

        # Add a todo
        todo = service.add_todo("Test todo")

        # Verify it starts as incomplete
        assert service.get_todo(todo.id).completed is False

        # Mark it as complete
        service.mark_complete(todo.id)
        assert service.get_todo(todo.id).completed is True

        # Mark it as incomplete
        service.mark_incomplete(todo.id)
        assert service.get_todo(todo.id).completed is False

    def test_mark_complete_affects_other_todos_correctly(self):
        """Test that marking one todo complete doesn't affect others."""
        service = TodoService()

        # Add multiple todos
        todo1 = service.add_todo("Todo 1")
        todo2 = service.add_todo("Todo 2")
        todo3 = service.add_todo("Todo 3")

        # Mark only the second one as complete
        service.mark_complete(todo2.id)

        # Check the status of all todos
        assert service.get_todo(todo1.id).completed is False
        assert service.get_todo(todo2.id).completed is True
        assert service.get_todo(todo3.id).completed is False