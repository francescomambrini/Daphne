"""Safe execution boundary for pinned DepEdit scenarios."""

from __future__ import annotations

import argparse
import difflib
import os
import stat
import sys
import tempfile
from dataclasses import dataclass
from importlib.metadata import version
from pathlib import Path
from typing import Sequence, TextIO

from depedit import DepEdit


DEPEDIT_VERSION = version("depedit")


class DepEditConfigurationError(ValueError):
    """Raised when DepEdit rejects a scenario file."""


@dataclass(frozen=True)
class FileResult:
    """The complete in-memory result of transforming one file."""

    path: Path
    original: str
    transformed: str

    @property
    def changed(self) -> bool:
        return self.original != self.transformed

    @property
    def match_count(self) -> int:
        """Count changed serialized records as the public match proxy.

        DepEdit 4.0.0 does not expose a public rule-match counter. For Daphne's
        mutation scenarios, a changed record is the stable, reviewable unit we
        can derive without depending on DepEdit internals.
        """

        before = self.original.splitlines()
        after = self.transformed.splitlines()
        if len(before) == len(after):
            return sum(before_line != after_line for before_line, after_line in zip(before, after))
        matcher = difflib.SequenceMatcher(a=before, b=after, autojunk=False)
        return sum(
            max(before_end - before_start, after_end - after_start)
            for tag, before_start, before_end, after_start, after_end
            in matcher.get_opcodes()
            if tag != "equal"
        )

    def unified_diff(self) -> str:
        if not self.changed:
            return ""
        return "".join(
            difflib.unified_diff(
                self.original.splitlines(keepends=True),
                self.transformed.splitlines(keepends=True),
                fromfile=str(self.path),
                tofile=f"{self.path} (DepEdit preview)",
            )
        )


@dataclass(frozen=True)
class FileFailure:
    path: Path
    message: str


@dataclass(frozen=True)
class RunReport:
    results: tuple[FileResult, ...]
    failures: tuple[FileFailure, ...]

    @property
    def changed_results(self) -> tuple[FileResult, ...]:
        return tuple(result for result in self.results if result.changed)

    @property
    def match_count(self) -> int:
        return sum(result.match_count for result in self.results)


def _scenario_preserves_non_token_layout(scenario_text: str) -> bool:
    for raw_line in scenario_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";"):
            continue
        if line.startswith("#") and not line.startswith("#S:"):
            continue
        columns = line.split("\t", 2)
        if len(columns) == 3 and "#S:" in columns[2]:
            return False
    return True


def find_repository_root(start: Path) -> Path:
    """Find a Daphne checkout from *start* or one of its parents."""

    resolved = start.expanduser().resolve()
    candidates = (resolved, *resolved.parents)
    for candidate in candidates:
        if (
            (candidate / "pyproject.toml").is_file()
            and (candidate / "data" / "annotation").is_dir()
        ):
            return candidate
    raise FileNotFoundError(
        f"could not find a Daphne repository at or above {resolved}"
    )


def select_input_files(root: Path, input_file: Path | None = None) -> tuple[Path, ...]:
    """Select one explicit CoNLL-U file or every annotation file recursively."""

    if input_file is not None:
        path = input_file.expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"input file does not exist: {path}")
        if path.suffix != ".conllu":
            raise ValueError(f"input file must have a .conllu suffix: {path}")
        return (path,)

    annotation_root = root / "data" / "annotation"
    if not annotation_root.is_dir():
        raise FileNotFoundError(f"annotation directory does not exist: {annotation_root}")
    paths = tuple(sorted(path.resolve() for path in annotation_root.rglob("*.conllu")))
    if not paths:
        raise FileNotFoundError(f"no .conllu files found under {annotation_root}")
    return paths


def load_scenario(path: Path) -> DepEdit:
    """Load one UTF-8 DepEdit configuration through its documented API."""

    scenario = path.expanduser().resolve()
    if not scenario.is_file():
        raise FileNotFoundError(f"scenario file does not exist: {scenario}")
    try:
        scenario_text = scenario.read_text(encoding="utf-8")
        with scenario.open("r", encoding="utf-8", newline="") as handle:
            transformer = DepEdit(handle)
        transformer._daphne_preserve_non_token_layout = (
            _scenario_preserves_non_token_layout(scenario_text)
        )
        return transformer
    except SystemExit as error:
        raise DepEditConfigurationError(
            f"DepEdit rejected scenario file {scenario}"
        ) from error


def _is_token_line(line: str) -> bool:
    content = line.rstrip("\r\n")
    return bool(content) and not content.startswith("#") and "\t" in content


def _preserve_non_token_layout(original: str, transformed: str) -> str:
    """Keep source layout for scenarios without sentence-annotation actions.

    DepEdit may reorder existing sentence comments while serializing. If its
    output has the same token structure, splice transformed token records into
    the original comments, blank lines, and newline endings instead.
    """

    original_lines = original.splitlines(keepends=True)
    transformed_lines = transformed.splitlines(keepends=True)
    original_tokens = [line for line in original_lines if _is_token_line(line)]
    transformed_tokens = [line for line in transformed_lines if _is_token_line(line)]
    original_ids = [line.split("\t", 1)[0] for line in original_tokens]
    transformed_ids = [line.split("\t", 1)[0] for line in transformed_tokens]
    if original_ids != transformed_ids:
        return transformed

    token_iterator = iter(transformed_tokens)
    merged: list[str] = []
    for original_line in original_lines:
        if not _is_token_line(original_line):
            merged.append(original_line)
            continue
        transformed_line = next(token_iterator).rstrip("\r\n")
        original_content = original_line.rstrip("\r\n")
        line_ending = original_line[len(original_content) :]
        merged.append(transformed_line + line_ending)
    return "".join(merged)


def transform_files(transformer: DepEdit, paths: Sequence[Path]) -> RunReport:
    """Transform all inputs in memory without changing any source file."""

    results: list[FileResult] = []
    failures: list[FileFailure] = []
    for path in paths:
        try:
            with path.open("r", encoding="utf-8", newline="") as stream:
                original = stream.read()
            transformed = transformer.run_depedit(
                original.splitlines(keepends=True), filename=str(path)
            )
            if getattr(transformer, "_daphne_preserve_non_token_layout", False):
                transformed = _preserve_non_token_layout(original, transformed)
            results.append(FileResult(path, original, transformed))
        except SystemExit as error:
            failures.append(
                FileFailure(
                    path,
                    f"DepEdit exited while processing the file ({error.code})",
                )
            )
        except Exception as error:
            failures.append(FileFailure(path, f"{type(error).__name__}: {error}"))
    return RunReport(tuple(results), tuple(failures))


def atomic_write(path: Path, content: str) -> None:
    """Replace *path* atomically after writing and syncing a sibling temp file."""

    mode = stat.S_IMODE(path.stat().st_mode)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            descriptor = -1
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary.exists():
            temporary.unlink()


def apply_report(report: RunReport) -> None:
    """Atomically replace changed targets after a complete successful preview."""

    if report.failures:
        raise RuntimeError("refusing to write because one or more inputs failed")
    for result in report.changed_results:
        atomic_write(result.path, result.transformed)


def _display_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def print_report(
    report: RunReport,
    *,
    scenario: Path,
    root: Path,
    mode: str,
    show_diff: bool,
    stream: TextIO | None = None,
) -> None:
    """Print a deterministic human-readable preview/application report."""

    if stream is None:
        stream = sys.stdout
    print(f"Mode: {mode}", file=stream)
    print(f"Scenario: {_display_path(scenario, root)}", file=stream)
    print(f"DepEdit version: {DEPEDIT_VERSION}", file=stream)
    print(f"Selected files: {len(report.results) + len(report.failures)}", file=stream)
    print(f"Matches/changed records: {report.match_count}", file=stream)
    print(f"Changed files: {len(report.changed_results)}", file=stream)
    print(f"Failures: {len(report.failures)}", file=stream)
    print("Files:", file=stream)
    for result in report.results:
        status = f"changed ({result.match_count})" if result.changed else "unchanged"
        print(f"  {status}: {_display_path(result.path, root)}", file=stream)
    for failure in report.failures:
        print(
            f"  failed: {_display_path(failure.path, root)}: {failure.message}",
            file=stream,
        )
    if show_diff:
        for result in report.changed_results:
            print(result.unified_diff(), end="", file=stream)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="daphne-edit",
        description=(
            "Preview or atomically apply a DepEdit scenario. Without --input-file, "
            "all .conllu files under data/annotation are selected recursively."
        ),
    )
    parser.add_argument("scenario", type=Path, help="path to a DepEdit .ini scenario")
    parser.add_argument(
        "--input-file",
        "--input",
        type=Path,
        help="select exactly one .conllu file instead of the full annotation corpus",
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Daphne repository root (default: discover from the working directory)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="atomically replace changed inputs after all transformations succeed",
    )
    parser.add_argument(
        "--no-diff",
        action="store_true",
        help="suppress unified diffs in the report",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root = (
            args.root.expanduser().resolve()
            if args.root is not None
            else find_repository_root(Path.cwd())
        )
        paths = select_input_files(root, args.input_file)
        scenario = args.scenario.expanduser().resolve()
        transformer = load_scenario(scenario)
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"daphne-edit: {error}", file=sys.stderr)
        return 2

    report = transform_files(transformer, paths)
    print_report(
        report,
        scenario=scenario,
        root=root,
        mode="apply" if args.apply else "preview",
        show_diff=not args.no_diff,
    )
    if report.failures:
        print("No files were written because at least one input failed.", file=sys.stderr)
        return 2
    if not report.changed_results:
        print("No matches found; review the scenario and target selection.", file=sys.stderr)
        return 1
    if args.apply:
        try:
            apply_report(report)
        except (OSError, RuntimeError) as error:
            print(f"daphne-edit: apply failed: {error}", file=sys.stderr)
            return 2
        print(f"Applied changes to {len(report.changed_results)} file(s).")
    else:
        print("Preview only; no files were written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
