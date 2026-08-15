from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .model import Issue


WORD_ID = re.compile(r"^[1-9][0-9]*$")
RANGE_ID = re.compile(r"^([1-9][0-9]*)-([1-9][0-9]*)$")
EMPTY_ID = re.compile(r"^([0-9]+)\.([1-9][0-9]*)$")
DEPS_HEAD = re.compile(r"^(?:0|[1-9][0-9]*)(?:\.[1-9][0-9]*)?$")


@dataclass(frozen=True)
class Row:
    line: int
    fields: tuple[str, ...]

    @property
    def token_id(self) -> str:
        return self.fields[0]


def check_conllu(path: Path) -> list[Issue]:
    """Check CoNLL-U serialization without evaluating linguistic annotation."""

    issues: list[Issue] = []
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        return [Issue(path, f"not valid UTF-8: {error}")]
    except OSError as error:
        return [Issue(path, f"cannot read file: {error}")]

    if not text:
        return [Issue(path, "empty CoNLL-U file")]
    if b"\r" in raw:
        issues.append(Issue(path, "contains CR characters; CoNLL-U requires LF line endings"))
    if not text.endswith("\n\n"):
        issues.append(Issue(path, "the final sentence is not followed by a blank line"))

    sentence: list[Row] = []
    token_lines_started = False
    saw_sentence = False

    for line_number, line in enumerate(text.split("\n"), start=1):
        if line == "":
            if sentence:
                issues.extend(_check_sentence(path, sentence))
                sentence = []
                token_lines_started = False
                saw_sentence = True
            continue

        if line.startswith("#"):
            if token_lines_started:
                issues.append(Issue(path, "comment occurs after a token line", line_number))
            continue

        fields = tuple(line.split("\t"))
        if len(fields) != 10:
            issues.append(
                Issue(path, f"token line has {len(fields)} fields instead of 10", line_number)
            )
            token_lines_started = True
            continue

        if any(field == "" for field in fields):
            issues.append(Issue(path, "token line contains an empty field", line_number))

        for index in (0, 3, 4, 5, 6, 7, 8):
            if " " in fields[index]:
                issues.append(
                    Issue(path, f"field {index + 1} contains a space", line_number)
                )

        sentence.append(Row(line_number, fields))
        token_lines_started = True

    if sentence:
        issues.extend(_check_sentence(path, sentence))
        saw_sentence = True
    if not saw_sentence:
        issues.append(Issue(path, "file contains no sentence"))

    return issues


def _check_sentence(path: Path, rows: list[Row]) -> list[Issue]:
    issues: list[Issue] = []
    seen_ids: dict[str, int] = {}
    word_rows: list[Row] = []
    range_rows: list[tuple[Row, int, int]] = []
    empty_rows: list[tuple[Row, int, int]] = []

    for row in rows:
        token_id = row.token_id
        if token_id in seen_ids:
            issues.append(
                Issue(
                    path,
                    f"duplicate ID {token_id}; first used on line {seen_ids[token_id]}",
                    row.line,
                )
            )
        else:
            seen_ids[token_id] = row.line

        if WORD_ID.fullmatch(token_id):
            word_rows.append(row)
            issues.extend(_check_word(path, row))
            continue

        range_match = RANGE_ID.fullmatch(token_id)
        if range_match:
            start, end = map(int, range_match.groups())
            range_rows.append((row, start, end))
            issues.extend(_check_range(path, row, start, end))
            continue

        empty_match = EMPTY_ID.fullmatch(token_id)
        if empty_match:
            base, suffix = map(int, empty_match.groups())
            empty_rows.append((row, base, suffix))
            issues.extend(_check_empty(path, row))
            continue

        issues.append(Issue(path, f"invalid ID {token_id!r}", row.line))

    if not word_rows:
        issues.append(Issue(path, "sentence has no syntactic word", rows[0].line))
        return issues

    word_ids = [int(row.token_id) for row in word_rows]
    expected = list(range(1, len(word_ids) + 1))
    if word_ids != expected:
        issues.append(
            Issue(path, f"word IDs are {word_ids!r}; expected {expected!r}", word_rows[0].line)
        )

    word_id_set = set(word_ids)
    row_positions = {row.token_id: position for position, row in enumerate(rows)}

    previous_end = 0
    for row, start, end in range_rows:
        if start <= previous_end:
            issues.append(Issue(path, "multiword-token ranges overlap", row.line))
        previous_end = max(previous_end, end)
        if any(word not in word_id_set for word in range(start, end + 1)):
            issues.append(Issue(path, "multiword-token range contains a missing word", row.line))
        if str(start) in row_positions and row_positions[row.token_id] > row_positions[str(start)]:
            issues.append(
                Issue(path, "multiword-token row does not precede its first word", row.line)
            )

    empty_suffixes: dict[int, list[tuple[int, int]]] = {}
    for row, base, suffix in empty_rows:
        if base not in word_id_set and base != 0:
            issues.append(Issue(path, f"empty-node base {base} is not a word ID", row.line))
        empty_suffixes.setdefault(base, []).append((suffix, row.line))
    for base, values in empty_suffixes.items():
        suffixes = [suffix for suffix, _ in values]
        expected_suffixes = list(range(1, len(suffixes) + 1))
        if suffixes != expected_suffixes:
            issues.append(
                Issue(
                    path,
                    f"empty-node suffixes after {base} are {suffixes!r}; "
                    f"expected {expected_suffixes!r}",
                    values[0][1],
                )
            )

    for row in word_rows:
        head = int(row.fields[6]) if row.fields[6].isdigit() else None
        if head is not None and head != 0 and head not in word_id_set:
            issues.append(Issue(path, f"HEAD {head} is not a word ID", row.line))

    return issues


def _check_word(path: Path, row: Row) -> list[Issue]:
    issues: list[Issue] = []
    fields = row.fields
    if not re.fullmatch(r"(?:_|0|[1-9][0-9]*)", fields[6]):
        issues.append(Issue(path, f"invalid HEAD {fields[6]!r}", row.line))
    issues.extend(_check_deps(path, row))
    return issues


def _check_range(path: Path, row: Row, start: int, end: int) -> list[Issue]:
    issues: list[Issue] = []
    if start >= end:
        issues.append(Issue(path, "multiword-token range is empty or reversed", row.line))
    for index in (2, 3, 4, 6, 7, 8):
        if row.fields[index] != "_":
            issues.append(
                Issue(path, f"multiword-token field {index + 1} must be _", row.line)
            )
    if row.fields[5] not in {"_", "Typo=Yes"}:
        issues.append(Issue(path, "multiword-token FEATS must be _ or Typo=Yes", row.line))
    return issues


def _check_empty(path: Path, row: Row) -> list[Issue]:
    issues: list[Issue] = []
    if row.fields[6] != "_" or row.fields[7] != "_":
        issues.append(Issue(path, "empty-node HEAD and DEPREL must be _", row.line))
    if row.fields[8] == "_":
        issues.append(Issue(path, "empty node must have a DEPS value", row.line))
    issues.extend(_check_deps(path, row))
    return issues


def _check_deps(path: Path, row: Row) -> list[Issue]:
    deps = row.fields[8]
    if deps == "_":
        return []

    issues: list[Issue] = []
    for edge in deps.split("|"):
        head, separator, relation = edge.partition(":")
        if not separator or not relation or not DEPS_HEAD.fullmatch(head):
            issues.append(Issue(path, f"invalid DEPS edge {edge!r}", row.line))
    return issues
