# Quickstart Guide: In-Memory Python Console Todo App (Phase I)

## Prerequisites
- Python 3.13 or higher
- UV package manager

## Setup
1. Clone the repository
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   uv sync
   ```

## Running the Application
```bash
uv run src/todo_app/cli/main.py
```

Or if the project is configured as a package:
```bash
uv run python -m todo_app.cli.main
```

## Available Commands
- `add "todo description"` - Add a new todo
- `view` - View all todos
- `update <id> "new description"` - Update a todo
- `delete <id>` - Delete a todo
- `complete <id>` - Mark a todo as complete
- `quit` or `exit` - Exit the application

## Example Usage
```
> add "Buy groceries"
Todo added with ID: 1

> add "Walk the dog"
Todo added with ID: 2

> view
ID  | Title           | Status
----|-----------------|--------
1   | Buy groceries   | Pending
2   | Walk the dog    | Pending

> complete 1
Todo 1 marked as complete

> view
ID  | Title           | Status
----|-----------------|--------
1   | Buy groceries   | Complete
2   | Walk the dog    | Pending

> quit
```

## Running Tests
```bash
uv run pytest
```

## Development
The application follows a clean architecture with:
- Models in `src/todo_app/models/`
- Repositories in `src/todo_app/repositories/`
- Services in `src/todo_app/services/`
- CLI interface in `src/todo_app/cli/`