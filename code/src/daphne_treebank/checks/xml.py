from __future__ import annotations

import xml.etree.ElementTree as ElementTree
from pathlib import Path

from .model import Issue


def check_xml(path: Path) -> list[Issue]:
    """Check that an XML file can be parsed as a well-formed document."""

    try:
        ElementTree.parse(path)
    except ElementTree.ParseError as error:
        line = error.position[0] if error.position else None
        return [Issue(path, f"not well-formed XML: {error}", line)]
    except OSError as error:
        return [Issue(path, f"cannot read file: {error}")]
    return []
