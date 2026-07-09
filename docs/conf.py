"""Sphinx configuration for the PokerHandEvaluator documentation.

This is a single documentation site covering the project as a whole. It is
organised into three sections:

* ``algorithm`` - the description of the underlying perfect-hash algorithm,
  sourced from ``Documentation/Algorithm.md``.
* ``cpp`` - usage and examples of the C/C++ library.
* ``python`` - usage and API reference of the ``phevaluator`` Python package.

The Python API reference is generated from the package's Google-style
docstrings via autodoc + napoleon. The native ``phevaluator._pheval`` C
extension is mocked so the documentation can be built without a C compiler or
the C sources.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Make the ``phevaluator`` package importable for autodoc. This file lives in
# ``docs`` at the repository root, so the package is one level up.
_DOCS_DIR = Path(__file__).parent.resolve()
_REPO_ROOT = _DOCS_DIR.parent
_PYTHON_DIR = _REPO_ROOT / "python"
sys.path.insert(0, str(_PYTHON_DIR))


def _read_version() -> str:
    """Read the package version from the project's ``pyproject.toml``."""
    text = (_PYTHON_DIR / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if match is None:
        msg = "Could not find the version in pyproject.toml"
        raise RuntimeError(msg)
    return match.group(1)


# -- Project information ------------------------------------------------------
project = "PokerHandEvaluator"
author = "Henry Lee"
project_copyright = "2018, Henry Lee"
release = _read_version()
version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

# The native C extension has no Python source to import, so mock it.
autodoc_mock_imports = ["phevaluator._pheval"]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
autodoc_typehints = "description"
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# The imported Algorithm.md relies on GitHub-style implicit heading anchors.
myst_heading_anchors = 4

# Algorithm.md (rendered as-is from the repository) uses in-page links to raw
# HTML ``<a name="...">`` anchors, which work at runtime (they are emitted
# verbatim) but cannot be resolved at build time. Silence those warnings
# instead of editing the canonical source document.
suppress_warnings = ["myst.xref_missing"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_title = f"PokerHandEvaluator {release}"
html_static_path = ["_static"]


def setup(app):  # noqa: ANN001, ANN201, D103
    # Algorithm.md uses ``pseudocode`` code fences, which is not a real Pygments
    # lexer. Register it as plain text so highlighting (and the -W build) works.
    from pygments.lexers.special import TextLexer

    app.add_lexer("pseudocode", TextLexer)
