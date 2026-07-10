#!/usr/bin/env python3
"""Validate relative Markdown links without external dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SKIPPED_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#")


def normalize_target(raw_target: str) -> str:
    """Return the local path portion of a Markdown link target."""
    target = raw_target.strip()

    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    elif " " in target:
        target = target.split(" ", 1)[0]

    target = target.split("#", 1)[0].split("?", 1)[0]
    return unquote(target)


def resolve_target(source: Path, target: str) -> Path:
    """Resolve a target relative to its source Markdown file."""
    candidate = (source.parent / target).resolve()
    if candidate.is_dir():
        candidate = candidate / "README.md"
    return candidate


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    markdown_files = sorted(
        path for path in root.rglob("*.md") if ".git" not in path.parts
    )

    failures: list[str] = []

    for source in markdown_files:
        text = source.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in LINK_RE.finditer(line):
                raw_target = match.group(1).strip()
                if not raw_target or raw_target.startswith(SKIPPED_PREFIXES):
                    continue

                target = normalize_target(raw_target)
                if not target:
                    continue

                resolved = resolve_target(source, target)
                try:
                    resolved.relative_to(root)
                except ValueError:
                    failures.append(
                        f"{source.relative_to(root)}:{line_number}: "
                        f"link escapes repository: {raw_target}"
                    )
                    continue

                if not resolved.exists():
                    failures.append(
                        f"{source.relative_to(root)}:{line_number}: "
                        f"missing target: {raw_target}"
                    )

    if failures:
        print("Broken relative Markdown links found:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        f"Validated {len(markdown_files)} Markdown files; "
        "no broken relative links found."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
