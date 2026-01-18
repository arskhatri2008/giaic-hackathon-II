"""
Integration tests for the view command flow.
"""

import pytest
from todo_app.services.todo_service import TodoService
from todo_app.repositories.todo_repository import TodoRepository
from todo_app.cli.commands import TodoCLI


class TestViewCommandIntegration:
    def test_view_command_empty_list(self):
        """Test that the view command shows appropriate message when no todos exist."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # View todos when none exist
        result = cli.handle_view("")

        assert result == "No todos found."

    def test_view_command_single_todo(self):
        """Test that the view command displays a single todo correctly."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a single todo
        service.add_todo("Single todo item")

        # View todos
        result = cli.handle_view("")

        assert "Single todo item" in result
        assert "ID" in result
        assert "Title" in result
        assert "Status" in result

    def test_view_command_multiple_todos(self):
        """Test that the view command displays multiple todos correctly."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add multiple todos
        service.add_todo("First todo")
        service.add_todo("Second todo")
        service.add_todo("Third todo")

        # View todos
        result = cli.handle_view("")

        assert "First todo" in result
        assert "Second todo" in result
        assert "Third todo" in result
        assert result.count("|") >= 6  # At least header + 3 todos with separators

    def test_view_command_with_completed_todos(self):
        """Test that the view command shows completion status correctly."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo and mark it as complete
        todo = service.add_todo("Completed todo")
        service.mark_complete(todo.id)

        # Add a pending todo
        service.add_todo("Pending todo")

        # View todos
        result = cli.handle_view("")

        assert "Complete" in result
        assert "Pending" in result

    def test_add_and_view_workflow(self):
        """Test the workflow of adding a todo and then viewing it."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo via the CLI
        add_result = cli.handle_add("Workflow test todo")

        # Verify add was successful
        assert "Todo added with ID:" in add_result

        # View todos via the CLI
        view_result = cli.handle_view("")

        assert "Workflow test todo" in view_result

    def test_view_after_adding_and_completing(self):
        """Test viewing todos after adding and marking one as complete."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add two todos
        todo1 = service.add_todo("Pending todo")
        todo2 = service.add_todo("Will be completed")

        # Mark one as complete using the service
        service.mark_complete(todo2.id)

        # View todos
        result = cli.handle_view("")

        # Both should appear but with different statuses
        assert "Pending todo" in result
        assert "Will be completed" in result
        assert "Complete" in result
        assert "Pending" in result

    def test_view_command_via_cli_and_verification_through_service(self):
        """Test that todos added via service are visible through CLI view command."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add todos directly through service
        service.add_todo("Service added todo 1")
        service.add_todo("Service added todo 2")

        # Verify they appear when viewed via CLI
        result = cli.handle_view("")

        assert "Service added todo 1" in result
        assert "Service added todo 2" in result