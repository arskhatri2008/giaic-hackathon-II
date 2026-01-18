# Data Model: In-Memory Python Console Todo App (Phase I)

## Todo Entity

### Fields
- **id** (int): Unique identifier for the todo item, auto-generated and immutable
- **title** (str): The text description of the todo item, required field
- **completed** (bool): Boolean indicating whether the todo is completed, defaults to False

### Validation Rules
- **title** must not be empty or contain only whitespace
- **id** must be unique within the application session
- **completed** can only be True or False

### State Transitions
- **Incomplete → Complete**: When the mark_complete operation is performed
- **Complete → Incomplete**: When the mark_incomplete operation is performed (optional feature)

## TodoList Collection

### Properties
- **todos** (dict[int, Todo]): Dictionary mapping todo IDs to Todo objects for O(1) lookup
- **next_id** (int): Counter for generating unique IDs, starts at 1 and increments

### Operations
- **add(todo)**: Add a new todo to the collection with a unique ID
- **get(id)**: Retrieve a todo by its ID
- **update(id, **kwargs)**: Update properties of an existing todo
- **remove(id)**: Remove a todo from the collection
- **list_all()**: Return all todos in the collection
- **list_completed()**: Return only completed todos
- **list_pending()**: Return only pending todos

## Relationships
- TodoList contains multiple Todo entities
- Each Todo has a unique relationship to its containing TodoList via the ID