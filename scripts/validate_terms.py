#!/usr/bin/env python3
"""Validate topic terms against configured ontologies (currently AIO).

Uses linkml-term-validator to check that ontology-backed topic terms
in the schema have valid meanings (CURIEs exist in their ontologies).

This validates the SCHEMA itself (that meaning CURIEs are real),
not individual data files. Data-level topic validation is handled
by the base validator's enum check in validate.py.

Usage:
    python scripts/validate_terms.py
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "knowledge-entry.yaml"
OAK_CONFIG = REPO_ROOT / "conf" / "oak_config.yaml"


def main() -> int:
    # Use the linkml-term-validator from the same venv as this Python
    venv_bin = Path(sys.executable).parent
    validator_bin = venv_bin / "linkml-term-validator"

    if not validator_bin.exists():
        print("Error: linkml-term-validator not found. Run 'uv sync' first.")
        return 1

    cmd = [
        str(validator_bin),
        "validate-schema",
        str(SCHEMA_PATH),
        "-c", str(OAK_CONFIG),
    ]

    print(f"Validating schema term meanings against ontologies...")
    print(f"  Schema: {SCHEMA_PATH.relative_to(REPO_ROOT)}")
    print(f"  OAK config: {OAK_CONFIG.relative_to(REPO_ROOT)}")
    print()

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    if result.returncode == 0:
        print("Term validation passed.")
    else:
        print("Term validation failed.")

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
