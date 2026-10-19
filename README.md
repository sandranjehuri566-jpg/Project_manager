# Project Management CLI

A Python command-line tool to manage users, projects, and tasks with JSON persistence.

**Author:** Sandra Njehuri

---

## Features

- Create and list users
- Add projects per user (one-to-many)
- Add tasks to projects with optional assignees (many-to-many)
- Mark tasks complete
- Search projects by keyword
- JSON persistence with corruption-safe loading
- Pretty terminal output via `rich`
- Human-friendly timestamps via `python-dateutil`

---

## Setup

```bash
git clone https://github.com/YOUR-USERNAME/project-manager-cli.git
cd project-manager-cli
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py --help
python main.py add-user --name "Alex" --email "alex@example.com"
python main.py list-users
python main.py add-project --user "Alex" --title "CLI Tool"
python main.py list-projects --user "Alex"
python main.py add-task --project "CLI Tool" --title "Implement add-task" --assignee "Alex"
python main.py list-tasks --project "CLI Tool"
python main.py complete-task --project "CLI Tool" --task "Implement add-task"
python main.py search-projects cli
```

`--user`, `--project`, `--assignee`, and `--task` accept **either an id or a name/title**.

---

## Commands

| Command | Required flags | Optional flags |
|---|---|---|
| `add-user` | `--name` | `--email` |
| `list-users` | — | — |
| `add-project` | `--user`, `--title` | `--description` |
| `list-projects` | — | `--user` |
| `add-task` | `--project`, `--title` | `--assignee`, `--description` |
| `list-tasks` | `--project` | — |
| `complete-task` | `--project`, `--task` | — |
| `search-projects` | `keyword` | — |

---

## Project Structure

```
project_manager/
├── main.py                    # CLI dispatcher
├── requirements.txt
├── Pipfile
├── project_manager/
│   ├── models/                # BaseEntity, User, Project, Task
│   ├── cli/                   # argparse subcommands
│   ├── utils/                 # JSON storage, rich display
│   └── data/                  # data.json (runtime, gitignored)
└── tests/                     # pytest unit tests
```

**OOP design:** `BaseEntity` (abstract) → `User`, `Project`, `Task`. A `Project` *has many* `Task`s (composition). A `Project` *belongs to* a `User` (one-to-many via `owner_id`).

---

## Testing

```bash
pytest -q
```

7 tests covering model roundtrips, task completion, and safe JSON loading.

---

## Known Issues

- Timestamps use naive UTC (no timezone info).
- No delete commands yet.
- `in_progress` exists in the enum but isn't exposed in the CLI.

---

## License

MIT License

Copyright (c) 2026 Sandra Njehuri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.