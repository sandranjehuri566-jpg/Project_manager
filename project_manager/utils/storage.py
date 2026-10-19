"""JSON persistence layer with error handling."""
import json
import os

from project_manager.models import User, Project


class Storage:
    """Loads and saves User/Project objects to a JSON file."""

    def __init__(self, path: str):
        self.path = path
        self.users: list[User] = []
        self.projects: list[Project] = []

    def load(self) -> None:
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)
            self.users = [User.from_dict(d) for d in data.get("users", [])]
            self.projects = [Project.from_dict(d) for d in data.get("projects", [])]
        except (json.JSONDecodeError, KeyError) as exc:
            print(f"[warn] Could not load data: {exc}")

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        payload = {
            "users": [u.to_dict() for u in self.users],
            "projects": [p.to_dict() for p in self.projects],
        }
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
        except OSError as exc:
            print(f"[error] Could not save data: {exc}")

    def find_user(self, token: str):
        return next(
            (u for u in self.users
             if u.id == token or u.name.lower() == token.lower()),
            None,
        )

    def find_project(self, token: str):
        return next(
            (p for p in self.projects
             if p.id == token or p.name.lower() == token.lower()),
            None,
        )