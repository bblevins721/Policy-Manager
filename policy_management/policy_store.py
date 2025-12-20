class Policy:
    """Represents a policy with version history."""

    def __init__(self, policy_id: str, title: str, content: str):
        self.policy_id = policy_id
        self.title = title
        self.content = content
        self.versions = [content]

    def update(self, new_content: str) -> None:
        """Update policy content and track version history."""
        self.content = new_content
        self.versions.append(new_content)


class PolicyLibrary:
    """Represents a collection of policies grouped under a library ID."""

    def __init__(self, library_id: str):
        self.library_id = library_id
        self.policies: dict[str, Policy] = {}

    def add_policy(self, policy: Policy) -> None:
        if policy.policy_id in self.policies:
            raise ValueError(f"Policy {policy.policy_id} already in library {self.library_id}")
        self.policies[policy.policy_id] = policy

    def remove_policy(self, policy_id: str) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found in library {self.library_id}")
        del self.policies[policy_id]

    def list_policies(self) -> list[Policy]:
        return list(self.policies.values())


class PolicyStore:
    """In-memory store for policies."""

    def __init__(self) -> None:
        self.policies: dict[str, Policy] = {}
        self.libraries: dict[str, PolicyLibrary] = {}

    def add_policy(self, policy_id: str, title: str, content: str) -> None:
        if policy_id in self.policies:
            raise ValueError(f"Policy {policy_id} already exists")
        self.policies[policy_id] = Policy(policy_id, title, content)

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

    def list_policies(self) -> list[Policy]:
        return list(self.policies.values())

    def create_library(self, library_id: str) -> None:
        if library_id in self.libraries:
            raise ValueError(f"Library {library_id} already exists")
        self.libraries[library_id] = PolicyLibrary(library_id)

    def delete_library(self, library_id: str) -> None:
        if library_id not in self.libraries:
            raise KeyError(f"Library {library_id} not found")
        del self.libraries[library_id]

    def view_library(self, library_id: str) -> PolicyLibrary:
        if library_id not in self.libraries:
            raise KeyError(f"Library {library_id} not found")
        return self.libraries[library_id]

    def list_libraries(self) -> list[PolicyLibrary]:
        return list(self.libraries.values())

    def add_policy_to_library(self, policy_id: str, library_id: str) -> None:
        if policy_id not in self.policies:
            raise KeyError(f"Policy {policy_id} not found")
        library = self.view_library(library_id)
        library.add_policy(self.policies[policy_id])

    def remove_policy_from_library(self, policy_id: str, library_id: str) -> None:
        library = self.view_library(library_id)
        library.remove_policy(policy_id)

    def list_policies_in_library(self, library_id: str) -> list[Policy]:
        library = self.view_library(library_id)
        return library.list_policies()
