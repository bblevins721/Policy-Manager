# README #

This repository hosts an open source Policy Management platform for small to medium businesses.

### What is this repository for? ###

The aim is to provide a lightweight system for managing company policies.

### Incremental Development Plan ###

Phase 1:
 - Ability to add, edit, view and delete policies.
 - Ability to create policy libraries.
 - Ability to create multiple policy versions.
 - MI information on policies

Phase 2:
 - Implement Authentication: forms authentication
 - Implement Authorization and limitedrole base access (publisher (person who can create policy) & end user (person who reads and complies ot policy)).

Phase 3/4 (TBC):
 - Implement Policy Sunsetting and Review: Ability to schdeule a release of a policy version.

Phase 3/4 (TBC):
 - Implement test framework.

Phase 5:
 - Workflow: Add authentication and workflow management layer to create, update, and properly route policies.

As each of the above phases are constructed, a tick (`) will be added.

Known Issues/Bugs:

### Development ###

A minimal Python implementation for Phase 1 exists in `policy_management/`.
Install dependencies and run tests with:

```bash
pip install -r requirements.txt
pytest
```

### Command line usage ###

The toolkit ships with a CLI so you can manage policies without writing code. By default
it stores data in `policies.json` in your working directory, but you can point it anywhere
with `--store`.

```bash
# List all policies
python -m policy_management list

# Add, update and review a policy (and put it in the "hr" library)
python -m policy_management add 1 "Remote Work" "Initial draft" --library hr --store ./my_policies.json
python -m policy_management edit 1 "Final content" --store ./my_policies.json
python -m policy_management view 1 --store ./my_policies.json

# Show detailed history and revert to an earlier version (recording a new version)
python -m policy_management history 1 --store ./my_policies.json
python -m policy_management revert 1 1 --store ./my_policies.json

# Filter by library and see usage stats
python -m policy_management list --library hr --store ./my_policies.json
python -m policy_management stats --store ./my_policies.json
```
