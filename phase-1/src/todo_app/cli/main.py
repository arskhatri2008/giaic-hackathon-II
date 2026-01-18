#!/usr/bin/env python3
"""
Main application entry point for the todo CLI application.
"""

import sys
from typing import List
from ..services.todo_service import TodoService
from ..repositories.todo_repository import TodoRepository
from .commands import TodoCLI


def main():
    """
    Main entry point for the todo CLI application.
    """
    # Create the service and CLI components
    repository = TodoRepository()
    service = TodoService(repository)
    cli = TodoCLI(service)

    print("Welcome to the Todo App!")
    print("Available commands: add, view, update, delete, complete, quit")

    # Start the CLI loop
    while True:
        try:
            user_input = input("> ").strip()

            if not user_input:
                continue

            # Split the input into command and arguments
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            # Handle the command
            if command == "quit" or command == "exit":
                print("Goodbye!")
                break
            elif hasattr(cli, f"handle_{command}"):
                handler = getattr(cli, f"handle_{command}")
                result = handler(args)
                if result:
                    print(result)
            else:
                print(f"Unknown command: {command}. Available commands: add, view, update, delete, complete, quit")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()