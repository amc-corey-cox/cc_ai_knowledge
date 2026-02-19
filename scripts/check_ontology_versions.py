#!/usr/bin/env python3
"""Check local ontology files against upstream releases.

Compares the version embedded in local OBO files against the latest
GitHub release tag, without downloading anything.

Usage:
    python scripts/check_ontology_versions.py
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ONTOLOGIES = [
    {
        "name": "AIO (Artificial Intelligence Ontology)",
        "local_file": REPO_ROOT / "conf" / "aio.obo",
        "github_repo": "berkeleybop/artificial-intelligence-ontology",
    },
]


def get_local_version(obo_path: Path) -> str | None:
    """Extract the date from the data-version line in an OBO file."""
    with open(obo_path) as f:
        for line in f:
            if line.startswith("data-version:"):
                match = re.search(r"(\d{4}-\d{2}-\d{2})", line)
                return match.group(1) if match else None
            if line.startswith("[Term]"):
                break
    return None


def get_latest_release(github_repo: str) -> str | None:
    """Get the latest release tag date from a GitHub repo."""
    result = subprocess.run(
        ["gh", "api", f"repos/{github_repo}/releases/latest", "--jq", ".tag_name"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    tag = result.stdout.strip()
    match = re.search(r"(\d{4}-\d{2}-\d{2})", tag)
    return match.group(1) if match else None


def main() -> int:
    outdated = False

    for ont in ONTOLOGIES:
        local = get_local_version(ont["local_file"])
        latest = get_latest_release(ont["github_repo"])

        if not local:
            print(f"WARNING {ont['name']}: could not read local version from {ont['local_file'].name}")
            continue
        if not latest:
            print(f"WARNING {ont['name']}: could not fetch latest release from {ont['github_repo']}")
            continue

        if local >= latest:
            print(f"  OK {ont['name']}: local {local}, latest release {latest}")
        else:
            outdated = True
            print(f"  OUTDATED {ont['name']}: local {local}, latest release {latest}")
            print(f"    Update from: https://github.com/{ont['github_repo']}/releases")

    if outdated:
        print("\nSome ontology files are outdated.")
        return 1

    print("\nAll ontology files are current.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
