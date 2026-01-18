"""
Integration tests for the update command flow.
"""

import pytest
from todo_app.services.todo_service import TodoService
from todo_app.repositories.todo_repository import TodoRepository
from todo_app.cli.commands import TodoCLI


class TestUpdateCommandIntegration:
    def test_update_command_success(self):
        """Test successfully updating a todo via CLI command."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo via service
        todo = service.add_todo("Original title")

        # Update the todo via CLI command
        result = cli.handle_update(f'{todo.id} "Updated title"')

        # Verify the result message
        assert f"Todo {todo.id} updated successfully." in result

        # Verify the todo is actually updated in the service
        retrieved_todo = service.get_todo(todo.id)
        assert retrieved_todo is not None
        assert retrieved_todo.title == "Updated title"

    def test_update_command_nonexistent_todo(self):
        """Test updating a nonexistent todo via CLI command."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Try to update a nonexistent todo
        result = cli.handle_update('999 "New title"')

        # Verify the error message
        assert "not found" in result.lower()

    def test_update_command_invalid_id(self):
        """Test updating a todo with an invalid ID via CLI command."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Try to update a todo with an invalid ID
        result = cli.handle_update('invalid "New title"')

        # Verify the error message
        assert "error:" in result.lower()
        assert "invalid" in result.lower()

    def test_update_command_empty_new_title(self):
        """Test updating a todo with an empty new title via CLI command."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo
        todo = service.add_todo("Original title")

        # Try to update with an empty title
        result = cli.handle_update(f'{todo.id} ""')

        # Verify the error message
        assert "error:" in result.lower()
        assert "empty" in result.lower()

    def test_update_command_then_view(self):
        """Test updating a todo then viewing it."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo via service
        todo = service.add_todo("To be updated")

        # Update it via CLI command
        update_result = cli.handle_update(f'{todo.id} "Updated title"')
        assert "updated successfully" in update_result.lower()

        # View todos via CLI command
        view_result = cli.handle_view("")

        # Verify the updated title appears
        assert "updated title" in view_result.lower()

    def test_update_command_with_quotes_in_title(self):
        """Test updating a todo with quotes in the new title."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo
        todo = service.add_todo("Original title")

        # Update it with a title containing quotes
        result = cli.handle_update(f'{todo.id} "Title with \\"quotes\\" inside"')

        # Verify the update succeeded
        assert "updated successfully" in result.lower()

        # Verify the title was updated correctly
        retrieved_todo = service.get_todo(todo.id)
        assert retrieved_todo is not None
        assert "quotes" in retrieved_todo.title

    def test_add_then_update_via_cli_workflow(self):
        """Test the workflow of adding a todo then updating it via CLI."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo via CLI
        add_result = cli.handle_add("Initial title")
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

        # Update it via CLI
        update_result = cli.handle_update(f'{added_todo_id} "Updated via CLI"')
        assert "updated successfully" in update_result.lower()

        # Verify it's updated
        all_todos = service.get_all_todos()
        updated_todo = next((t for t in all_todos if t.id == added_todo_id), None)
        assert updated_todo is not None
        assert updated_todo.title == "Updated via CLI"

    def test_update_then_view_consistency_across_layers(self):
        """Test that update changes are consistent across service and CLI layers."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo via service
        todo = service.add_todo("Consistency test")

        # Update it via service directly
        service.update_todo(todo.id, title="Updated via service")

        # Verify via CLI view command
        view_result = cli.handle_view("")
        assert "updated via service" in view_result.lower()

        # Update it via CLI
        cli.handle_update(f'{todo.id} "Updated via CLI"')

        # Verify the change is reflected in the service
        retrieved_todo = service.get_todo(todo.id)
        assert retrieved_todo is not None
        assert "updated via cli" in retrieved_todo.title.lower()

    def test_update_command_with_completion_status_change_not_supported(self):
        """Test that the CLI update command doesn't change completion status (directly)."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo and mark it as complete
        todo = service.add_todo("Test todo")
        service.mark_complete(todo.id)

        # Update the title via CLI
        cli.handle_update(f'{todo.id} "Updated title"')

        # Verify the completion status didn't change
        retrieved_todo = service.get_todo(todo.id)
        assert retrieved_todo is not None
        assert retrieved_todo.completed is True  # Should still be complete
        assert retrieved_todo.title == "Updated title"