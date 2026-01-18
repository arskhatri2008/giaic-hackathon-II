"""
Unit tests for delete functionality in TodoService.
"""

import pytest
from todo_app.services.todo_service import TodoService


class TestDeleteFunctionality:
    def test_delete_existing_todo(self):
        """Test successfully deleting an existing todo."""
        service = TodoService()

        # Add a todo
        todo = service.add_todo("Test todo")

        # Delete the todo
        result = service.delete_todo(todo.id)

        # Verify the result
        assert result is True

        # Verify the todo no longer exists
        retrieved_todo = service.get_todo(todo.id)
        assert retrieved_todo is None

    def test_delete_nonexistent_todo(self):
        """Test deleting a nonexistent todo."""
        service = TodoService()

        # Try to delete a nonexistent todo
        result = service.delete_todo(999)

        # Verify the result
        assert result is False

    def test_delete_todo_removes_from_list(self):
        """Test that deleting a todo removes it from the list."""
        service = TodoService()

        # Add multiple todos
        todo1 = service.add_todo("Todo 1")
        todo2 = service.add_todo("Todo 2")
        todo3 = service.add_todo("Todo 3")

        # Verify all exist initially
        assert len(service.get_all_todos()) == 3
        assert service.get_todo(todo1.id) is not None
        assert service.get_todo(todo2.id) is not None
        assert service.get_todo(todo3.id) is not None

        # Delete one todo
        service.delete_todo(todo2.id)

        # Verify it's gone but others remain
        assert len(service.get_all_todos()) == 2
        assert service.get_todo(todo1.id) is not None
        assert service.get_todo(todo2.id) is None
        assert service.get_todo(todo3.id) is not None

    def test_delete_all_todos(self):
        """Test deleting all todos."""
        service = TodoService()

        # Add multiple todos
        todo1 = service.add_todo("Todo 1")
        todo2 = service.add_todo("Todo 2")
        todo3 = service.add_todo("Todo 3")

        # Delete all of them
        result1 = service.delete_todo(todo1.id)
        result2 = service.delete_todo(todo2.id)
        result3 = service.delete_todo(todo3.id)

        # Verify all deletions succeeded
        assert result1 is True
        assert result2 is True
        assert result3 is True

        # Verify no todos remain
        assert len(service.get_all_todos()) == 0
        assert service.get_todo(todo1.id) is None
        assert service.get_todo(todo2.id) is None
        assert service.get_todo(todo3.id) is None

    def test_delete_todo_does_not_affect_others(self):
        """Test that deleting one todo doesn't affect others."""
        service = TodoService()

        # Add multiple todos with different statuses
        todo1 = service.add_todo("Pending todo")
        todo2 = service.add_todo("To be completed")
        todo3 = service.add_todo("Another pending todo")

        # Mark one as complete
        service.mark_complete(todo2.id)

        # Verify initial state
        assert service.get_todo(todo1.id).completed is False
        assert service.get_todo(todo2.id).completed is True
        assert service.get_todo(todo3.id).completed is False

        # Delete the completed todo
        service.delete_todo(todo2.id)

        # Verify the other todos are unaffected
        assert service.get_todo(todo1.id) is not None
        assert service.get_todo(todo1.id).completed is False
        assert service.get_todo(todo3.id) is not None
        assert service.get_todo(todo3.id).completed is False
        assert service.get_todo(todo2.id) is None

    def test_delete_todo_then_try_to_update(self):
        """Test that updating a deleted todo fails."""
        service = TodoService()

        # Add a todo
        todo = service.add_todo("Test todo")

        # Delete the todo
        service.delete_todo(todo.id)

        # Try to update the deleted todo
        result = service.update_todo(todo.id, title="Updated title")

        # Verify the update failed
        assert result is None

    def test_delete_todo_then_try_to_mark_complete(self):
        """Test that marking a deleted todo as complete fails."""
        service = TodoService()

        # Add a todo
        todo = service.add_todo("Test todo")

        # Delete the todo
        service.delete_todo(todo.id)

        # Try to mark the deleted todo as complete
        result = service.mark_complete(todo.id)

        # Verify the operation failed
        assert result is None

    def test_delete_todo_id_generation_continues_correctly(self):
        """Test that ID generation continues correctly after deletion."""
        service = TodoService()

        # Add some todos
        todo1 = service.add_todo("First todo")
        todo2 = service.add_todo("Second todo")
        todo3 = service.add_todo("Third todo")

        # Delete the middle one
        service.delete_todo(todo2.id)

        # Add a new todo - it should get the next available ID
        todo4 = service.add_todo("Fourth todo")

        # Verify the ID assignment
        assert todo4.id == 4  # Should be the next ID after deletion

    def test_delete_todo_and_add_new_one(self):
        """Test deleting a todo and adding a new one."""
        service = TodoService()

        # Add a todo
        original_todo = service.add_todo("Original todo")
        original_id = original_todo.id

        # Delete the todo
        service.delete_todo(original_id)

        # Add a new todo
        new_todo = service.add_todo("New todo")

        # Verify the new todo has a different ID
        assert new_todo.id != original_id
        assert new_todo.id == original_id + 1  # Next available ID

    def test_delete_todo_with_same_title_as_others(self):
        """Test deleting a todo when other todos have the same title."""
        service = TodoService()

        # Add todos with the same title
        todo1 = service.add_todo("Same title")
        todo2 = service.add_todo("Same title")
        todo3 = service.add_todo("Same title")

        # Delete only one of them
        service.delete_todo(todo2.id)

        # Verify the others remain
        assert service.get_todo(todo1.id) is not None
        assert service.get_todo(todo2.id) is None
        assert service.get_todo(todo3.id) is not None
        assert len(service.get_all_todos()) == 2