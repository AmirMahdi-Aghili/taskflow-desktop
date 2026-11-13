from taskflow.storage import JsonStorage
from taskflow.task import Task


class TaskManager:
    """Handle the task operations used by the desktop interface."""

    def __init__(self, storage=None):
        self.storage = storage if storage is not None else JsonStorage()
        self.tasks = self.storage.load_tasks()
        self.next_id = max((task.task_id for task in self.tasks), default=0) + 1

    def get_tasks(self):
        """Return the current tasks."""
        return list(self.tasks)

    def add_task(self, title):
        """Create and save a task. Empty titles are not allowed."""
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")

        task = Task(task_id=self.next_id, title=title)
        self.tasks.append(task)
        self.next_id += 1
        self.storage.save_tasks(self.tasks)
        return task

    def mark_completed(self, task_id):
        """Mark a task as completed. Return False if it does not exist."""
        for task in self.tasks:
            if task.task_id == task_id:
                task.completed = True
                self.storage.save_tasks(self.tasks)
                return True
        return False

    def delete_task(self, task_id):
        """Delete a task. Return False if it does not exist."""
        for index, task in enumerate(self.tasks):
            if task.task_id == task_id:
                del self.tasks[index]
                self.storage.save_tasks(self.tasks)
                return True
        return False
