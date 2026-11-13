import json
from pathlib import Path

from taskflow.task import Task


class JsonStorage:
    """Load and save tasks in a JSON file."""

    def __init__(self, file_path=None):
        if file_path is None:
            project_root = Path(__file__).resolve().parent.parent
            file_path = project_root / "data" / "tasks.json"

        self.file_path = Path(file_path)

    def load_tasks(self):
        """Return all saved tasks, or an empty list for a new project."""
        if not self.file_path.exists():
            return []

        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError("The tasks.json file contains invalid JSON.") from error

        if not isinstance(data, list):
            raise ValueError("The tasks.json file must contain a JSON list.")

        return [Task.from_dict(item) for item in data]

    def save_tasks(self, tasks):
        """Save the supplied tasks to the JSON file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        data = [task.to_dict() for task in tasks]
        self.file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=4),
            encoding="utf-8",
        )
