"""Project entity — owned by a user, contains many tasks."""
from .base import BaseEntity
from .task import Task


class Project(BaseEntity):
    def __init__(self, name: str, owner_id: str, description: str = ""):
        super().__init__(name)
        self.owner_id = owner_id
        self.description = description
        self._tasks: list[Task] = []

    @property
    def tasks(self) -> list[Task]:
        return list(self._tasks)

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def find_task_by_title(self, title: str) -> Task | None:
        return next(
            (t for t in self._tasks if t.name.lower() == title.lower()),
            None,
        )

    def find_task_by_id(self, task_id: str) -> Task | None:
        return next((t for t in self._tasks if t.id == task_id), None)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner_id,
            "description": self.description,
            "tasks": [t.to_dict() for t in self._tasks],
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        p = cls(data["name"], data["owner_id"], data.get("description", ""))
        p._id = data["id"]
        p.created_at = data["created_at"]
        for td in data.get("tasks", []):
            p._tasks.append(Task.from_dict(td))
        return p

    def __repr__(self):
        return f"<Project {self.name} tasks={len(self._tasks)}>"