"""User entity — one user can own many projects."""
from .base import BaseEntity


class User(BaseEntity):
    def __init__(self, name: str, email: str = ""):
        super().__init__(name)
        self.email = email

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        u = cls(data["name"], data.get("email", ""))
        u._id = data["id"]
        u.created_at = data["created_at"]
        return u

    def __repr__(self):
        return f"<User {self.name}>"