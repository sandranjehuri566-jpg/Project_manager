"""Task entity — belongs to a project, can be assigned to a user."""
from enum import Enum
from .base import BaseEntity


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(BaseEntity):
    def __init__(self, title: str, project_id: str,
                 assignee_id: str | None = None, description: str = ""):
        super().__init__(title)
        self.project_id = project_id
        self.assignee_id = assignee_id
        self.description = description
        self.status = TaskStatus.TODO

    def complete(self) -> None:
        self.status = TaskStatus.DONE

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "project_id": self.project_id,
            "assignee_id": self.assignee_id,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        t = cls(data["name"], data["project_id"],
                data.get("assignee_id"), data.get("description", ""))
        t._id = data["id"]
        t.created_at = data["created_at"]
        t.status = TaskStatus(data["status"])
        return t

    def __repr__(self):
        return f"<Task {self.name} [{self.status.value}]>"