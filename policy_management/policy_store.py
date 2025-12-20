from datetime import datetime
from typing import Optional


class Policy:
    """Represents a policy with version history and management info."""

    def __init__(
        self,
        policy_id: str,
        title: str,
        content: str,
        *,
        owner: Optional[str] = None,
        status: str = "draft",
    ) -> None:
        self.policy_id = policy_id
        self.title = title
        self.content = content
        self.owner = owner
        self.status = status
        self.created_at = datetime.utcnow()
        self.last_reviewed_at: Optional[datetime] = None
        self.versions: list[dict[str, object]] = []
        self._append_version_record(updated_by=owner, updated_at=self.created_at)

    def _append_version_record(
        self,
        *,
        updated_by: Optional[str],
        updated_at: datetime,
    ) -> None:
        self.versions.append(
            {
                "content": self.content,
                "title": self.title,
                "updated_at": updated_at,
                "updated_by": updated_by,
                "status": self.status,
                "owner": self.owner,
                "last_reviewed_at": self.last_reviewed_at,
            }
        )

    def update(
        self,
        new_content: Optional[str] = None,
        *,
        title: Optional[str] = None,
        updated_by: Optional[str] = None,
        updated_at: Optional[datetime] = None,
        owner: Optional[str] = None,
        status: Optional[str] = None,
        last_reviewed_at: Optional[datetime] = None,
    ) -> None:
        """Update policy details and track version history."""

        if new_content is not None:
            self.content = new_content
        if title is not None:
            self.title = title
        if owner is not None:
            self.owner = owner
        if status is not None:
            self.status = status
        if last_reviewed_at is not None:
            self.last_reviewed_at = last_reviewed_at

        self._append_version_record(
            updated_by=updated_by,
            updated_at=updated_at or datetime.utcnow(),
        )

    def mark_reviewed(self, reviewer: Optional[str] = None, reviewed_at: Optional[datetime] = None) -> None:
        timestamp = reviewed_at or datetime.utcnow()
        self.update(updated_by=reviewer, last_reviewed_at=timestamp, updated_at=timestamp)


class PolicyLibrary:
    """Represents a collection of policies."""

    def __init__(self, library_id: str, name: str) -> None:
        self.library_id = library_id
        self.name = name
        self.policy_ids: set[str] = set()

    def add_policy(self, policy_id: str) -> None:
        self.policy_ids.add(policy_id)

    def remove_policy(self, policy_id: str) -> None:
        self.policy_ids.discard(policy_id)


class PolicyStore:
    """In-memory store for policies and libraries."""

    def __init__(self) -> None:
        self.policies: dict[str, Policy] = {}
        self.libraries: dict[str, PolicyLibrary] = {}

    def add_policy(
        self,
        policy_id: str,
        title: str,
        content: str,
        *,
        owner: Optional[str] = None,
        status: str = "draft",
    ) -> None:
        if policy_id in self.policies:
            raise ValueError(f"Policy {policy_id} already exists")
        self.policies[policy_id] = Policy(
            policy_id,
            title,
            content,
            owner=owner,
            status=status,
        )

    def edit_policy(
        self,
        policy_id: str,
        new_content: Optional[str] = None,
        *,
        title: Optional[str] = None,
        updated_by: Optional[str] = None,
        owner: Optional[str] = None,
        status: Optional[str] = None,
    ) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        self.policies[policy_id].update(
            new_content,
            title=title,
            updated_by=updated_by,
            owner=owner,
            status=status,
        )

    def delete_policy(self, policy_id: str) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        del self.policies[policy_id]
        for library in self.libraries.values():
            library.remove_policy(policy_id)

    def view_policy(self, policy_id: str) -> Policy:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        return self.policies[policy_id]

    def list_policies(self) -> list[Policy]:
        return list(self.policies.values())

    def set_policy_owner(self, policy_id: str, owner: str) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        self.policies[policy_id].update(owner=owner)

    def set_policy_status(self, policy_id: str, status: str) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        self.policies[policy_id].update(status=status)

    def mark_policy_reviewed(self, policy_id: str, reviewer: Optional[str] = None) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        self.policies[policy_id].mark_reviewed(reviewer=reviewer)

    def create_library(self, library_id: str, name: str) -> None:
        if library_id in self.libraries:
            raise ValueError(f"Library {library_id} already exists")
        self.libraries[library_id] = PolicyLibrary(library_id, name)

    def delete_library(self, library_id: str) -> None:
        if library_id not in self.libraries:
            raise KeyError(f"Library {library_id} not found")
        del self.libraries[library_id]

    def add_policy_to_library(self, library_id: str, policy_id: str) -> None:
        if library_id not in self.libraries:
            raise KeyError(f"Library {library_id} not found")
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        self.libraries[library_id].add_policy(policy_id)

    def remove_policy_from_library(self, library_id: str, policy_id: str) -> None:
        if library_id not in self.libraries:
            raise KeyError(f"Library {library_id} not found")
        self.libraries[library_id].remove_policy(policy_id)

    def list_policies_in_library(self, library_id: str) -> list[Policy]:
        if library_id not in self.libraries:
            raise KeyError(f"Library {library_id} not found")
        library = self.libraries[library_id]
        return [self.policies[pid] for pid in library.policy_ids if pid in self.policies]
