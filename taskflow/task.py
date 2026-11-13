from dataclasses import dataclass


@dataclass
class Task:
    """Represent one task in the task list."""

    task_id: int
    title: str
    completed: bool = False

    def to_dict(self):
        """Convert the task to a dictionary so it can be saved as JSON."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task object from a dictionary loaded from JSON."""
        return cls(
            task_id=int(data["task_id"]),
            title=str(data["title"]),
            completed=bool(data.get("completed", False)),
        )
