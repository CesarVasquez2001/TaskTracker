import sys
import json
import os
from datetime import datetime


# File to store tasks
TASKS_FILE = "./tasks.json"


def load_tasks():
    """Load tasks from the JSON file or initialize if not present."""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            # Handle corrupted or empty file
            print("Corrupted or empty tasks file. Reinitializing...")
            return []
    else:
        return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)



def generate_id(tasks):
    """Generate a unique ID for a new task."""
    if tasks:
        return max(task["id"] for task in tasks) + 1
    return 1


def add_task(description):
    """Add a new task."""
    tasks = load_tasks()
    task = {
        "id": generate_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task['id']})")


def update_task(task_id, new_description):
    """Update a task's description."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task (ID: {task_id}) updated successfully")
            return
    print(f"Task (ID: {task_id}) not found")


def delete_task(task_id):
    """Delete a task by ID."""
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task (ID: {task_id}) deleted successfully")


def mark_status(task_id, status):
    """Mark a task as in-progress or done."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task (ID: {task_id}) marked as {status}")
            return
    print(f"Task (ID: {task_id}) not found")


def list_tasks(status=None):
    """List tasks, optionally filtering by status."""
    tasks = load_tasks()
    filtered_tasks = tasks if status is None else [task for task in tasks if task["status"] == status]
    if not filtered_tasks:
        print("No tasks found.")
        return
    for task in filtered_tasks:
        print(f"[ID: {task['id']}] {task['description']} (Status: {task['status']})")


def main():
    """Main entry point for the CLI."""
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [<args>]")
        return

    command = sys.argv[1]
    if command == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif command == "update" and len(sys.argv) > 3:
        update_task(int(sys.argv[2]), " ".join(sys.argv[3:]))
    elif command == "delete" and len(sys.argv) > 2:
        delete_task(int(sys.argv[2]))
    elif command in ("mark-in-progress", "mark-done") and len(sys.argv) > 2:
        status = "in-progress" if command == "mark-in-progress" else "done"
        mark_status(int(sys.argv[2]), status)
    elif command == "list":
        status = None if len(sys.argv) == 2 else sys.argv[2]
        list_tasks(status)
    else:
        print("Invalid command or arguments")


if __name__ == "__main__":
    main()
