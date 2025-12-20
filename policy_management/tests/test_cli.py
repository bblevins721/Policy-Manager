import subprocess
import sys
from pathlib import Path


def run_cli(args: list[str], store_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "policy_management.cli", *args, "--store", str(store_path)],
        text=True,
        capture_output=True,
        check=False,
    )


def test_cli_crud_flow(tmp_path: Path):
    store_path = tmp_path / "cli_store.json"

    add_result = run_cli(["add", "7", "CLI Policy", "initial", "--library", "hr"], store_path)
    assert add_result.returncode == 0
    assert "Policy 7 added." in add_result.stdout

    list_result = run_cli(["list"], store_path)
    assert list_result.returncode == 0
    assert "7: CLI Policy (library: hr)" in list_result.stdout

    list_filtered = run_cli(["list", "--library", "ops"], store_path)
    assert "No policies found." in list_filtered.stdout

    edit_result = run_cli(["edit", "7", "revised"], store_path)
    assert edit_result.returncode == 0
    assert "updated to version 2" in edit_result.stdout

    history_result = run_cli(["history", "7"], store_path)
    assert history_result.returncode == 0
    assert "Versions:" in history_result.stdout

    view_result = run_cli(["view", "7"], store_path)
    assert view_result.returncode == 0
    assert "Current version: revised" in view_result.stdout
    assert "1: initial" in view_result.stdout
    assert "2: revised" in view_result.stdout

    revert_result = run_cli(["revert", "7", "1"], store_path)
    assert revert_result.returncode == 0
    assert "reverted to version 1" in revert_result.stdout

    stats_result = run_cli(["stats"], store_path)
    assert stats_result.returncode == 0
    assert "Total policies: 1" in stats_result.stdout
    assert "hr: 1" in stats_result.stdout

    delete_result = run_cli(["delete", "7"], store_path)
    assert delete_result.returncode == 0
    assert "Policy 7 deleted." in delete_result.stdout

    empty_result = run_cli(["list"], store_path)
    assert "No policies found." in empty_result.stdout
