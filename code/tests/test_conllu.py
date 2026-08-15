from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from daphne_treebank.checks import check_conllu


VALID_SENTENCE = """# sent_id = test.1
# text = A test.
1\tA\ta\tDET\t_\t_\t2\tdet\t_\t_
2\ttest\ttest\tNOUN\t_\tNumber=Sing\t0\troot\t0:root\tSpaceAfter=No
3\t.\t.\tPUNCT\t_\t_\t2\tpunct\t2:punct\t_

"""


class ConlluCheckTests(unittest.TestCase):
    def check_text(self, text: str):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.conllu"
            path.write_text(text, encoding="utf-8", newline="")
            return check_conllu(path)

    def test_accepts_well_formed_sentence(self):
        self.assertEqual(self.check_text(VALID_SENTENCE), [])

    def test_accepts_unspecified_annotation_and_non_nfc_text(self):
        text = """# sent_id = partial.1
# text = ά
1	ά	_	_	_	_	_	_	_	_

"""
        self.assertEqual(self.check_text(text), [])

    def test_accepts_multiword_token_and_empty_node(self):
        text = """# sent_id = test.2
# text = can't go
1-2\tcan't\t_\t_\t_\t_\t_\t_\t_\t_
1\tca\tcan\tAUX\t_\t_\t3\taux\t3:aux\t_
2\tn't\tnot\tPART\t_\t_\t3\tadvmod\t3:advmod\t_
3\tgo\tgo\tVERB\t_\t_\t0\troot\t0:root\t_
3.1\tleave\tleave\tVERB\t_\t_\t_\t_\t3:conj\t_

"""
        self.assertEqual(self.check_text(text), [])

    def test_rejects_wrong_column_count(self):
        text = "# sent_id = bad\n1\ttoo\tfew\tfields\n\n"
        messages = [issue.message for issue in self.check_text(text)]
        self.assertTrue(any("instead of 10" in message for message in messages))

    def test_rejects_comment_after_token(self):
        text = VALID_SENTENCE.replace(
            "2\ttest", "# misplaced comment\n2\ttest"
        )
        messages = [issue.message for issue in self.check_text(text)]
        self.assertIn("comment occurs after a token line", messages)

    def test_rejects_missing_final_blank_line(self):
        messages = [issue.message for issue in self.check_text(VALID_SENTENCE.rstrip("\n"))]
        self.assertTrue(any("final sentence" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
