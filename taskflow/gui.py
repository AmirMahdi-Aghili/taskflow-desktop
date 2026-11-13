import tkinter as tk
from tkinter import messagebox, ttk

from taskflow.manager import TaskManager


class TaskFlowApp(tk.Tk):
    """A small desktop window for managing everyday tasks."""

    def __init__(self):
        super().__init__()

        self.title("TaskFlow - Task Manager")
        self.geometry("620x480")
        self.minsize(520, 400)

        self.manager = TaskManager()
        self.task_ids = []

        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self):
        """Create the labels, input, task list, and action buttons."""
        container = ttk.Frame(self, padding=18)
        container.pack(fill="both", expand=True)

        title_label = ttk.Label(
            container,
            text="TaskFlow",
            font=("Segoe UI", 18, "bold"),
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            container,
            text="A simple place to keep track of your tasks.",
        )
        subtitle_label.pack(anchor="w", pady=(2, 14))

        input_frame = ttk.Frame(container)
        input_frame.pack(fill="x", pady=(0, 12))

        self.task_entry = ttk.Entry(input_frame)
        self.task_entry.pack(side="left", fill="x", expand=True)
        self.task_entry.bind("<Return>", self.add_task)

        add_button = ttk.Button(
            input_frame,
            text="Add task",
            command=self.add_task,
        )
        add_button.pack(side="left", padx=(8, 0))

        list_frame = ttk.Frame(container)
        list_frame.pack(fill="both", expand=True)

        self.task_list = tk.Listbox(
            list_frame,
            height=14,
            font=("Segoe UI", 10),
            activestyle="none",
            selectmode=tk.SINGLE,
        )
        self.task_list.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.task_list.yview,
        )
        scrollbar.pack(side="right", fill="y")
        self.task_list.configure(yscrollcommand=scrollbar.set)

        action_frame = ttk.Frame(container)
        action_frame.pack(fill="x", pady=(12, 0))

        complete_button = ttk.Button(
            action_frame,
            text="Mark completed",
            command=self.complete_task,
        )
        complete_button.pack(side="left")

        delete_button = ttk.Button(
            action_frame,
            text="Delete selected",
            command=self.delete_task,
        )
        delete_button.pack(side="left", padx=(8, 0))

        self.status_label = ttk.Label(container, text="")
        self.status_label.pack(anchor="w", pady=(10, 0))

    def refresh_tasks(self):
        """Refresh the visible list using the latest saved task data."""
        self.task_list.delete(0, tk.END)
        self.task_ids.clear()

        tasks = self.manager.get_tasks()
        for task in tasks:
            marker = "[Done]" if task.completed else "[     ]"
            self.task_list.insert(tk.END, f"{marker}  {task.title}")
            self.task_ids.append(task.task_id)

        remaining = sum(not task.completed for task in tasks)
        self.status_label.configure(
            text=f"{len(tasks)} task(s) total  |  {remaining} remaining"
        )

    def add_task(self, event=None):
        """Add the text from the input field as a new task."""
        title = self.task_entry.get()
        try:
            self.manager.add_task(title)
        except ValueError as error:
            messagebox.showwarning("Task not added", str(error), parent=self)
            return

        self.task_entry.delete(0, tk.END)
        self.refresh_tasks()
        self.task_entry.focus_set()

    def get_selected_task_id(self):
        """Return the ID of the selected task, or None if nothing is selected."""
        selection = self.task_list.curselection()
        if not selection:
            messagebox.showinfo(
                "No task selected",
                "Please select a task first.",
                parent=self,
            )
            return None

        selected_index = selection[0]
        return self.task_ids[selected_index]

    def complete_task(self):
        """Mark the selected task as completed."""
        task_id = self.get_selected_task_id()
        if task_id is None:
            return

        self.manager.mark_completed(task_id)
        self.refresh_tasks()

    def delete_task(self):
        """Delete the selected task after asking for confirmation."""
        task_id = self.get_selected_task_id()
        if task_id is None:
            return

        confirmed = messagebox.askyesno(
            "Delete task",
            "Are you sure you want to delete this task?",
            parent=self,
        )
        if confirmed:
            self.manager.delete_task(task_id)
            self.refresh_tasks()
