from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from daphne_treebank.editing.depedit import (
    FileResult,
    apply_report,
    load_scenario,
    main,
    select_input_files,
    transform_files,
)


ROOT = Path(__file__).resolve().parents[2]
SCENARIO = (
    ROOT
    / "code"
    / "rules"
    / "depedit"
    / "nonaccusative-objects-to-obl-arg"
    / "scenario.ini"
)
FIXTURES = (
    ROOT
    / "code"
    / "tests"
    / "fixtures"
    / "depedit"
    / "nonaccusative-objects-to-obl-arg"
)


class DepEditScenarioTests(unittest.TestCase):
    def test_match_count_is_positional_for_line_preserving_scenarios(self):
        result = FileResult(
            Path("repeated.conllu"),
            "same\nold\nsame\nold\nsame\n",
            "same\nnew\nsame\nnew\nsame\n",
        )

        self.assertEqual(result.match_count, 2)

    def test_scenario_matches_only_dative_and_genitive_objects(self):
        transformer = load_scenario(SCENARIO)
        input_path = FIXTURES / "input.conllu"
        report = transform_files(transformer, (input_path,))

        self.assertEqual(report.failures, ())
        self.assertEqual(len(report.changed_results), 1)
        self.assertEqual(report.match_count, 2)
        self.assertEqual(
            report.results[0].transformed,
            (FIXTURES / "expected.conllu").read_text(encoding="utf-8"),
        )

    def test_token_only_scenario_preserves_comment_order(self):
        content = """#           <persName>Editor</persName>

# sent_id = comments.1
# text = λόγος
# Speaker = Narrator
1\tλόγῳ\tλόγος\tNOUN\t_\tCase=Dat\t2\tobj\t_\t_
2\tχρῶμαι\tχράομαι\tVERB\t_\tMood=Ind\t0\troot\t_\t_

"""
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "comments.conllu"
            target.write_text(content, encoding="utf-8", newline="")

            result = transform_files(load_scenario(SCENARIO), (target,)).results[0]

        self.assertEqual(
            result.transformed,
            content.replace("\tobj\t", "\tobl:arg\t"),
        )
        self.assertEqual(result.match_count, 1)

    def test_sentence_annotation_action_is_not_discarded(self):
        content = """# sent_id = annotations.1
1\tλέγω\tλέγω\tVERB\t_\tMood=Ind\t0\troot\t_\t_

"""
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            scenario = directory_path / "annotation.ini"
            target = directory_path / "annotations.conllu"
            scenario.write_text(
                "func=/root/\tnone\t#S:review=needed\n",
                encoding="utf-8",
                newline="",
            )
            target.write_text(content, encoding="utf-8", newline="")

            result = transform_files(load_scenario(scenario), (target,)).results[0]

        self.assertIn("# review = needed\n", result.transformed)

    def test_default_selection_is_recursive_and_sorted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "data" / "annotation" / "a" / "first.conllu"
            second = root / "data" / "annotation" / "b" / "second.conllu"
            second.parent.mkdir(parents=True)
            first.parent.mkdir(parents=True)
            second.write_text("", encoding="utf-8")
            first.write_text("", encoding="utf-8")

            self.assertEqual(
                select_input_files(root),
                (first.resolve(), second.resolve()),
            )

    def test_explicit_input_selects_exactly_one_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            selected = root / "one.conllu"
            selected.write_text("", encoding="utf-8")

            self.assertEqual(select_input_files(root, selected), (selected.resolve(),))

    def test_preview_does_not_write_and_apply_does(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "input.conllu"
            original = (FIXTURES / "input.conllu").read_text(encoding="utf-8")
            expected = (FIXTURES / "expected.conllu").read_text(encoding="utf-8")
            target.write_text(original, encoding="utf-8", newline="")

            report = transform_files(load_scenario(SCENARIO), (target,))
            self.assertEqual(target.read_text(encoding="utf-8"), original)

            apply_report(report)
            self.assertEqual(target.read_text(encoding="utf-8"), expected)

    def test_cli_preview_is_default(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "input.conllu"
            original = (FIXTURES / "input.conllu").read_text(encoding="utf-8")
            target.write_text(original, encoding="utf-8", newline="")
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                exit_code = main(
                    [str(SCENARIO), "--input-file", str(target), "--root", str(ROOT)]
                )

            self.assertEqual(exit_code, 0)
            self.assertIn("Mode: preview", stdout.getvalue())
            self.assertIn("DepEdit version: 4.0.0.0", stdout.getvalue())
            self.assertIn("Matches/changed records: 2", stdout.getvalue())
            self.assertIn("Preview only; no files were written.", stdout.getvalue())
            self.assertEqual(target.read_text(encoding="utf-8"), original)

    def test_processing_failure_blocks_all_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            valid = directory_path / "valid.conllu"
            invalid = directory_path / "invalid.conllu"
            original = (FIXTURES / "input.conllu").read_text(encoding="utf-8")
            valid.write_text(original, encoding="utf-8", newline="")
            invalid.write_text("1\ttoo-few-columns\n\n", encoding="utf-8", newline="")

            report = transform_files(load_scenario(SCENARIO), (valid, invalid))

            self.assertEqual(len(report.changed_results), 1)
            self.assertEqual(len(report.failures), 1)
            with self.assertRaises(RuntimeError):
                apply_report(report)
            self.assertEqual(valid.read_text(encoding="utf-8"), original)

    def test_no_matches_is_a_review_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "expected.conllu"
            content = (FIXTURES / "expected.conllu").read_text(encoding="utf-8")
            target.write_text(content, encoding="utf-8", newline="")
            stdout = io.StringIO()
            stderr = io.StringIO()

            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = main(
                    [
                        str(SCENARIO),
                        "--input-file",
                        str(target),
                        "--root",
                        str(ROOT),
                        "--no-diff",
                    ]
                )

            self.assertEqual(exit_code, 1)
            self.assertIn("Changed files: 0", stdout.getvalue())
            self.assertIn("No matches found", stderr.getvalue())
            self.assertEqual(target.read_text(encoding="utf-8"), content)


if __name__ == "__main__":
    unittest.main()
