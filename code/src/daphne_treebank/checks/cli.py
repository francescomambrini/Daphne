from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from .catalog import check_catalog
from .conllu import check_conllu
from .model import Issue
from .xml import check_xml


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check the basic well-formedness of Daphne CoNLL-U and XML data."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="repository root (default: current directory)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    conllu_root = root / "data" / "annotation"
    xml_root = root / "data" / "texts" / "data"

    conllu_files = sorted(conllu_root.rglob("*.conllu")) if conllu_root.is_dir() else []
    xml_files = sorted(xml_root.rglob("*.xml")) if xml_root.is_dir() else []

    issues: list[Issue] = []
    issues.extend(check_catalog(root))
    if not conllu_files:
        issues.append(Issue(conllu_root, "no CoNLL-U files found"))
    if not xml_files:
        issues.append(Issue(xml_root, "no XML files found"))

    for path in conllu_files:
        issues.extend(check_conllu(path))
    for path in xml_files:
        issues.extend(check_xml(path))

    if issues:
        for issue in issues:
            try:
                display_issue = Issue(
                    issue.path.relative_to(root), issue.message, issue.line
                )
            except ValueError:
                display_issue = issue
            print(display_issue)
        print(
            f"FAILED: {len(issues)} issue(s); checked the catalog, "
            f"{len(conllu_files)} CoNLL-U files, and {len(xml_files)} XML files."
        )
        return 1

    print(
        f"OK: {len(conllu_files)} CoNLL-U and {len(xml_files)} XML files "
        "are well-formed; the catalog is valid and complete."
    )
    return 0
