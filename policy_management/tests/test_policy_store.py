from datetime import datetime
import pytest

from policy_management.policy_store import PolicyStore


def test_add_edit_delete_policy():
    store = PolicyStore()
    created_at = datetime(2024, 1, 1, 12, 0, 0)
    review_time = datetime(2024, 1, 2, 12, 0, 0)
    store.add_policy("1", "First", "content v1", "Alice", "Draft", created_at)

    policy = store.view_policy("1")
    assert policy.title == "First"
    assert policy.content == "content v1"
    assert policy.owner == "Alice"
    assert policy.status == "Draft"
    assert policy.created_at == created_at
    assert policy.last_reviewed_at is None
    assert policy.versions == [
        {
            "content": "content v1",
            "owner": "Alice",
            "status": "Draft",
            "created_at": created_at,
            "last_reviewed_at": None,
        }
    ]

    store.edit_policy("1", "content v2")
    policy = store.view_policy("1")
    assert policy.content == "content v2"

    store.mark_policy_reviewed("1", review_time)
    policy = store.view_policy("1")
    assert policy.last_reviewed_at == review_time

    store.change_policy_owner("1", "Bob")
    policy = store.view_policy("1")
    assert policy.owner == "Bob"

    store.change_policy_status("1", "Approved")
    policy = store.view_policy("1")
    assert policy.status == "Approved"

    assert policy.versions == [
        {
            "content": "content v1",
            "owner": "Alice",
            "status": "Draft",
            "created_at": created_at,
            "last_reviewed_at": None,
        },
        {
            "content": "content v2",
            "owner": "Alice",
            "status": "Draft",
            "created_at": created_at,
            "last_reviewed_at": None,
        },
        {
            "content": "content v2",
            "owner": "Alice",
            "status": "Draft",
            "created_at": created_at,
            "last_reviewed_at": review_time,
        },
        {
            "content": "content v2",
            "owner": "Bob",
            "status": "Draft",
            "created_at": created_at,
            "last_reviewed_at": review_time,
        },
        {
            "content": "content v2",
            "owner": "Bob",
            "status": "Approved",
            "created_at": created_at,
            "last_reviewed_at": review_time,
        },
    ]

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


def test_duplicate_library_and_policy_addition_errors():
    store = PolicyStore()
    store.create_library("lib1")
    with pytest.raises(ValueError):
        store.create_library("lib1")

    store.add_policy("1", "Policy One", "content")
    store.create_library("lib2")
    store.add_policy_to_library("1", "lib2")
    with pytest.raises(ValueError):
        store.add_policy_to_library("1", "lib2")


def test_policy_deletion_cleans_libraries():
    store = PolicyStore()
    store.add_policy("1", "Policy One", "content")
    store.add_policy("2", "Policy Two", "content")
    store.create_library("lib1")
    store.create_library("lib2")

    store.add_policy_to_library("1", "lib1")
    store.add_policy_to_library("1", "lib2")
    store.add_policy_to_library("2", "lib2")

    store.delete_policy("1")

    assert [p.policy_id for p in store.list_policies_in_library("lib1")] == []
    assert [p.policy_id for p in store.list_policies_in_library("lib2")] == ["2"]
