"""Project Management CLI - interactive menu version."""
import sys

from project_manager.models import User, Project, Task
from project_manager.utils import (
    Storage, render_user, render_project, render_task,
)

DATA_FILE = "project_manager/data/data.json"


def show_menu():
    print()
    print("=== Project Management CLI ===")
    print("1. Add user")
    print("2. List users")
    print("3. Add project")
    print("4. List projects")
    print("5. Add task")
    print("6. List tasks")
    print("7. Complete task")
    print("8. Search projects")
    print("9. Exit")


def add_user(storage):
    name = input("User name: ").strip()
    if not name:
        print("Name required.")
        return

    if storage.find_user(name):
        print(f"User '{name}' already exists.")
        return

    email = input("Email (optional): ").strip()
    u = User(name, email)
    storage.users.append(u)
    print(f"Created user {u.name} ({u.id})")


def list_users(storage):
    if not storage.users:
        print("No users yet.")
        return

    for u in storage.users:
        render_user(u)


def add_project(storage):
    if not storage.users:
        print("Create a user first.")
        return

    token = input("Which user (name or id): ").strip()
    user = storage.find_user(token)
    if not user:
        print(f"User '{token}' not found.")
        return

    title = input("Project title: ").strip()
    if not title:
        print("Title required.")
        return

    if storage.find_project(title):
        print(f"Project '{title}' already exists.")
        return

    description = input("Description (optional): ").strip()
    p = Project(title, user.id, description)
    storage.projects.append(p)
    print(f"Project '{p.name}' created for {user.name}")


def list_projects(storage):
    token = input("Filter by user (blank for all): ").strip()

    projects = storage.projects
    if token:
        user = storage.find_user(token)
        if not user:
            print(f"User '{token}' not found.")
            return
        projects = [p for p in projects if p.owner_id == user.id]

    if not projects:
        print("No projects found.")
        return

    for p in projects:
        owner = None
        for u in storage.users:
            if u.id == p.owner_id:
                owner = u
                break
        render_project(p, owner.name if owner else "")


def add_task(storage):
    if not storage.projects:
        print("Create a project first.")
        return

    token = input("Which project (name or id): ").strip()
    project = storage.find_project(token)
    if not project:
        print(f"Project '{token}' not found.")
        return

    title = input("Task title: ").strip()
    if not title:
        print("Title required.")
        return

    assignee_id = None
    assignee_token = input("Assignee (blank for none): ").strip()
    if assignee_token:
        user = storage.find_user(assignee_token)
        if not user:
            print(f"Assignee '{assignee_token}' not found.")
            return
        assignee_id = user.id

    description = input("Description (optional): ").strip()
    t = Task(title, project.id, assignee_id, description)
    project.add_task(t)
    print(f"Task '{t.name}' added to {project.name} ({t.id})")


def list_tasks(storage):
    token = input("Which project (name or id): ").strip()
    project = storage.find_project(token)
    if not project:
        print(f"Project '{token}' not found.")
        return

    if not project.tasks:
        print("No tasks.")
        return

    for t in project.tasks:
        render_task(t)


def complete_task(storage):
    token = input("Which project (name or id): ").strip()
    project = storage.find_project(token)
    if not project:
        print(f"Project '{token}' not found.")
        return

    task_token = input("Which task (title or id): ").strip()
    task = project.find_task_by_title(task_token)
    if not task:
        task = project.find_task_by_id(task_token)
    if not task:
        print(f"Task '{task_token}' not found in project '{project.name}'.")
        return

    task.complete()
    print(f"Task '{task.name}' marked done.")


def search_projects(storage):
    kw = input("Keyword: ").strip().lower()
    if not kw:
        print("Keyword required.")
        return

    hits = []
    for p in storage.projects:
        if kw in p.name.lower() or kw in p.description.lower():
            hits.append(p)

    if not hits:
        print("No matching projects.")
        return

    for p in hits:
        owner = None
        for u in storage.users:
            if u.id == p.owner_id:
                owner = u
                break
        render_project(p, owner.name if owner else "")


def main():
    storage = Storage(DATA_FILE)
    storage.load()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_user(storage)
        elif choice == "2":
            list_users(storage)
        elif choice == "3":
            add_project(storage)
        elif choice == "4":
            list_projects(storage)
        elif choice == "5":
            add_task(storage)
        elif choice == "6":
            list_tasks(storage)
        elif choice == "7":
            complete_task(storage)
        elif choice == "8":
            search_projects(storage)
        elif choice == "9":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Try again.")
            continue

        storage.save()

    storage.save()
    return 0


if __name__ == "__main__":
    (main()) 