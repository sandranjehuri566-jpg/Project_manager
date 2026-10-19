from project_manager.models import User, Project, Task, TaskStatus


def test_user_roundtrip():
    u = User("Alice", "alice@example.com")
    u2 = User.from_dict(u.to_dict())
    assert u2.id == u.id
    assert u2.name == "Alice"
    assert u2.email == "alice@example.com"


def test_project_with_tasks_roundtrip():
    p = Project("Website", owner_id="u1", description="Marketing site")
    t = Task("Write copy", p.id)
    p.add_task(t)

    p2 = Project.from_dict(p.to_dict())
    assert len(p2.tasks) == 1
    assert p2.tasks[0].name == "Write copy"


def test_complete_task():
    t = Task("Ship", "p1")
    assert t.status == TaskStatus.TODO
    t.complete()
    assert t.status == TaskStatus.DONE


def test_find_task_by_title_and_id():
    p = Project("X", "u1")
    t = Task("Build homepage", p.id)
    p.add_task(t)
    assert p.find_task_by_title("build homepage") is t
    assert p.find_task_by_id(t.id) is t
    assert p.find_task_by_id("nope") is None