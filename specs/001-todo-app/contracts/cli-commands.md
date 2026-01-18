# CLI Command Contracts: In-Memory Python Console Todo App (Phase I)

## Command Interface Definition

### Add Todo Command
- **Command**: `add "todo description"`
- **Input**: String containing the todo description
- **Output**: Success message with assigned ID or error message
- **Errors**: Empty description, invalid format
- **Preconditions**: Description is not empty or whitespace-only
- **Postconditions**: New todo exists in memory with unique ID

### View Todos Command
- **Command**: `view`
- **Input**: None
- **Output**: Formatted table/list of all todos with ID, title, and completion status
- **Errors**: None
- **Preconditions**: None
- **Postconditions**: Todos are displayed to user

### Update Todo Command
- **Command**: `update <id> "new description"`
- **Input**: Integer ID and new description string
- **Output**: Success message or error message
- **Errors**: Invalid ID, empty description, non-existent ID
- **Preconditions**: ID exists, description is not empty
- **Postconditions**: Todo description is updated in memory

### Delete Todo Command
- **Command**: `delete <id>`
- **Input**: Integer ID
- **Output**: Success message or error message
- **Errors**: Invalid ID, non-existent ID
- **Preconditions**: ID exists
- **Postconditions**: Todo is removed from memory

### Mark Complete Command
- **Command**: `complete <id>`
- **Input**: Integer ID
- **Output**: Success message or error message
- **Errors**: Invalid ID, non-existent ID
- **Preconditions**: ID exists
- **Postconditions**: Todo completion status is set to True

### Quit Command
- **Command**: `quit` or `exit`
- **Input**: None
- **Output**: Application termination
- **Errors**: None
- **Preconditions**: None
- **Postconditions**: Application terminates gracefully