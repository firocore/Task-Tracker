import os
import sys
import json
from enum import Enum
from datetime import datetime


TASK_FILE = "tasks.json"


class Commands(Enum):
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    MARK_PROCESS = "mark-in-progress"
    MARK_DONE = "mark-done"
    MARK_TODO = "mark-todo"
    LIST = "list"


class Statuses(Enum):
    IN_PROGRESS = "in-progress"
    DONE = "done"
    TODO = "todo"


def load_tasks():
    """Load tasks from JSON file."""
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []
        

def save_tasks(tasks: list[dict]):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)


def generate_task_id(tasks: list[dict]):
    return len(tasks) + 1


def add_task(description: str):
    tasks = load_tasks()

    task_id = generate_task_id(tasks)
    timestamp = datetime.now().isoformat()

    new_task = {
        "id": str(task_id),
        "description": description,
        "status": Statuses.TODO.value,
        "createdAt": timestamp,
        "updatedAt": timestamp
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully ID: {task_id}")


def delete_task(task_id: str):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    print(f"Task deleted successfully ID: {task_id}")


def update_task(task_id: str, new_description: str):
    tasks = load_tasks()

    timestamp = datetime.now().isoformat()

    for task in tasks:
        if task['id'] != task_id: continue

        task['description'] = new_description
        task['updatedAt'] = timestamp
        print(f"Task updated successfully ID: {task_id}")
        save_tasks(tasks)
        return 0
    
    print(f"Task not found ID: {task_id}")


def set_task_status(task_id: str, status: str):
    tasks = load_tasks()

    timestamp = datetime.now().isoformat()

    for task in tasks:
        if task['id'] != task_id: continue

        task['status'] = status
        task['updatedAt'] = timestamp
        print(f"Task updated successfully ID: {task_id}")
        save_tasks(tasks)
        return 0
    
    print(f"Task not found ID: {task_id}")


def list_tasks(filter_status=None):
    tasks = load_tasks()
    filtered_tasks = tasks if filter_status is None else [task for task in tasks if task['status'] == filter_status]
    if not filtered_tasks:
        print("No tasks found.")
        return
    for task in filtered_tasks:
        print(f"ID: {task['id']} | Description: {task['description']} | Status: {task['status']} | Created: {task['createdAt']} | Updated: {task['updatedAt']}")


def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        return 0
    
    command = sys.argv[1]
    count_argv = len(sys.argv)

    if command not in [cmd.value for cmd in Commands]:
        print("Invalid command.")
        return
    

    if command == Commands.ADD.value and count_argv == 3:
        add_task(sys.argv[2])

    elif command == Commands.DELETE.value and count_argv == 3:
        delete_task(sys.argv[2])

    elif command == Commands.UPDATE.value and count_argv == 4:
        update_task(sys.argv[2], sys.argv[3])

    elif command == Commands.MARK_DONE.value and count_argv == 3:
        set_task_status(sys.argv[2], Statuses.DONE.value)

    elif command == Commands.MARK_PROCESS.value and count_argv == 3:
        set_task_status(sys.argv[2], Statuses.IN_PROGRESS.value)

    elif command == Commands.MARK_TODO.value and count_argv == 3:
        set_task_status(sys.argv[2], Statuses.TODO.value)

    elif command == Commands.LIST.value and count_argv in [2, 3]:
        filter_status = None if count_argv == 2 else sys.argv[2]
        list_tasks(filter_status)
    

if __name__ == "__main__":
    main()