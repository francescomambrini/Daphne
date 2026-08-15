from __future__ import annotations

import json
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

from .model import Issue


def check_catalog(root: Path) -> list[Issue]:
    """Validate the catalog schema, identities, paths, and coverage."""

    data_root = root / "data"
    catalog_path = data_root / "catalog.yaml"
    schema_path = data_root / "catalog.schema.json"
    issues: list[Issue] = []

    try:
        catalog = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [Issue(catalog_path, "catalog file not found")]
    except OSError as error:
        return [Issue(catalog_path, f"cannot read catalog: {error}")]
    except yaml.YAMLError as error:
        line = error.problem_mark.line + 1 if error.problem_mark else None
        return [Issue(catalog_path, f"invalid YAML: {error.problem or error}", line)]

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [Issue(schema_path, "catalog schema not found")]
    except OSError as error:
        return [Issue(schema_path, f"cannot read catalog schema: {error}")]
    except json.JSONDecodeError as error:
        return [Issue(schema_path, f"invalid JSON: {error.msg}", error.lineno)]

    try:
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        validator.check_schema(schema)
    except SchemaError as error:
        return [Issue(schema_path, f"invalid JSON Schema: {error.message}")]

    for error in sorted(validator.iter_errors(catalog), key=_schema_error_key):
        location = _json_path(error.absolute_path)
        issues.append(Issue(catalog_path, f"schema {location}: {error.message}"))

    if not isinstance(catalog, dict):
        return issues
    treebanks = catalog.get("treebanks")
    exceptions = catalog.get("path_exceptions")
    if not isinstance(treebanks, list) or not isinstance(exceptions, list):
        return issues

    records = [record for record in treebanks if isinstance(record, dict)]
    exception_records = [record for record in exceptions if isinstance(record, dict)]
    issues.extend(_check_unique_values(catalog_path, records, "id"))
    issues.extend(_check_unique_values(catalog_path, records, "urn"))

    primary_works = [
        f"{record.get('author_id')}.{record.get('work_id')}"
        for record in records
        if record.get("role") == "primary"
    ]
    issues.extend(
        _duplicate_issues(catalog_path, primary_works, "duplicate primary work")
    )

    catalog_paths: list[str] = []
    for record in records:
        record_id = record.get("id", "<unknown>")
        author_id = record.get("author_id")
        work_id = record.get("work_id")
        edition_id = record.get("edition_id")
        expected_id = f"{author_id}.{work_id}.{edition_id}"
        if all(isinstance(value, str) for value in (author_id, work_id, edition_id)):
            if record_id != expected_id:
                issues.append(
                    Issue(
                        catalog_path,
                        f"record {record_id}: id does not match {expected_id}",
                    )
                )
        urn = record.get("urn")
        if isinstance(urn, str) and isinstance(record_id, str):
            expected_urn = f"urn:cts:greekLit:{record_id}"
            if urn != expected_urn:
                issues.append(
                    Issue(
                        catalog_path,
                        f"record {record_id}: URN does not match {expected_urn}",
                    )
                )

        files = record.get("files")
        if not isinstance(files, list):
            continue
        for file_record in files:
            if not isinstance(file_record, dict) or not isinstance(file_record.get("path"), str):
                continue
            path = file_record["path"]
            catalog_paths.append(path)
            issues.extend(_check_resolved_path(catalog_path, data_root, path, "catalog"))
            if record.get("role") != "legacy_external":
                issues.extend(
                    _check_canonical_path(
                        catalog_path,
                        record_id,
                        author_id,
                        work_id,
                        path,
                    )
                )

    exception_paths: list[str] = []
    for exception in exception_records:
        path = exception.get("path")
        if not isinstance(path, str):
            continue
        exception_paths.append(path)
        issues.extend(_check_resolved_path(catalog_path, data_root, path, "exception"))

    issues.extend(_duplicate_issues(catalog_path, catalog_paths, "duplicate catalog path"))
    issues.extend(_duplicate_issues(catalog_path, exception_paths, "duplicate exception path"))

    overlap = sorted(set(catalog_paths) & set(exception_paths))
    for path in overlap:
        issues.append(Issue(catalog_path, f"path is both cataloged and excepted: {path}"))

    annotation_root = data_root / "annotation"
    actual_paths = {
        path.relative_to(data_root).as_posix()
        for path in annotation_root.rglob("*.conllu")
        if path.is_file()
    }
    covered_paths = set(catalog_paths) | set(exception_paths)
    for path in sorted(actual_paths - covered_paths):
        issues.append(Issue(catalog_path, f"uncataloged CoNLL-U path: {path}"))
    for path in sorted(covered_paths - actual_paths):
        issues.append(Issue(catalog_path, f"catalog path does not exist: {path}"))

    return issues


def _check_unique_values(
    catalog_path: Path,
    records: list[dict[str, Any]],
    key: str,
) -> list[Issue]:
    values = [record.get(key) for record in records]
    strings = [value for value in values if isinstance(value, str)]
    return _duplicate_issues(catalog_path, strings, f"duplicate {key}")


def _duplicate_issues(catalog_path: Path, values: list[str], label: str) -> list[Issue]:
    return [
        Issue(catalog_path, f"{label}: {value}")
        for value, count in sorted(Counter(values).items())
        if count > 1
    ]


def _check_resolved_path(
    catalog_path: Path,
    data_root: Path,
    relative_path: str,
    kind: str,
) -> list[Issue]:
    resolved_root = data_root.resolve()
    resolved_path = (data_root / relative_path).resolve()
    try:
        resolved_path.relative_to(resolved_root)
    except ValueError:
        return [Issue(catalog_path, f"{kind} path escapes data/: {relative_path}")]
    if not resolved_path.is_file():
        return [Issue(catalog_path, f"{kind} path is not a file: {relative_path}")]
    return []


def _check_canonical_path(
    catalog_path: Path,
    record_id: Any,
    author_id: Any,
    work_id: Any,
    relative_path: str,
) -> list[Issue]:
    if not all(isinstance(value, str) for value in (record_id, author_id, work_id)):
        return []
    path = PurePosixPath(relative_path)
    expected_parent = PurePosixPath("annotation", author_id, work_id)
    issues: list[Issue] = []
    if path.parent != expected_parent:
        issues.append(
            Issue(
                catalog_path,
                f"record {record_id}: non-canonical directory {path.parent}; "
                f"expected {expected_parent}",
            )
        )
    canonical_name = f"{record_id}.conllu"
    partition_prefix = f"{record_id}."
    if path.name != canonical_name and not (
        path.name.startswith(partition_prefix) and path.name.endswith(".conllu")
    ):
        issues.append(
            Issue(catalog_path, f"record {record_id}: non-canonical filename {path.name}")
        )
    return issues


def _schema_error_key(error: Any) -> tuple[str, str]:
    return (_json_path(error.absolute_path), error.message)


def _json_path(parts: Any) -> str:
    values = list(parts)
    if not values:
        return "$"
    result = "$"
    for value in values:
        result += f"[{value}]" if isinstance(value, int) else f".{value}"
    return result
