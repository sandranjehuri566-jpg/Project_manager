import sys

from project_manager.models import User, Project, Task
from project_manager.utils import (
    Storage, render_user, render_project, render_task,
)
from project_manager.cli.parser import build_parser

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
    desc = input("Description (optional): ").strip()
    p = Project(title, user.id, desc)
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
    tok = input("Assignee (blank for none): ").strip()
    if tok:
        user = storage.find_user(tok)
        if not user:
            print(f"Assignee '{tok}' not found.")
            return
        assignee_id = user.id
    desc = input("Description (optional): ").strip()
    t = Task(title, project.id, assignee_id, desc)
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
    tok = input("Which task (title or id): ").strip()
    task = project.find_task_by_title(tok) or project.find_task_by_id(tok)
    if not task:
        print(f"Task '{tok}' not found.")
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


def run_interactive():
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
            print("Invalid option.")
            continue

        storage.save()

    storage.save()
    return 0


def run_cli(argv):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 1

    storage = Storage(DATA_FILE)
    storage.load()

    if args.command == "add-user":
        if storage.find_user(args.name):
            print(f"User '{args.name}' already exists.")
            return 1
        u = User(args.name, args.email)
        storage.users.append(u)
        print(f"Created user {u.name} ({u.id})")

    elif args.command == "list-users":
        if not storage.users:
            print("No users yet.")
        else:
            for u in storage.users:
                render_user(u)

    elif args.command == "add-project":
        user = storage.find_user(args.user)
        if not user:
            print(f"User '{args.user}' not found.")
            return 1
        if storage.find_project(args.title):
            print(f"Project '{args.title}' already exists.")
            return 1
        p = Project(args.title, user.id, args.description)
        storage.projects.append(p)
        print(f"Project '{p.name}' created for {user.name}")

    elif args.command == "list-projects":
        projects = storage.projects
        if args.user:
            user = storage.find_user(args.user)
            if not user:
                print(f"User '{args.user}' not found.")
                return 1
            projects = [p for p in projects if p.owner_id == user.id]
        if not projects:
            print("No projects found.")
        else:
            for p in projects:
                owner = None
                for u in storage.users:
                    if u.id == p.owner_id:
                        owner = u
                        break
                render_project(p, owner.name if owner else "")

    elif args.command == "add-task":
        project = storage.find_project(args.project)
        if not project:
            print(f"Project '{args.project}' not found.")
            return 1
        assignee_id = None
        if args.assignee:
            user = storage.find_user(args.assignee)
            if not user:
                print(f"Assignee '{args.assignee}' not found.")
                return 1
            assignee_id = user.id
        t = Task(args.title, project.id, assignee_id, args.description)
        project.add_task(t)
        print(f"Task '{t.name}' added to {project.name} ({t.id})")

    elif args.command == "list-tasks":
        project = storage.find_project(args.project)
        if not project:
            print(f"Project '{args.project}' not found.")
            return 1
        if not project.tasks:
            print("No tasks.")
        else:
            for t in project.tasks:
                render_task(t)

    elif args.command == "complete-task":
        project = storage.find_project(args.project)
        if not project:
            print(f"Project '{args.project}' not found.")
            return 1
        task = project.find_task_by_title(args.task) or project.find_task_by_id(args.task)
        if not task:
            print(f"Task '{args.task}' not found.")
            return 1
        task.complete()
        print(f"Task '{task.name}' marked done.")

    elif args.command == "search-projects":
        kw = args.keyword.lower()
        hits = []
        for p in storage.projects:
            if kw in p.name.lower() or kw in p.description.lower():
                hits.append(p)
        if not hits:
            print("No matching projects.")
        else:
            for p in hits:
                owner = None
                for u in storage.users:
                    if u.id == p.owner_id:
                        owner = u
                        break
                render_project(p, owner.name if owner else "")

    storage.save()
    return 0


def main():
    if len(sys.argv) > 1:
        return run_cli(sys.argv[1:])
    return run_interactive()


if __name__ == "__main__":
    sys.exit(main())