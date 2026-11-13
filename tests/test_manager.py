import tempfile
import unittest
from pathlib import Path

from taskflow.manager import TaskManager
from taskflow.storage import JsonStorage


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        data_file = Path(self.temp_dir.name) / "tasks.json"
        self.manager = TaskManager(storage=JsonStorage(data_file))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_task(self):
        task = self.manager.add_task("Study Python")
        self.assertEqual(task.title, "Study Python")
        self.assertEqual(len(self.manager.get_tasks()), 1)

    def test_reject_empty_task(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("   ")

    def test_mark_task_completed(self):
        task = self.manager.add_task("Read a chapter")
        result = self.manager.mark_completed(task.task_id)
        self.assertTrue(result)
        self.assertTrue(self.manager.get_tasks()[0].completed)

    def test_delete_task(self):
        task = self.manager.add_task("Clean the desk")
        result = self.manager.delete_task(task.task_id)
        self.assertTrue(result)
        self.assertEqual(self.manager.get_tasks(), [])

    def test_tasks_are_saved_and_loaded(self):
        self.manager.add_task("Keep learning Git")
        new_manager = TaskManager(storage=self.manager.storage)
        self.assertEqual(new_manager.get_tasks()[0].title, "Keep learning Git")


if __name__ == "__main__":
    unittest.main()
