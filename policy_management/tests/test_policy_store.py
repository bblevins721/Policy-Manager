from datetime import datetime

from policy_management.policy_store import PolicyStore


def test_add_edit_delete_policy_with_versions_and_title_updates():
    store = PolicyStore()
    store.add_policy("1", "First", "content v1", owner="alice", status="approved")

    policy = store.view_policy("1")
    assert policy.title == "First"
    assert policy.content == "content v1"
    assert policy.owner == "alice"
    assert policy.status == "approved"
    assert policy.versions[0]["title"] == "First"

    store.edit_policy("1", "content v2", title="Updated", updated_by="bob")
    policy = store.view_policy("1")
    assert policy.title == "Updated"
    assert policy.content == "content v2"
    assert len(policy.versions) == 2
    assert policy.versions[-1]["updated_by"] == "bob"
    assert policy.versions[-1]["title"] == "Updated"
    assert policy.versions[-1]["content"] == "content v2"

    store.delete_policy("1")
    assert store.list_policies() == []


def test_policy_library_grouping():
    store = PolicyStore()
    store.add_policy("1", "Policy A", "A")
    store.add_policy("2", "Policy B", "B")
    store.create_library("lib1", "Library One")
    store.add_policy_to_library("lib1", "1")
    store.add_policy_to_library("lib1", "2")

    policies_in_library = store.list_policies_in_library("lib1")
    assert {p.policy_id for p in policies_in_library} == {"1", "2"}

    store.remove_policy_from_library("lib1", "2")
    policies_in_library = store.list_policies_in_library("lib1")
    assert {p.policy_id for p in policies_in_library} == {"1"}


def test_policy_management_info_updates():
    store = PolicyStore()
    store.add_policy("1", "Policy", "content", status="draft")

    store.set_policy_owner("1", "owner1")
    store.set_policy_status("1", "approved")
    before_review = datetime.utcnow()
    store.mark_policy_reviewed("1", reviewer="qa")
    policy = store.view_policy("1")

    assert policy.owner == "owner1"
    assert policy.status == "approved"
    assert policy.last_reviewed_at is not None
    assert policy.last_reviewed_at >= before_review
    assert policy.versions[-1]["updated_by"] == "qa"
