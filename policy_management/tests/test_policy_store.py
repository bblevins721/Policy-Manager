from policy_management.policy_store import PolicyStore


def test_add_edit_delete_policy():
    store = PolicyStore()
    store.add_policy("1", "First", "content v1")

    policy = store.view_policy("1")
    assert policy.title == "First"
    assert policy.content == "content v1"

    store.edit_policy("1", "content v2")
    policy = store.view_policy("1")
    assert policy.content == "content v2"
    assert policy.versions == ["content v1", "content v2"]

    store.delete_policy("1")
    assert store.list_policies() == []


def test_library_creation_and_policy_assignment():
    store = PolicyStore()
    store.add_policy("1", "Policy One", "content a")
    store.add_policy("2", "Policy Two", "content b")

    store.create_library("lib1")
    libraries = store.list_libraries()
    assert len(libraries) == 1
    assert libraries[0].library_id == "lib1"

    store.add_policy_to_library("1", "lib1")
    store.add_policy_to_library("2", "lib1")

    policies_in_library = store.list_policies_in_library("lib1")
    assert {policy.policy_id for policy in policies_in_library} == {"1", "2"}

    store.remove_policy_from_library("1", "lib1")
    policies_after_removal = store.list_policies_in_library("lib1")
    assert [policy.policy_id for policy in policies_after_removal] == ["2"]

    store.delete_library("lib1")
    assert store.list_libraries() == []
