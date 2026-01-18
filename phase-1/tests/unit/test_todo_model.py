"""
Unit tests for Todo model and TodoList collection.
"""

import pytest
from todo_app.models.todo import Todo, TodoList


class TestTodo:
    def test_create_valid_todo(self):
        """Test creating a valid Todo object."""
        todo = Todo(id=1, title="Test todo", completed=False)

        assert todo.id == 1
        assert todo.title == "Test todo"
        assert todo.completed is False

    def test_create_completed_todo(self):
        """Test creating a completed Todo object."""
        todo = Todo(id=1, title="Test todo", completed=True)

        assert todo.id == 1
        assert todo.title == "Test todo"
        assert todo.completed is True

    def test_empty_title_raises_error(self):
        """Test that creating a Todo with empty title raises ValueError."""
        with pytest.raises(ValueError):
            Todo(id=1, title="", completed=False)

    def test_whitespace_only_title_raises_error(self):
        """Test that creating a Todo with whitespace-only title raises ValueError."""
        with pytest.raises(ValueError):
            Todo(id=1, title="   ", completed=False)

    def test_title_setter_with_empty_value_raises_error(self):
        """Test that setting empty title raises ValueError."""
        todo = Todo(id=1, title="Initial title", completed=False)

        with pytest.raises(ValueError):
            todo.title = ""

    def test_title_setter_with_whitespace_only_raises_error(self):
        """Test that setting whitespace-only title raises ValueError."""
        todo = Todo(id=1, title="Initial title", completed=False)

        with pytest.raises(ValueError):
            todo.title = "   "

    def test_title_setter_strips_whitespace(self):
        """Test that setting title strips leading/trailing whitespace."""
        todo = Todo(id=1, title="Initial title", completed=False)
        todo.title = "  New title  "

        assert todo.title == "New title"

    def test_completed_setter_with_non_bool_raises_error(self):
        """Test that setting completed with non-bool raises ValueError."""
        todo = Todo(id=1, title="Test todo", completed=False)

        with pytest.raises(ValueError):
            todo.completed = "not a boolean"

    def test_repr(self):
        """Test the __repr__ method."""
        todo = Todo(id=1, title="Test todo", completed=True)
        repr_str = repr(todo)

        assert "Todo(id=1, title='Test todo', completed=True)" in repr_str

    def test_equality(self):
        """Test the __eq__ method."""
        todo1 = Todo(id=1, title="Test todo", completed=True)
        todo2 = Todo(id=1, title="Test todo", completed=True)
        todo3 = Todo(id=2, title="Different todo", completed=False)

        assert todo1 == todo2
        assert todo1 != todo3


class TestTodoList:
    def test_initial_state(self):
        """Test initial state of TodoList."""
        todo_list = TodoList()

        assert len(todo_list.todos) == 0
        assert todo_list.next_id == 1

    def test_add_todo(self):
        """Test adding a todo to the list."""
        todo_list = TodoList()
        todo = Todo(id=1, title="Test todo", completed=False)

        result = todo_list.add(todo)

        assert result == todo
        assert 1 in todo_list.todos
        assert todo_list.todos[1] == todo

    def test_add_duplicate_id_raises_error(self):
        """Test that adding a todo with duplicate ID raises ValueError."""
        todo_list = TodoList()
        todo1 = Todo(id=1, title="Test todo 1", completed=False)
        todo2 = Todo(id=1, title="Test todo 2", completed=False)

        todo_list.add(todo1)

        with pytest.raises(ValueError):
            todo_list.add(todo2)

    def test_get_existing_todo(self):
        """Test getting an existing todo."""
        todo_list = TodoList()
        todo = Todo(id=1, title="Test todo", completed=False)
        todo_list.add(todo)

        result = todo_list.get(1)

        assert result == todo

    def test_get_nonexistent_todo(self):
        """Test getting a nonexistent todo returns None."""
        todo_list = TodoList()

        result = todo_list.get(999)

        assert result is None

    def test_update_existing_todo(self):
        """Test updating an existing todo."""
        todo_list = TodoList()
        todo = Todo(id=1, title="Original title", completed=False)
        todo_list.add(todo)

        result = todo_list.update(1, title="Updated title", completed=True)

        assert result is not None
        assert result.title == "Updated title"
        assert result.completed is True

    def test_update_nonexistent_todo(self):
        """Test updating a nonexistent todo returns None."""
        todo_list = TodoList()

        result = todo_list.update(999, title="Updated title")

        assert result is None

    def test_remove_existing_todo(self):
        """Test removing an existing todo."""
        todo_list = TodoList()
        todo = Todo(id=1, title="Test todo", completed=False)
        todo_list.add(todo)

        result = todo_list.remove(1)

        assert result is True
        assert 1 not in todo_list.todos

    def test_remove_nonexistent_todo(self):
        """Test removing a nonexistent todo returns False."""
        todo_list = TodoList()

        result = todo_list.remove(999)

        assert result is False

    def test_list_all(self):
        """Test listing all todos."""
        todo_list = TodoList()
        todo1 = Todo(id=1, title="Test todo 1", completed=False)
        todo2 = Todo(id=2, title="Test todo 2", completed=True)
        todo_list.add(todo1)
        todo_list.add(todo2)

        result = todo_list.list_all()

        assert len(result) == 2
        assert todo1 in result
        assert todo2 in result

    def test_list_completed(self):
        """Test listing completed todos."""
        todo_list = TodoList()
        todo1 = Todo(id=1, title="Completed todo", completed=True)
        todo2 = Todo(id=2, title="Pending todo", completed=False)
        todo_list.add(todo1)
        todo_list.add(todo2)

        result = todo_list.list_completed()

        assert len(result) == 1
        assert result[0] == todo1

    def test_list_pending(self):
        """Test listing pending todos."""
        todo_list = TodoList()
        todo1 = Todo(id=1, title="Completed todo", completed=True)
        todo2 = Todo(id=2, title="Pending todo", completed=False)
        todo_list.add(todo1)
        todo_list.add(todo2)

        result = todo_list.list_pending()

        assert len(result) == 1
        assert result[0] == todo2

    def test_generate_next_id(self):
        """Test generating next unique ID."""
        todo_list = TodoList()

        first_id = todo_list.generate_next_id()
        second_id = todo_list.generate_next_id()

        assert first_id == 1
        assert second_id == 2
        assert todo_list.next_id == 3