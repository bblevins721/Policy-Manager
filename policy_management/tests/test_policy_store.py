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


def test_scan_policies_recommendations():
    store = PolicyStore()
    stale_timestamp = datetime(2024, 7, 1, tzinfo=timezone.utc)
    recent_timestamp = datetime(2024, 12, 1, tzinfo=timezone.utc)

    store.add_policy(
        "stale",
        "Old Policy",
        "old content",
        created_by=None,
        created_at=stale_timestamp,
    )
    # Missing updated_by metadata and old timestamp should trigger recommendations.
    store.edit_policy(
        "stale",
        "old content updated",
        updated_by=None,
        updated_at=stale_timestamp,
    )

    store.add_policy(
        "fresh",
        "New Policy",
        "new content",
        created_by="owner",
        created_at=recent_timestamp,
    )

    report = store.scan_policies(
        staleness_days=120,
        now=datetime(2024, 12, 31, tzinfo=timezone.utc),
    )

    stale_policy_report = next(item for item in report if item["policy_id"] == "stale")
    assert stale_policy_report == {
        "policy_id": "stale",
        "title": "Old Policy",
        "last_updated": stale_timestamp.isoformat(),
        "recommendations": [
            "Review policy; last updated over 120 days ago.",
            "Capture updated_by metadata on next revision.",
        ],
    }

    fresh_policy_report = next(item for item in report if item["policy_id"] == "fresh")
    assert fresh_policy_report == {
        "policy_id": "fresh",
        "title": "New Policy",
        "last_updated": recent_timestamp.isoformat(),
        "recommendations": [],
    }
