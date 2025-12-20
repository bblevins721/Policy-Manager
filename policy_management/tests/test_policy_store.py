from pathlib import Path

from policy_management.policy_store import FilePolicyStore, PolicyStore


def test_add_edit_delete_policy():
    store = PolicyStore()
    store.add_policy("1", "First", "content v1", library="hr")

    policy = store.view_policy("1")
    assert policy.title == "First"
    assert policy.content == "content v1"
    assert policy.library == "hr"

    store.edit_policy("1", "content v2")
    policy = store.view_policy("1")
    assert policy.content == "content v2"
    assert policy.versions == ["content v1", "content v2"]

    new_version = store.revert_policy("1", 1)
    policy = store.view_policy("1")
    assert new_version == 3
    assert policy.content == "content v1"
    assert policy.versions == ["content v1", "content v2", "content v1"]

    store.delete_policy("1")
    assert store.list_policies() == []


def test_file_policy_store_persists_to_disk(tmp_path: Path):
    store_path = tmp_path / "policies.json"
    first_store = FilePolicyStore(store_path)
    first_store.add_policy("42", "Persistent", "v1", library="ops")
    first_store.edit_policy("42", "v2")

    new_store = FilePolicyStore(store_path)
    policy = new_store.view_policy("42")

    assert policy.title == "Persistent"
    assert policy.content == "v2"
    assert policy.versions == ["v1", "v2"]
    assert policy.library == "ops"


def test_filter_and_library_summary():
    store = PolicyStore()
    store.add_policy("1", "HR", "v1", library="hr")
    store.add_policy("2", "Ops", "v1", library="ops")
    store.add_policy("3", "HR 2", "v1", library="hr")

    assert {p.policy_id for p in store.list_policies(library="hr")} == {"1", "3"}
    assert {p.policy_id for p in store.list_policies(library="ops")} == {"2"}
    assert {p.policy_id for p in store.list_policies()} == {"1", "2", "3"}

    summary = store.library_summary()
    assert summary == {"hr": 2, "ops": 1}
