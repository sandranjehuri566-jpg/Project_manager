"""Pretty-printing helpers using `rich`."""
from rich.console import Console

console = Console()


def render_user(user) -> None:
    console.print(
        f"[bold cyan]{user.name}[/]  email={user.email or '-'}  id={user.id}"
    )


def render_project(project, owner_name: str = "") -> None:
    console.print(
        f"[bold green]{project.name}[/]  owner={owner_name or project.owner_id}  "
        f"tasks={len(project.tasks)}"
    )


def render_task(task) -> None:
    color = {"todo": "yellow", "in_progress": "blue", "done": "green"}[task.status.value]
    console.print(
        f"  [{color}]{task.status.value:>11}[/]  {task.name}  id={task.id}"
    )