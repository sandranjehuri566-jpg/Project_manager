from project_manager.models import User, Project
from project_manager.utils import Storage


def test_save_and_load(tmp_path):
    path = tmp_path / "data.json"
    s = Storage(str(path))
    s.users.append(User("Alice", "a@x.com"))
    s.projects.append(Project("Site", s.users[0].id))
    s.save()

    s2 = Storage(str(path))
    s2.load()
    assert len(s2.users) == 1
    assert s2.users[0].name == "Alice"
    assert len(s2.projects) == 1


def test_load_missing_file_is_safe(tmp_path):
    s = Storage(str(tmp_path / "missing.json"))
    s.load()
    assert s.users == []


def test_load_corrupt_json_is_safe(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not json")
    s = Storage(str(path))
    s.load()
    assert s.users == []


def test_find_user_by_name_or_id(tmp_path):
    s = Storage(str(tmp_path / "d.json"))
    u = User("Alice")
    s.users.append(u)
    assert s.find_user("alice") is u
    assert s.find_user(u.id) is u
    assert s.find_user("Bob") is None