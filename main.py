"""Entry point for the Project Management CLI."""
import sys

from project_manager.cli import build_parser
from project_manager.models import User, Project, Task
from project_manager.utils import (
    Storage, render_user, render_project, render_task,
)

DATA_FILE = "project_manager/data/data.json"


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

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
        for p in projects:
            owner = next((u for u in storage.users if u.id == p.owner_id), None)
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
        for t in project.tasks:
            render_task(t)

    elif args.command == "complete-task":
        project = storage.find_project(args.project)
        if not project:
            print(f"Project '{args.project}' not found.")
            return 1
        task = project.find_task_by_title(args.task) or project.find_task_by_id(args.task)
        if not task:
            print(f"Task '{args.task}' not found in project '{project.name}'.")
            return 1
        task.complete()
        print(f"Task '{task.name}' marked done.")

    elif args.command == "search-projects":
        kw = args.keyword.lower()
        hits = [
            p for p in storage.projects
            if kw in p.name.lower() or kw in p.description.lower()
        ]
        if not hits:
            print("No matching projects.")
        for p in hits:
            owner = next((u for u in storage.users if u.id == p.owner_id), None)
            render_project(p, owner.name if owner else "")

    storage.save()
    return 0


if __name__ == "__main__":
    sys.exit(main())