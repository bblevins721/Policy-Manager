from datetime import datetime

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
