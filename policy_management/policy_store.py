from __future__ import annotations

from datetime import datetime
from typing import Any


class Policy:
    """Represents a policy with version history."""

    def __init__(
        self,
        policy_id: str,
        title: str,
        content: str,
        owner: str,
        status: str,
        created_at: datetime | None = None,
        last_reviewed_at: datetime | None = None,
    ):
        self.policy_id = policy_id
        self.title = title
        self.content = content
        self.owner = owner
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.last_reviewed_at = last_reviewed_at
        self.versions: list[dict[str, Any]] = []
        self._record_version()

    def _record_version(self) -> None:
        self.versions.append(
            {
                "content": self.content,
                "owner": self.owner,
                "status": self.status,
                "created_at": self.created_at,
                "last_reviewed_at": self.last_reviewed_at,
            }
        )

    def update(self, new_content: str) -> None:
        """Update policy content and track version history."""
        self.content = new_content
        self._record_version()

    def mark_reviewed(self, reviewed_at: datetime | None = None) -> None:
        """Mark policy as reviewed and track history."""
        self.last_reviewed_at = reviewed_at or datetime.utcnow()
        self._record_version()

    def change_owner(self, new_owner: str) -> None:
        """Change policy owner and track history."""
        self.owner = new_owner
        self._record_version()

    def change_status(self, new_status: str) -> None:
        """Change policy status and track history."""
        self.status = new_status
        self._record_version()


class PolicyStore:
    """In-memory store for policies."""

    def __init__(self) -> None:
        self.policies: dict[str, Policy] = {}

    def add_policy(
        self,
        policy_id: str,
        title: str,
        content: str,
        owner: str,
        status: str,
        created_at: datetime | None = None,
    ) -> None:
        if policy_id in self.policies:
            raise ValueError(f"Policy {policy_id} already exists")
        self.policies[policy_id] = Policy(
            policy_id,
            title,
            content,
            owner,
            status,
            created_at=created_at,
        )

    def edit_policy(self, policy_id: str, new_content: str) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        self.policies[policy_id].update(new_content)

    def mark_policy_reviewed(
        self, policy_id: str, reviewed_at: datetime | None = None
    ) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        self.policies[policy_id].mark_reviewed(reviewed_at)

    def change_policy_owner(self, policy_id: str, new_owner: str) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        self.policies[policy_id].change_owner(new_owner)

    def change_policy_status(self, policy_id: str, new_status: str) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        self.policies[policy_id].change_status(new_status)

    def delete_policy(self, policy_id: str) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        del self.policies[policy_id]

    def view_policy(self, policy_id: str) -> Policy:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        return self.policies[policy_id]

    def list_policies(self) -> list[Policy]:
        return list(self.policies.values())
