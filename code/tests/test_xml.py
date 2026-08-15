from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from daphne_treebank.checks import check_xml


class XmlCheckTests(unittest.TestCase):
    def check_text(self, text: str):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.xml"
            path.write_text(text, encoding="utf-8")
            return check_xml(path)

    def test_accepts_well_formed_xml(self):
        self.assertEqual(self.check_text("<TEI><text/></TEI>"), [])

    def test_rejects_mismatched_tags(self):
        issues = self.check_text("<TEI><text></TEI>")
        self.assertEqual(len(issues), 1)
        self.assertIn("not well-formed XML", issues[0].message)


if __name__ == "__main__":
    unittest.main()
