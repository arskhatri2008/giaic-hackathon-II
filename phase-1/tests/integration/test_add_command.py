"""
Integration tests for the add command flow.
"""

import pytest
from todo_app.services.todo_service import TodoService
from todo_app.repositories.todo_repository import TodoRepository
from todo_app.cli.commands import TodoCLI


class TestAddCommandIntegration:
    def test_add_command_creates_todo(self):
        """Test that the add command creates a todo via the service layer."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo using the CLI command
        result = cli.handle_add("Buy groceries")

        # Verify the result message indicates success
        assert "Todo added with ID:" in result
        assert "1" in result  # Should be the first todo with ID 1

        # Verify the todo was actually created in the repository
        all_todos = repository.get_all_todos()
        assert len(all_todos) == 1
        assert all_todos[0].id == 1
        assert all_todos[0].title == "Buy groceries"
        assert all_todos[0].completed is False

    def test_add_command_with_multiple_todos(self):
        """Test that multiple add commands create multiple todos."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add multiple todos
        result1 = cli.handle_add("Buy groceries")
        result2 = cli.handle_add("Walk the dog")

        # Verify both results indicate success
        assert "Todo added with ID: 1" in result1
        assert "Todo added with ID: 2" in result2

        # Verify both todos were created
        all_todos = repository.get_all_todos()
        assert len(all_todos) == 2

        # Find and verify the specific todos
        todo1 = repository.get_todo(1)
        todo2 = repository.get_todo(2)
        assert todo1.title == "Buy groceries"
        assert todo2.title == "Walk the dog"

    def test_add_command_with_empty_description(self):
        """Test that the add command handles empty description."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Try to add an empty todo
        result = cli.handle_add("")

        # Verify error message
        assert "Error:" in result

        # Verify no todos were created
        all_todos = repository.get_all_todos()
        assert len(all_todos) == 0

    def test_add_command_with_whitespace_only_description(self):
        """Test that the add command handles whitespace-only description."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Try to add a whitespace-only todo
        result = cli.handle_add("   ")

        # Verify error message
        assert "Error:" in result

        # Verify no todos were created
        all_todos = repository.get_all_todos()
        assert len(all_todos) == 0

    def test_add_command_via_service_directly_and_verify_cli_can_see_it(self):
        """Test that a todo added via service directly is visible to CLI commands."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo directly through the service
        service.add_todo("Directly added todo")

        # Verify it can be seen when viewing all todos via CLI
        view_result = cli.handle_view("")
        assert "Directly added todo" in view_result