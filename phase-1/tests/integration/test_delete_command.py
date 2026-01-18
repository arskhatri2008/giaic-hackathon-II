"""
Integration tests for the delete command flow.
"""

import pytest
from todo_app.services.todo_service import TodoService
from todo_app.repositories.todo_repository import TodoRepository
from todo_app.cli.commands import TodoCLI


class TestDeleteCommandIntegration:
    def test_delete_command_success(self):
        """Test successfully deleting a todo via CLI command."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo via service
        todo = service.add_todo("Test todo")

        # Delete the todo via CLI command
        result = cli.handle_delete(str(todo.id))

        # Verify the result message
        assert f"Todo {todo.id} deleted successfully." in result

        # Verify the todo is actually deleted from the service
        retrieved_todo = service.get_todo(todo.id)
        assert retrieved_todo is None

    def test_delete_command_nonexistent_todo(self):
        """Test deleting a nonexistent todo via CLI command."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Try to delete a nonexistent todo
        result = cli.handle_delete("999")

        # Verify the error message
        assert "not found" in result.lower()

    def test_delete_command_invalid_id(self):
        """Test deleting a todo with an invalid ID via CLI command."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Try to delete a todo with an invalid ID
        result = cli.handle_delete("invalid")

        # Verify the error message
        assert "error:" in result.lower()
        assert "invalid" in result.lower()

    def test_delete_command_then_view(self):
        """Test deleting a todo then viewing the remaining todos."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add multiple todos
        todo1 = service.add_todo("First todo")
        todo2 = service.add_todo("Second todo")
        todo3 = service.add_todo("Third todo")

        # Verify all exist initially
        initial_view = cli.handle_view("")
        assert "First todo" in initial_view
        assert "Second todo" in initial_view
        assert "Third todo" in initial_view
        assert initial_view.count("todo") >= 3  # At least 3 occurrences

        # Delete one via CLI command
        delete_result = cli.handle_delete(str(todo2.id))
        assert "deleted successfully" in delete_result.lower()

        # View remaining todos
        final_view = cli.handle_view("")

        # Verify deleted todo is gone but others remain
        assert "First todo" in final_view
        assert "Second todo" not in final_view
        assert "Third todo" in final_view
        assert final_view.count("todo") == 2  # Exactly 2 occurrences now

    def test_delete_all_todos_via_cli(self):
        """Test deleting all todos via CLI commands."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add multiple todos
        todo1 = service.add_todo("First todo")
        todo2 = service.add_todo("Second todo")
        todo3 = service.add_todo("Third todo")

        # Delete all via CLI commands
        cli.handle_delete(str(todo1.id))
        cli.handle_delete(str(todo2.id))
        cli.handle_delete(str(todo3.id))

        # View remaining todos
        final_view = cli.handle_view("")

        # Verify no todos remain
        assert "No todos found." in final_view

    def test_add_then_delete_via_cli_workflow(self):
        """Test the workflow of adding a todo then deleting it via CLI."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo via CLI
        add_result = cli.handle_add("To be deleted")
        # Extract the ID from the result
        added_todo_id = None
        if "ID:" in add_result:
            id_part = add_result.split("ID:")[-1].strip()
            # Extract the numeric ID
            import re
            match = re.search(r'\d+', id_part)
            if match:
                added_todo_id = int(match.group())

        assert added_todo_id is not None

        # Verify it exists
        view_before = cli.handle_view("")
        assert "To be deleted" in view_before

        # Delete it via CLI
        delete_result = cli.handle_delete(str(added_todo_id))
        assert "deleted successfully" in delete_result.lower()

        # Verify it's gone
        view_after = cli.handle_view("")
        assert "To be deleted" not in view_after
        assert "No todos found." in view_after

    def test_delete_then_view_consistency_across_layers(self):
        """Test that delete changes are consistent across service and CLI layers."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo via service
        todo = service.add_todo("Consistency test")

        # Verify it exists via CLI
        initial_view = cli.handle_view("")
        assert "consistency test" in initial_view.lower()

        # Delete it via service directly
        service.delete_todo(todo.id)

        # Verify it's gone via CLI view command
        final_view = cli.handle_view("")
        assert "consistency test" not in final_view.lower()
        assert "No todos found." in final_view

        # Add another via CLI
        cli.handle_add("Added via CLI")

        # Verify it exists via service
        all_todos = service.get_all_todos()
        assert len(all_todos) == 1
        assert "added via cli" in all_todos[0].title.lower()

        # Delete it via CLI
        for todo_item in all_todos:
            cli.handle_delete(str(todo_item.id))

        # Verify it's gone via service
        all_todos_after = service.get_all_todos()
        assert len(all_todos_after) == 0

    def test_delete_todo_then_add_new_one(self):
        """Test deleting a todo then adding a new one."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo via CLI
        add_result = cli.handle_add("To be deleted")
        import re
        match = re.search(r'\d+', add_result)
        if match:
            original_id = int(match.group())

        assert original_id is not None

        # Delete it via CLI
        delete_result = cli.handle_delete(str(original_id))
        assert "deleted successfully" in delete_result.lower()

        # Add a new one via CLI
        new_add_result = cli.handle_add("New todo")
        new_match = re.search(r'\d+', new_add_result)
        if new_match:
            new_id = int(new_match.group())

        assert new_id is not None
        assert new_id == original_id + 1  # Should be the next ID

    def test_delete_completed_todo(self):
        """Test deleting a completed todo."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo and mark it as complete
        todo = service.add_todo("Completed to delete")
        service.mark_complete(todo.id)

        # Verify it's complete
        all_todos = service.get_all_todos()
        assert len(all_todos) == 1
        assert all_todos[0].completed is True

        # Delete it via CLI
        delete_result = cli.handle_delete(str(todo.id))
        assert "deleted successfully" in delete_result.lower()

        # Verify it's gone
        all_todos_after = service.get_all_todos()
        assert len(all_todos_after) == 0