from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import yaml

from daphne_treebank.checks import check_catalog


class CatalogCheckTests(unittest.TestCase):
    def make_repository(self, catalog, schema=None):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        data = root / "data"
        data.mkdir()
        (data / "catalog.yaml").write_text(
            yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8"
        )
        (data / "catalog.schema.json").write_text(
            json.dumps(schema if schema is not None else {}), encoding="utf-8"
        )
        return temporary, root

    @staticmethod
    def record(path, *, role="primary", record_id="tlg0001.tlg001.test-grc1"):
        return {
            "id": record_id,
            "author_id": "tlg0001",
            "work_id": "tlg001",
            "edition_id": "test-grc1",
            "role": role,
            "files": [{"path": path}],
        }

    @staticmethod
    def touch(root: Path, relative_path: str):
        path = root / "data" / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# sent_id = test\n1\tx\tx\tX\t_\t_\t0\troot\t_\t_\n\n")

    def test_accepts_complete_catalog_and_legacy_backup_exception(self):
        primary = "annotation/tlg0001/tlg001/tlg0001.tlg001.test-grc1.conllu"
        backup = "annotation/tlg0001/tlg001/BAK_test.conllu"
        catalog = {
            "treebanks": [self.record(primary)],
            "path_exceptions": [
                {"path": backup, "role": "legacy_backup", "reason": "test backup"}
            ],
        }
        temporary, root = self.make_repository(catalog)
        self.addCleanup(temporary.cleanup)
        self.touch(root, primary)
        self.touch(root, backup)
        self.assertEqual(check_catalog(root), [])

    def test_allows_noncanonical_path_for_legacy_external_record(self):
        path = "annotation/legacy/weird-name.conllu"
        catalog = {
            "treebanks": [self.record(path, role="legacy_external")],
            "path_exceptions": [],
        }
        temporary, root = self.make_repository(catalog)
        self.addCleanup(temporary.cleanup)
        self.touch(root, path)
        self.assertEqual(check_catalog(root), [])

    def test_reports_duplicate_ids_and_uncataloged_files(self):
        path = "annotation/tlg0001/tlg001/tlg0001.tlg001.test-grc1.conllu"
        extra = "annotation/tlg0002/tlg001/extra.conllu"
        record = self.record(path)
        catalog = {"treebanks": [record, dict(record)], "path_exceptions": []}
        temporary, root = self.make_repository(catalog)
        self.addCleanup(temporary.cleanup)
        self.touch(root, path)
        self.touch(root, extra)
        messages = [issue.message for issue in check_catalog(root)]
        self.assertTrue(any(message.startswith("duplicate id:") for message in messages))
        self.assertIn(f"uncataloged CoNLL-U path: {extra}", messages)

    def test_reports_schema_error(self):
        catalog = {"treebanks": [], "path_exceptions": []}
        schema = {"type": "object", "required": ["missing"]}
        temporary, root = self.make_repository(catalog, schema)
        self.addCleanup(temporary.cleanup)
        messages = [issue.message for issue in check_catalog(root)]
        self.assertTrue(any(message.startswith("schema $:") for message in messages))


if __name__ == "__main__":
    unittest.main()
