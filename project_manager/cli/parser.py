"""Argparse setup with subcommands matching the assignment examples."""
import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pm",
        description="Project Management CLI — manage users, projects, and tasks.",
        epilog=(
            "Examples:\n"
            '  python main.py add-user --name "Alex"\n'
            '  python main.py add-project --user "Alex" --title "CLI Tool"\n'
            '  python main.py add-task --project "CLI Tool" '
            '--title "Implement add-task"'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    # add-user --name "Alex" [--email "..."]
    p = sub.add_parser("add-user", help="Create a new user")
    p.add_argument("--name", required=True, help="User name")
    p.add_argument("--email", default="", help="Optional email")

    # list-users
    sub.add_parser("list-users", help="List all users")

    # add-project --user "Alex" --title "CLI Tool"
    p = sub.add_parser("add-project", help="Create a project for a user")
    p.add_argument("--user", required=True, help="User name or id")
    p.add_argument("--title", required=True, help="Project title")
    p.add_argument("--description", default="")

    # list-projects [--user "Alex"]
    p = sub.add_parser("list-projects", help="List projects (optionally by user)")
    p.add_argument("--user", default=None)

    # add-task --project "CLI Tool" --title "Implement add-task" [--assignee "Alex"]
    p = sub.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--project", required=True, help="Project title or id")
    p.add_argument("--title", required=True, help="Task title")
    p.add_argument("--assignee", default=None, help="User name or id")
    p.add_argument("--description", default="")

    # list-tasks --project "CLI Tool"
    p = sub.add_parser("list-tasks", help="List tasks of a project")
    p.add_argument("--project", required=True, help="Project title or id")

    # complete-task --project "CLI Tool" --task "Implement add-task"
    p = sub.add_parser("complete-task", help="Mark a task as done")
    p.add_argument("--project", required=True, help="Project title or id")
    p.add_argument("--task", required=True, help="Task title or id")

    # search-projects "web"
    p = sub.add_parser("search-projects", help="Search projects by keyword")
    p.add_argument("keyword", help="Keyword to search")

    return parser