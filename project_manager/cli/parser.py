import argparse


def build_parser():
    parser = argparse.ArgumentParser(
        prog="pm",
        description="Project Management CLI",
        epilog=(
            "examples:\n"
            '  python main.py add-user --name "Alex"\n'
            '  python main.py add-project --user "Alex" --title "CLI Tool"\n'
            '  python main.py add-task --project "CLI Tool" --title "write docs"'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    p = sub.add_parser("add-user", help="create a user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", default="")

    sub.add_parser("list-users", help="list users")

    p = sub.add_parser("add-project", help="create a project for a user")
    p.add_argument("--user", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", default="")

    p = sub.add_parser("list-projects", help="list projects")
    p.add_argument("--user", default=None)

    p = sub.add_parser("add-task", help="add a task to a project")
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--assignee", default=None)
    p.add_argument("--description", default="")

    p = sub.add_parser("list-tasks", help="list tasks of a project")
    p.add_argument("--project", required=True)

    p = sub.add_parser("complete-task", help="mark a task done")
    p.add_argument("--project", required=True)
    p.add_argument("--task", required=True)

    p = sub.add_parser("search-projects", help="search projects")
    p.add_argument("keyword")

    return parser