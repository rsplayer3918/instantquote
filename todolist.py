from rich.console import Console
from rich.table import Table
import json
import os
import time
from getpass import getpass

PASSWORD = "root123"
TASK_FILE = "tasks.json"

console = Console()


def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_tasks(tasks):
    with console.status("Saving...", spinner="dots"):
        with open(TASK_FILE, 'w') as f:
            json.dump(tasks, f, indent=2)
        time.sleep(1)


def add_task(tasks):
    console.print("[bold green]Add a new task[/bold green]")
    title = console.input("Task: ")
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)


def list_tasks(tasks):
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return
    table = Table(title="Your Tasks")
    table.add_column("ID", justify="right")
    table.add_column("Task")
    table.add_column("Status")
    for i, task in enumerate(tasks, 1):
        status = "[green]Done[/green]" if task.get("done") else "[yellow]Pending[/yellow]"
        table.add_row(str(i), task.get("title", ""), status)
    console.print(table)


def mark_done(tasks):
    if not tasks:
        console.print("[yellow]No tasks to mark.[/yellow]")
        return
    list_tasks(tasks)
    idx = console.input("Mark which task as done? ")
    if not idx.isdigit():
        console.print("[red]Invalid input[/red]")
        return
    idx = int(idx) - 1
    if 0 <= idx < len(tasks):
        tasks[idx]["done"] = True
        save_tasks(tasks)
    else:
        console.print("[red]Invalid task number[/red]")


def delete_task(tasks):
    if not tasks:
        console.print("[yellow]No tasks to delete.[/yellow]")
        return
    list_tasks(tasks)
    idx = console.input("Delete which task? ")
    if not idx.isdigit():
        console.print("[red]Invalid input[/red]")
        return
    idx = int(idx) - 1
    if 0 <= idx < len(tasks):
        tasks.pop(idx)
        save_tasks(tasks)
    else:
        console.print("[red]Invalid task number[/red]")


def main():
    console.print("[bold magenta]Welcome to Animated To-Do[/bold magenta]")
    for _ in range(3):
        password = getpass("Enter password: ")
        with console.status("[yellow]Checking...[/yellow]", spinner="dots"):
            time.sleep(1)
        if password == PASSWORD:
            break
        console.print("[red]Wrong password![/red]")
    else:
        console.print("[red]Too many attempts![/red]")
        return

    tasks = load_tasks()

    while True:
        console.print("\n[bold cyan]Menu[/bold cyan]")
        console.print("1. Add Task")
        console.print("2. List Tasks")
        console.print("3. Mark Task as Done")
        console.print("4. Delete Task")
        console.print("5. Exit")
        choice = console.input("Choose an option: ")
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            save_tasks(tasks)
            console.print("[bold green]Goodbye![/bold green]")
            break
        else:
            console.print("[red]Invalid choice[/red]")


if __name__ == "__main__":
    main()
