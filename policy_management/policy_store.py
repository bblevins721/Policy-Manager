from __future__ import annotations

import json
from pathlib import Path


class Policy:
    """Represents a policy with version history."""

    def __init__(self, policy_id: str, title: str, content: str, library: str | None = None):
        self.policy_id = policy_id
        self.title = title
        self.library = library or "default"
        self.content = content
        self.versions = [content]

    def update(self, new_content: str) -> None:
        """Update policy content and track version history."""
        self.content = new_content
        self.versions.append(new_content)

    def revert(self, version_number: int) -> int:
        """Revert to a previous version and record the revert as a new version.

        Args:
            version_number: One-based index of the version to restore.

        Returns:
            The new version number after the revert is recorded.
        """

        if version_number < 1 or version_number > len(self.versions):
            raise ValueError(
                f"Version {version_number} is out of range for policy {self.policy_id}"
            )
        content_to_restore = self.versions[version_number - 1]
        self.content = content_to_restore
        self.versions.append(content_to_restore)
        return len(self.versions)

    def to_dict(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "title": self.title,
            "library": self.library,
            "content": self.content,
            "versions": self.versions,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Policy":
        policy = cls(
            policy_id=str(data["policy_id"]),
            title=str(data["title"]),
            content=str(data["content"]),
            library=str(data.get("library") or "default"),
        )
        policy.versions = list(data.get("versions", [])) or [policy.content]
        policy.content = policy.versions[-1]
        return policy


class PolicyStore:
    """In-memory store for policies."""

    def __init__(self) -> None:
        self.policies: dict[str, Policy] = {}

    def add_policy(
        self, policy_id: str, title: str, content: str, library: str | None = None
    ) -> None:
        if policy_id in self.policies:
            raise ValueError(f"Policy {policy_id} already exists")
        self.policies[policy_id] = Policy(policy_id, title, content, library)

    def edit_policy(self, policy_id: str, new_content: str) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        self.policies[policy_id].update(new_content)

    def delete_policy(self, policy_id: str) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        del self.policies[policy_id]

    def view_policy(self, policy_id: str) -> Policy:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        return self.policies[policy_id]

    def list_policies(self, library: str | None = None) -> list[Policy]:
        if library is None:
            return list(self.policies.values())
        return [p for p in self.policies.values() if p.library == library]

    def revert_policy(self, policy_id: str, version_number: int) -> int:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        return self.policies[policy_id].revert(version_number)

    def library_summary(self) -> dict[str, int]:
        summary: dict[str, int] = {}
        for policy in self.policies.values():
            summary[policy.library] = summary.get(policy.library, 0) + 1
        return summary


class FilePolicyStore(PolicyStore):
    """Policy store that persists data to disk."""

    def __init__(self, filepath: str | Path) -> None:
        super().__init__()
        self.filepath = Path(filepath)
        self._load()

    def _load(self) -> None:
        if not self.filepath.exists():
            self.filepath.write_text(json.dumps({"policies": {}}))
        raw = json.loads(self.filepath.read_text())
        stored_policies = raw.get("policies", {})
        for policy_id, policy_data in stored_policies.items():
            self.policies[policy_id] = Policy.from_dict(policy_data)

    def _save(self) -> None:
        payload = {
            "policies": {pid: policy.to_dict() for pid, policy in self.policies.items()}
        }
        self.filepath.write_text(json.dumps(payload, indent=2))

    def add_policy(
        self, policy_id: str, title: str, content: str, library: str | None = None
    ) -> None:
        super().add_policy(policy_id, title, content, library)
        self._save()

    def edit_policy(self, policy_id: str, new_content: str) -> None:
        super().edit_policy(policy_id, new_content)
        self._save()

    def delete_policy(self, policy_id: str) -> None:
        super().delete_policy(policy_id)
        self._save()

    def revert_policy(self, policy_id: str, version_number: int) -> int:
        new_version = super().revert_policy(policy_id, version_number)
        self._save()
        return new_version
