#!/usr/bin/env python3
"""Validate knowledge entry frontmatter against the LinkML schema.

Extracts YAML frontmatter from Markdown files and validates each entry
against the LinkML schema defined in schema/knowledge-entry.yaml.

Usage:
    python scripts/validate.py                          # validate all entries
    python scripts/validate.py topics/transformers/*.md  # validate specific files
"""

import datetime
import json
import sys
from pathlib import Path

import yaml
from linkml.validator import validate as linkml_validate

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "knowledge-entry.yaml"
TOPICS_DIR = REPO_ROOT / "topics"
PENDING_DIR = REPO_ROOT / "pending"


def _serialize_dates(obj):
    """Convert datetime.date objects to ISO format strings.

    PyYAML auto-parses YAML dates (2025-01-02) into datetime.date objects,
    but LinkML validation expects ISO date strings.
    """
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f"Not serializable: {type(obj)}")


def extract_frontmatter(filepath: Path) -> dict | None:
    """Extract YAML frontmatter from a Markdown file."""
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    try:
        end = text.index("---", 3)
    except ValueError:
        print(f"WARNING {filepath}: missing closing '---' for YAML frontmatter")
        return None
    try:
        data = yaml.safe_load(text[3:end])
    except yaml.YAMLError as exc:
        print(f"WARNING {filepath}: invalid YAML frontmatter: {exc}")
        return None
    # Round-trip through JSON to convert datetime.date → string
    return json.loads(json.dumps(data, default=_serialize_dates))


def find_entries(paths: list[str] | None = None) -> list[Path]:
    """Find Markdown files to validate."""
    if paths:
        return [Path(p).resolve() for p in paths if p.endswith(".md")]

    entries = []
    for directory in [TOPICS_DIR, PENDING_DIR]:
        if directory.exists():
            entries.extend(
                p for p in directory.rglob("*.md") if p.name != ".gitkeep"
            )
    return sorted(entries)


def main() -> int:
    paths = sys.argv[1:] if len(sys.argv) > 1 else None
    entries = find_entries(paths)

    if not entries:
        print("No entries found to validate.")
        return 0

    total = 0
    failed = 0
    skipped = 0

    for filepath in entries:
        rel_path = filepath.relative_to(REPO_ROOT)
        frontmatter = extract_frontmatter(filepath)

        if frontmatter is None:
            skipped += 1
            print(f"SKIP {rel_path}: no YAML frontmatter found")
            continue

        total += 1

        report = linkml_validate(
            frontmatter, str(SCHEMA_PATH), target_class="KnowledgeEntry"
        )

        if report.results:
            failed += 1
            print(f"FAIL {rel_path}:")
            for result in report.results:
                print(f"  - {result.severity.value}: {result.message}")
        else:
            print(f"  OK {rel_path}")

    summary = f"\n{total} entries checked, {failed} failed"
    if skipped:
        summary += f", {skipped} skipped"
    print(summary)
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
