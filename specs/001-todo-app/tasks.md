# Tasks: In-Memory Python Console Todo App (Phase I)

## Overview

Implementation of a command-line todo application in Python that operates entirely in memory with no external storage. The application provides core todo management features (add, view, update, delete, mark complete) through a CLI interface. The architecture follows a layered approach with clear separation between presentation (CLI), application logic (services), and domain models (entities).

## Dependencies

- User Story 2 (View Todos) requires User Story 1 (Add Todo) to have basic functionality for testing
- User Stories 3-5 (Update, Delete, Mark Complete) require User Story 1 (Add Todo) to create test data

## Parallel Execution Examples

- Within each user story, model and repository implementations can often run in parallel [P]
- Unit tests for different components can run in parallel [P]
- CLI command implementations can run in parallel once services are available [P]

## Implementation Strategy

- MVP: User Story 1 (Add Todo) with basic CLI interface
- Incremental delivery: Add one user story at a time with associated tests
- Each user story should be independently testable

---

## Phase 1: Setup

- [X] T001 Create project structure per implementation plan in src/todo_app/
- [X] T002 Create pyproject.toml with Python 3.13+ requirement and pytest dependency
- [X] T003 Create directory structure: src/todo_app/{models,repositories,services,cli}/
- [X] T004 Create __init__.py files in all directories
- [X] T005 Set up basic testing structure in tests/

## Phase 2: Foundational Components

- [X] T010 [P] Implement Todo model in src/todo_app/models/todo.py
- [X] T011 [P] Implement TodoList collection in src/todo_app/models/todo.py
- [X] T012 [P] Implement TodoRepository in src/todo_app/repositories/todo_repository.py
- [X] T013 [P] Implement TodoService in src/todo_app/services/todo_service.py
- [X] T014 [P] Implement custom exception classes for error handling
- [X] T015 [P] Create basic CLI framework in src/todo_app/cli/main.py
- [X] T016 [P] Create command parsing utilities in src/todo_app/cli/commands.py

## Phase 3: User Story 1 - Add New Todo (Priority: P1)

Goal: A user wants to add a new task to their todo list by typing a command in the console. The user enters the todo description and the system stores it in memory with a unique identifier.

Independent Test: Can be fully tested by running the application, entering an "add" command with a todo description, and verifying the todo appears in the list.

- [X] T020 [US1] Implement add_todo method in TodoService with validation
- [X] T021 [US1] Implement add command handler in src/todo_app/cli/commands.py
- [X] T022 [US1] Connect add command to service layer in CLI
- [X] T023 [US1] Create unit tests for Todo model and add functionality
- [X] T024 [US1] Create unit tests for TodoService add functionality
- [X] T025 [US1] Create integration tests for add command flow
- [X] T026 [US1] Handle error case: empty todo description
- [X] T027 [US1] Verify unique ID generation works correctly

## Phase 4: User Story 2 - View Todos (Priority: P1)

Goal: A user wants to see all their current todos displayed in the console. The user can view all todos or filter them by completion status.

Independent Test: Can be fully tested by adding a few todos and then viewing them to confirm they appear correctly in the console.

- [X] T030 [US2] Implement view_todos method in TodoService
- [X] T031 [US2] Implement view command handler in src/todo_app/cli/commands.py
- [X] T032 [US2] Connect view command to service layer in CLI
- [X] T033 [US2] Format output as table with ID, title, and completion status
- [X] T034 [US2] Implement filtering for completed/pending todos
- [X] T035 [US2] Create unit tests for view functionality
- [X] T036 [US2] Create integration tests for view command flow
- [X] T037 [US2] Handle error case: no todos exist

## Phase 5: User Story 3 - Mark Todo as Complete (Priority: P2)

Goal: A user wants to mark a specific todo as completed by referencing its ID. The system updates the todo's status in memory.

Independent Test: Can be fully tested by adding a todo, marking it as complete, and then viewing todos to confirm the status has changed.

- [X] T040 [US3] Implement mark_complete method in TodoService with validation
- [X] T041 [US3] Implement complete command handler in src/todo_app/cli/commands.py
- [X] T042 [US3] Connect complete command to service layer in CLI
- [X] T043 [US3] Create unit tests for mark_complete functionality
- [X] T044 [US3] Create integration tests for complete command flow
- [X] T045 [US3] Handle error case: invalid/non-existent todo ID
- [X] T046 [US3] Handle edge case: marking already completed todo

## Phase 6: User Story 4 - Update Todo (Priority: P2)

Goal: A user wants to modify the text of an existing todo by referencing its ID. The system updates the todo's text in memory.

Independent Test: Can be fully tested by adding a todo, updating its text, and then viewing todos to confirm the text has changed.

- [X] T050 [US4] Implement update_todo method in TodoService with validation
- [X] T051 [US4] Implement update command handler in src/todo_app/cli/commands.py
- [X] T052 [US4] Connect update command to service layer in CLI
- [X] T053 [US4] Create unit tests for update functionality
- [X] T054 [US4] Create integration tests for update command flow
- [X] T055 [US4] Handle error case: invalid/non-existent todo ID
- [X] T056 [US4] Handle error case: empty new description

## Phase 7: User Story 5 - Delete Todo (Priority: P2)

Goal: A user wants to remove a specific todo from their list by referencing its ID. The system removes the todo from memory.

Independent Test: Can be fully tested by adding a todo, deleting it, and then viewing todos to confirm it has been removed.

- [X] T060 [US5] Implement delete_todo method in TodoService with validation
- [X] T061 [US5] Implement delete command handler in src/todo_app/cli/commands.py
- [X] T062 [US5] Connect delete command to service layer in CLI
- [X] T063 [US5] Create unit tests for delete functionality
- [X] T064 [US5] Create integration tests for delete command flow
- [X] T065 [US5] Handle error case: invalid/non-existent todo ID
- [X] T066 [US5] Handle edge case: ID counter behavior after deletion

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T070 Implement graceful exit functionality for quit/exit commands
- [X] T071 Add comprehensive error handling for invalid commands
- [X] T072 Implement command parsing for malformed input
- [X] T073 Add support for special characters in todo text
- [X] T074 Create end-to-end integration tests
- [X] T075 Refine user interface and error messages for better UX
- [X] T076 Update pyproject.toml with proper entry points for CLI
- [X] T077 Document all implemented functionality
- [X] T078 Run complete test suite to verify all features work together
- [X] T079 Test example usage scenarios from quickstart guide