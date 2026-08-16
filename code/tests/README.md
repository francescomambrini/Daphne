# Tests

Tests for maintained code belong here. Fixtures should be minimal examples that
exercise a specific behavior; complete treebanks and generated validator output
should not be copied into the test suite.

DepEdit scenario fixtures live under `fixtures/depedit/<scenario-id>/` and must
use the same stable identifier as the corresponding directory under
`code/rules/depedit/`.

Legacy files under `code/legacy/` are outside the supported test surface.

The test suite uses Python's standard `unittest` module. Its dependencies are
declared in the root `pyproject.toml` and resolved reproducibly by `uv.lock`.
From the repository root, synchronize the environment and run the tests with:

```bash
uv sync --locked
uv run python -m unittest discover -s code/tests -v
```
