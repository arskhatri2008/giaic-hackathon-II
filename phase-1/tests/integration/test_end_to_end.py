"""
End-to-end integration tests for the todo application.
"""

import pytest
from todo_app.services.todo_service import TodoService
from todo_app.repositories.todo_repository import TodoRepository
from todo_app.cli.commands import TodoCLI


class TestEndToEnd:
    def test_full_workflow_basic_scenario(self):
        """Test a full workflow: add, view, update, complete, delete."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Step 1: Add a todo
        add_result = cli.handle_add("Buy groceries")
        assert "Todo added with ID:" in add_result

        # Extract the ID from the result
        import re
        match = re.search(r'ID: (\d+)', add_result)
        assert match is not None
        todo_id = int(match.group(1))

        # Step 2: View todos
        view_result = cli.handle_view("")
        assert "Buy groceries" in view_result
        assert "Pending" in view_result

        # Step 3: Update the todo
        update_result = cli.handle_update(f'{todo_id} "Buy groceries and cook dinner"')
        assert "updated successfully" in update_result.lower()

        # Step 4: Verify the update
        view_after_update = cli.handle_view("")
        assert "cook dinner" in view_after_update.lower()

        # Step 5: Mark as complete
        complete_result = cli.handle_complete(str(todo_id))
        assert "marked as complete" in complete_result.lower()

        # Step 6: Verify completion status
        view_after_complete = cli.handle_view("")
        assert "complete" in view_after_complete.lower()

        # Step 7: Delete the todo
        delete_result = cli.handle_delete(str(todo_id))
        assert "deleted successfully" in delete_result.lower()

        # Step 8: Verify deletion
        final_view = cli.handle_view("")
        assert "No todos found." in final_view

    def test_multiple_todos_workflow(self):
        """Test working with multiple todos simultaneously."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add multiple todos
        result1 = cli.handle_add("First task")
        result2 = cli.handle_add("Second task")
        result3 = cli.handle_add("Third task")

        # Extract IDs
        import re
        id1 = int(re.search(r'ID: (\d+)', result1).group(1))
        id2 = int(re.search(r'ID: (\d+)', result2).group(1))
        id3 = int(re.search(r'ID: (\d+)', result3).group(1))

        # Verify all exist
        view_result = cli.handle_view("")
        assert "First task" in view_result
        assert "Second task" in view_result
        assert "Third task" in view_result
        assert view_result.count("task") >= 3

        # Complete the second one
        cli.handle_complete(str(id2))

        # Update the third one
        cli.handle_update(f'{id3} "Third task - updated"')

        # View and verify states
        view_result = cli.handle_view("")
        assert "first task" in view_result.lower()
        assert "second task" in view_result.lower()
        assert "pending" in view_result.lower() or "complete" in view_result.lower()
        assert "updated" in view_result.lower()

        # Delete the first one
        cli.handle_delete(str(id1))

        # Verify only 2 remain
        view_result = cli.handle_view("")
        assert view_result.count("task") == 2  # Only second and third remain

    def test_error_handling_workflow(self):
        """Test error handling throughout the workflow."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Try to update a non-existent todo
        error_result = cli.handle_update('999 "Non-existent"')
        assert "not found" in error_result.lower()

        # Add a valid todo
        add_result = cli.handle_add("Valid task")
        import re
        todo_id = int(re.search(r'ID: (\d+)', add_result).group(1))

        # Try to update with empty description
        error_result2 = cli.handle_update(f'{todo_id} ""')
        assert "error:" in error_result2.lower()
        assert "empty" in error_result2.lower()

        # Verify the original task is still there with original name
        view_result = cli.handle_view("")
        assert "valid task" in view_result.lower()

    def test_mixed_operations_workflow(self):
        """Test mixing different operations."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add several todos
        results = []
        for i in range(1, 6):
            result = cli.handle_add(f"Task {i}")
            results.append(int(re.search(r'ID: (\d+)', result).group(1)))

        # Mark some as complete
        cli.handle_complete(str(results[0]))  # Task 1
        cli.handle_complete(str(results[2]))  # Task 3

        # Update some
        cli.handle_update(f'{results[1]} "Updated Task 2"')  # Task 2
        cli.handle_update(f'{results[4]} "Updated Task 5"')  # Task 5

        # Delete one
        cli.handle_delete(str(results[3]))  # Task 4

        # View final state
        view_result = cli.handle_view("")

        # Should have 4 tasks remaining (original 5 - 1 deleted)
        # With proper statuses
        assert view_result.count("|") >= 5  # header + 4 tasks
        assert "updated task 2" in view_result.lower()
        assert "updated task 5" in view_result.lower()
        assert "task 1" in view_result.lower() or "complete" in view_result.lower()

    def test_edge_cases_workflow(self):
        """Test edge cases in a workflow."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add a todo with special characters
        special_result = cli.handle_add('Task with "quotes" and \'apostrophes\'!')
        import re
        special_id = int(re.search(r'ID: (\d+)', special_result).group(1))

        # View and ensure it's stored correctly
        view_result = cli.handle_view("")
        assert "quotes" in view_result.lower()
        assert "apostrophes" in view_result.lower()

        # Update it with more special characters
        cli.handle_update(f'{special_id} "Updated: [email protected]#$%"')

        # View again
        view_result = cli.handle_view("")
        assert "@" in view_result or "#" in view_result or "$" in view_result

        # Try various error conditions
        errors_tested = 0

        # Invalid ID for update
        if "not found" in cli.handle_update('999999 "test"').lower():
            errors_tested += 1

        # Invalid ID for complete
        if "not found" in cli.handle_complete('999999').lower():
            errors_tested += 1

        # Invalid ID for delete
        if "not found" in cli.handle_delete('999999').lower():
            errors_tested += 1

        # Ensure we tested error conditions
        assert errors_tested >= 3

    def test_consistency_across_operations(self):
        """Test that data remains consistent across operations."""
        repository = TodoRepository()
        service = TodoService(repository)
        cli = TodoCLI(service)

        # Add todos through different methods and verify consistency
        todo1_service = service.add_todo("Service added todo")

        add_cli_result = cli.handle_add("CLI added todo")
        cli_id = int(re.search(r'ID: (\d+)', add_cli_result).group(1))

        # View through CLI - both should be visible
        view_result = cli.handle_view("")
        assert "service added todo" in view_result.lower()
        assert "cli added todo" in view_result.lower()

        # Update through service, check through CLI
        service.update_todo(todo1_service.id, title="Service updated todo")

        view_after_update = cli.handle_view("")
        assert "service updated todo" in view_after_update.lower()

        # Mark complete through CLI, check through service
        cli.handle_complete(str(cli_id))

        cli_todo = service.get_todo(cli_id)
        assert cli_todo is not None
        assert cli_todo.completed is True

        # Count should be consistent
        all_from_service = service.get_all_todos()
        # We can't directly call the CLI's view function to count, but we know there are 2 todos
        assert len(all_from_service) == 2