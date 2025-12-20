from policy_management.policy_store import PolicyStore


from datetime import datetime, timezone


def test_add_edit_delete_policy():
    store = PolicyStore()
    created_at = datetime(2023, 12, 31, 8, 0, tzinfo=timezone.utc)
    store.add_policy(
        "1",
        "First",
        "content v1",
        created_by="author",
        created_at=created_at,
    )

    policy = store.view_policy("1")
    assert policy.title == "First"
    assert policy.content == "content v1"
    assert policy.versions[0]["content"] == "content v1"
    assert policy.versions[0]["title"] == "First"
    assert policy.versions[0]["user"] == "author"
    assert policy.versions[0]["timestamp"] == created_at.isoformat()

    edited_at = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    store.edit_policy(
        "1",
        "content v2",
        title="First edited",
        updated_by="admin",
        updated_at=edited_at,
    )
    policy = store.view_policy("1")
    assert policy.title == "First edited"
    assert policy.content == "content v2"
    assert len(policy.versions) == 2

    latest_version = policy.versions[-1]
    assert latest_version == {
        "content": "content v2",
        "title": "First edited",
        "timestamp": edited_at.isoformat(),
        "user": "admin",
    }

    store.delete_policy("1")
    assert store.list_policies() == []
