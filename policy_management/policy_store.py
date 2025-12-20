from datetime import datetime, timezone


class Policy:
    """Represents a policy with version history."""

    def __init__(
        self,
        policy_id: str,
        title: str,
        content: str,
        *,
        created_by: str | None = None,
        created_at: datetime | None = None,
    ):
        self.policy_id = policy_id
        self.title = title
        self.content = content
        timestamp = (created_at or datetime.now(tz=timezone.utc)).isoformat()
        self.versions = [
            {
                "content": content,
                "title": title,
                "timestamp": timestamp,
                "user": created_by,
            }
        ]

    def update(
        self,
        new_content: str,
        *,
        title: str | None = None,
        updated_by: str | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        """Update policy content and track version history."""
        self.content = new_content
        if title is not None:
            self.title = title
        timestamp = updated_at or datetime.now(tz=timezone.utc)
        self.versions.append(
            {
                "content": new_content,
                "title": self.title,
                "timestamp": timestamp.isoformat(),
                "user": updated_by,
            }
        )


class PolicyStore:
    """In-memory store for policies."""

    def __init__(self) -> None:
        self.policies: dict[str, Policy] = {}

    def add_policy(
        self,
        policy_id: str,
        title: str,
        content: str,
        *,
        created_by: str | None = None,
        created_at: datetime | None = None,
    ) -> None:
        if policy_id in self.policies:
            raise ValueError(f"Policy {policy_id} already exists")
        self.policies[policy_id] = Policy(
            policy_id,
            title,
            content,
            created_by=created_by,
            created_at=created_at,
        )

    def edit_policy(
        self,
        policy_id: str,
        new_content: str,
        *,
        title: str | None = None,
        updated_by: str | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        self.policies[policy_id].update(
            new_content,
            title=title,
            updated_by=updated_by,
            updated_at=updated_at,
        )

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
