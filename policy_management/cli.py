"""Command line interface for managing policies.

Usage examples:
    python -m policy_management.cli list --store policies.json
    python -m policy_management.cli add 1 "Policy title" "Initial content" --store policies.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .policy_store import FilePolicyStore, Policy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Policy Management CLI")
    store_parent = argparse.ArgumentParser(add_help=False)
    store_parent.add_argument(
        "--store",
        type=Path,
        default=Path("policies.json"),
        help="Path to the policy store file (default: policies.json)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", parents=[store_parent], help="Add a new policy")
    add_parser.add_argument("policy_id", help="Unique policy identifier")
    add_parser.add_argument("title", help="Policy title")
    add_parser.add_argument("content", help="Policy content")
    add_parser.add_argument("--library", help="Optional library name", default=None)

    edit_parser = subparsers.add_parser(
        "edit", parents=[store_parent], help="Edit an existing policy"
    )
    edit_parser.add_argument("policy_id", help="Policy identifier to edit")
    edit_parser.add_argument("content", help="New policy content")

    delete_parser = subparsers.add_parser(
        "delete", parents=[store_parent], help="Delete a policy"
    )
    delete_parser.add_argument("policy_id", help="Policy identifier to delete")

    view_parser = subparsers.add_parser("view", parents=[store_parent], help="View policy details")
    view_parser.add_argument("policy_id", help="Policy identifier to view")

    list_parser = subparsers.add_parser("list", parents=[store_parent], help="List all policies")
    list_parser.add_argument("--library", help="Filter policies by library", default=None)

    history_parser = subparsers.add_parser(
        "history", parents=[store_parent], help="Show version history for a policy"
    )
    history_parser.add_argument("policy_id", help="Policy identifier to inspect")

    revert_parser = subparsers.add_parser(
        "revert", parents=[store_parent], help="Revert a policy to a previous version"
    )
    revert_parser.add_argument("policy_id", help="Policy identifier to revert")
    revert_parser.add_argument(
        "version_number",
        type=int,
        help="One-based version number to restore (a new version will be recorded)",
    )

    subparsers.add_parser(
        "stats", parents=[store_parent], help="Show counts of policies per library"
    )

    return parser


def _format_policy(policy: Policy) -> str:
    version_lines = [f"  {idx + 1}: {content}" for idx, content in enumerate(policy.versions)]
    versions_text = "\n".join(version_lines) if version_lines else "  (no versions)"
    return (
        f"ID: {policy.policy_id}\n"
        f"Title: {policy.title}\n"
        f"Library: {policy.library}\n"
        f"Current version: {policy.content}\n"
        f"Versions:\n{versions_text}"
    )


def handle_command(args: argparse.Namespace) -> int:
    store = FilePolicyStore(args.store)

    try:
        if args.command == "add":
            store.add_policy(args.policy_id, args.title, args.content, args.library)
            print(f"Policy {args.policy_id} added.")
        elif args.command == "edit":
            store.edit_policy(args.policy_id, args.content)
            version = len(store.view_policy(args.policy_id).versions)
            print(f"Policy {args.policy_id} updated to version {version}.")
        elif args.command == "delete":
            store.delete_policy(args.policy_id)
            print(f"Policy {args.policy_id} deleted.")
        elif args.command == "view":
            policy = store.view_policy(args.policy_id)
            print(_format_policy(policy))
        elif args.command == "list":
            policies = store.list_policies(args.library)
            if not policies:
                print("No policies found.")
            else:
                for policy in policies:
                    print(f"{policy.policy_id}: {policy.title} (library: {policy.library})")
        elif args.command == "history":
            policy = store.view_policy(args.policy_id)
            print(_format_policy(policy))
        elif args.command == "revert":
            new_version = store.revert_policy(args.policy_id, args.version_number)
            print(
                f"Policy {args.policy_id} reverted to version {args.version_number}. "
                f"Current version is {new_version}."
            )
        elif args.command == "stats":
            policies = store.list_policies()
            summary = store.library_summary()
            print(f"Total policies: {len(policies)}")
            if not policies:
                print("No libraries found.")
            else:
                for library, count in sorted(summary.items()):
                    print(f"{library}: {count}")
        else:
            raise ValueError(f"Unknown command: {args.command}")
    except (ValueError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return handle_command(args)


if __name__ == "__main__":
    sys.exit(main())
