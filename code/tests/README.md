# Tests

Tests for maintained code belong here. Fixtures should be minimal examples that
exercise a specific behavior; complete treebanks and generated validator output
should not be copied into the test suite.

Legacy files under `code/legacy/` are outside the supported test surface.

The test suite uses Python's standard `unittest` module. Catalog checks depend on
the pinned packages in `code/requirements-checks.txt`. Run it from the repository
root with:

```bash
python -m pip install --requirement code/requirements-checks.txt
PYTHONPATH=code/src python -m unittest discover -s code/tests -v
```
