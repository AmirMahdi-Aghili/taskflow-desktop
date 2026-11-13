# TaskFlow Desktop

A small Python desktop application for keeping track of everyday tasks. It opens in its own Windows-style window and stores tasks locally in a JSON file.

## Features

- Add a task
- View all tasks
- Mark a task as completed
- Delete a task
- Save tasks automatically in `data/tasks.json`
- Restore saved tasks the next time the app opens

## Requirements

- Python 3.10 or newer
- Tkinter (usually included with the standard Python installer on Windows)

No third-party packages are required.

## Run the application

Open a terminal in the project folder and run:

```bash
python -m taskflow.main
```

## Run tests

```bash
python -m unittest discover -v
```

## Project structure

```text
TaskFlow-Desktop/
├── taskflow/
│   ├── __init__.py
│   ├── main.py
│   ├── task.py
│   ├── storage.py
│   ├── manager.py
│   └── gui.py
├── tests/
│   ├── __init__.py
│   └── test_manager.py
├── data/
│   └── .gitkeep
├── .gitignore
├── LICENSE
├── README.md
└── README_FA.md
```

## License

This project is licensed under the MIT License. See `LICENSE` for details.
