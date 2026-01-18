"""
Unit tests for update functionality in TodoService.
"""

import pytest
from todo_app.services.todo_service import TodoService
from todo_app.exceptions import TodoNotFoundError, InvalidTodoError


class TestUpdateFunctionality:
    def test_update_todo_title_success(self):
        """Test successfully updating a todo's title."""
        service = TodoService()

        # Add a todo
        todo = service.add_todo("Original title")

        # Update the title
        result = service.update_todo(todo.id, title="Updated title")

        # Verify the result
        assert result is not None
        assert result.id == todo.id
        assert result.title == "Updated title"
        assert result.completed == todo.completed  # Should remain unchanged

    def test_update_todo_completed_status(self):
        """Test updating a todo's completion status."""
        service = TodoService()

        # Add a todo
        todo = service.add_todo("Test todo")

        # Update the completion status
        result = service.update_todo(todo.id, completed=True)

        # Verify the result
        assert result is not None
        assert result.id == todo.id
        assert result.title == todo.title  # Should remain unchanged
        assert result.completed is True

    def test_update_todo_both_fields(self):
        """Test updating both title and completion status."""
        service = TodoService()

        # Add a todo
        todo = service.add_todo("Original title")

        # Update both fields
        result = service.update_todo(todo.id, title="New title", completed=True)

        # Verify the result
        assert result is not None
        assert result.id == todo.id
        assert result.title == "New title"
        assert result.completed is True

    def test_update_nonexistent_todo(self):
        """Test updating a nonexistent todo."""
        service = TodoService()

        # Try to update a nonexistent todo
        result = service.update_todo(999, title="New title")

        # Verify the result
        assert result is None

    def test_update_with_empty_title_raises_error(self):
        """Test that updating with an empty title raises ValueError."""
        service = TodoService()

        # Add a todo
        todo = service.add_todo("Original title")

        # Try to update with an empty title
        with pytest.raises(ValueError):
            service.update_todo(todo.id, title="")

    def test_update_with_whitespace_only_title_raises_error(self):
        """Test that updating with a whitespace-only title raises ValueError."""
        service = TodoService()

        # Add a todo
        todo = service.add_todo("Original title")

        # Try to update with a whitespace-only title
        with pytest.raises(ValueError):
            service.update_todo(todo.id, title="   ")

    def test_update_todo_partial_fields(self):
        """Test updating only one field while leaving others unchanged."""
        service = TodoService()

        # Add a todo with completed status True
        todo = service.add_todo("Original title")
        service.mark_complete(todo.id)  # Mark as complete

        # Update only the title, not the completion status
        result = service.update_todo(todo.id, title="Updated title")

        # Verify only the title changed
        assert result.title == "Updated title"
        assert result.completed is True  # Should remain completed

        # Update only the completion status, not the title
        result2 = service.update_todo(todo.id, completed=False)

        # Verify only the completion status changed
        assert result2.title == "Updated title"  # Should remain unchanged
        assert result2.completed is False

    def test_update_todo_persists_changes(self):
        """Test that updates persist in the repository."""
        service = TodoService()

        # Add a todo
        todo = service.add_todo("Original title")

        # Update the todo
        service.update_todo(todo.id, title="Updated title", completed=True)

        # Retrieve the todo again and verify changes persisted
        retrieved_todo = service.get_todo(todo.id)
        assert retrieved_todo is not None
        assert retrieved_todo.title == "Updated title"
        assert retrieved_todo.completed is True

    def test_update_todo_with_same_values(self):
        """Test updating a todo with the same values."""
        service = TodoService()

        # Add a todo
        todo = service.add_todo("Original title")

        # Update with the same title and completion status
        result = service.update_todo(todo.id, title="Original title", completed=False)

        # Verify the update worked (though values didn't change)
        assert result is not None
        assert result.id == todo.id
        assert result.title == "Original title"
        assert result.completed is False

    def test_update_multiple_todos_individually(self):
        """Test updating multiple todos individually."""
        service = TodoService()

        # Add multiple todos
        todo1 = service.add_todo("Todo 1")
        todo2 = service.add_todo("Todo 2")
        todo3 = service.add_todo("Todo 3")

        # Update each one differently
        service.update_todo(todo1.id, title="Updated Todo 1", completed=True)
        service.update_todo(todo2.id, title="Updated Todo 2", completed=False)
        service.update_todo(todo3.id, title="Updated Todo 3", completed=True)

        # Verify all updates occurred
        updated1 = service.get_todo(todo1.id)
        updated2 = service.get_todo(todo2.id)
        updated3 = service.get_todo(todo3.id)

        assert updated1.title == "Updated Todo 1"
        assert updated1.completed is True
        assert updated2.title == "Updated Todo 2"
        assert updated2.completed is False
        assert updated3.title == "Updated Todo 3"
        assert updated3.completed is True