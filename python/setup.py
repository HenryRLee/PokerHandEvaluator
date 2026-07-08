"""Build script for the native PH Evaluator extension.

The package metadata is defined in ``pyproject.toml``. This module compiles the
``phevaluator._pheval`` C extension, which wraps the C implementation of the
evaluator that lives in the sibling ``cpp`` directory.

setuptools requires that every extension source lives *inside* the project
root (it refuses paths that escape it, e.g. ``../cpp/...``). The C sources are
therefore vendored into a build-local directory (``_pheval_csrc``) at build
time by copying them from ``../cpp``. This keeps the wheel build self-contained
without committing a duplicate of the (large) generated tables to the Python
package.

The PLO5 and PLO6 evaluators depend on very large lookup tables (hundreds of MB
of source each), so they are opt-in. Set the ``PHEVALUATOR_BUILD_PLO``
environment variable to select which ones to build, for example::

    PHEVALUATOR_BUILD_PLO=5,6 pip install .
    PHEVALUATOR_BUILD_PLO=all pip install .

The PLO4 (Omaha) evaluator is always built.
"""

from __future__ import annotations

import os
import re
import shutil
import tarfile
from pathlib import Path

from setuptools import Extension
from setuptools import setup

HERE = Path(__file__).parent.resolve()
CPP_DIR = HERE.parent / "cpp"
CPP_SRC = CPP_DIR / "src"
CPP_INCLUDE = CPP_DIR / "include"

# Build-local directory (inside the project root) holding the vendored C
# sources and headers. It is regenerated on every build and is git-ignored.
VENDOR_DIR = HERE / "_pheval_csrc"
VENDOR_SRC = VENDOR_DIR / "src"
VENDOR_INCLUDE = VENDOR_DIR / "include"

# Private headers in ``cpp/src`` that the C sources include via "" includes.
_CPP_PRIVATE_HEADERS = ["hash.h", "tables.h"]

# C sources always compiled into the extension (5/6/7-card and PLO4/Omaha).
_CPP_SOURCES = [
    "evaluator5.c",
    "evaluator6.c",
    "evaluator7.c",
    "evaluator_plo4.c",
    "hash.c",
    "hashtable.c",
    "hashtable5.c",
    "hashtable6.c",
    "hashtable7.c",
    "dptables.c",
    "tables_bitwise.c",
    "tables_plo4.c",
]

# Opt-in PLO variants. Each maps to the evaluator source, the (tar-packed)
# table source, its tarball, and the macro that enables it in _pheval.c.
_PLO_VARIANTS = {
    "plo5": {
        "evaluator": "evaluator_plo5.c",
        "table": "tables_plo5.c",
        "tarball": "tables_plo5.tar.gz",
        "macro": "PHEVALUATOR_HAVE_PLO5",
    },
    "plo6": {
        "evaluator": "evaluator_plo6.c",
        "table": "tables_plo6.c",
        "tarball": "tables_plo6.tar.gz",
        "macro": "PHEVALUATOR_HAVE_PLO6",
    },
}


def _requested_plo_variants() -> list[str]:
    """Return the PLO variants to build based on ``PHEVALUATOR_BUILD_PLO``."""
    raw = os.environ.get("PHEVALUATOR_BUILD_PLO", "").strip().lower()
    if not raw:
        return []
    if raw in {"1", "all", "true", "yes"}:
        return list(_PLO_VARIANTS)
    variants = []
    for token in re.split(r"[,\s]+", raw):
        name = token if token.startswith("plo") else f"plo{token}"
        if name in _PLO_VARIANTS and name not in variants:
            variants.append(name)
    return variants


def _cpp_sources_available() -> bool:
    """Return whether the real C sources are present in the sibling ``cpp``.

    A mere ``cpp/src`` directory is not enough (stray/empty directories can
    exist in temporary build roots), so an actual source file is checked.
    """
    return (CPP_SRC / _CPP_SOURCES[0]).is_file()


def _extract_table(tarball: str, table: str) -> None:
    """Extract a single tar-packed table source into the vendored src dir."""
    with tarfile.open(CPP_SRC / tarball) as tf:
        extracted = tf.extractfile(table)
        if extracted is None:
            msg = f"{table} not found in {tarball}"
            raise FileNotFoundError(msg)
        (VENDOR_SRC / table).write_bytes(extracted.read())


def _vendor_cpp_sources(variants: list[str]) -> None:
    """Make the required C sources and headers available inside the project.

    When building from the repository the sources are copied from the sibling
    ``cpp`` directory. When building from an sdist that already bundles them
    (so ``cpp`` is unavailable), the existing vendored copy is reused.
    """
    if _cpp_sources_available():
        VENDOR_SRC.mkdir(parents=True, exist_ok=True)
        for name in _CPP_SOURCES + _CPP_PRIVATE_HEADERS:
            shutil.copy2(CPP_SRC / name, VENDOR_SRC / name)
        shutil.copytree(CPP_INCLUDE, VENDOR_INCLUDE, dirs_exist_ok=True)
        for name in variants:
            variant = _PLO_VARIANTS[name]
            shutil.copy2(
                CPP_SRC / variant["evaluator"], VENDOR_SRC / variant["evaluator"]
            )
            _extract_table(variant["tarball"], variant["table"])
        return

    # Building without access to ``cpp`` (e.g. from an sdist): the sources must
    # already be vendored/bundled.
    required = _CPP_SOURCES + _CPP_PRIVATE_HEADERS
    for name in variants:
        variant = _PLO_VARIANTS[name]
        required += [variant["evaluator"], variant["table"]]
    missing = [name for name in required if not (VENDOR_SRC / name).is_file()]
    if missing or not (VENDOR_INCLUDE / "phevaluator" / "phevaluator.h").is_file():
        msg = (
            f"Cannot find the C sources at {CPP_SRC}. Build the package from "
            "within the PokerHandEvaluator repository so the sibling 'cpp' "
            "directory is available. Note that PLO5/PLO6 tables are only "
            "available when building from the repository."
        )
        raise FileNotFoundError(msg)


_variants = _requested_plo_variants()
_vendor_cpp_sources(_variants)

sources = ["phevaluator/_pheval.c"]
sources += [f"_pheval_csrc/src/{name}" for name in _CPP_SOURCES]
define_macros = []
for _name in _variants:
    _variant = _PLO_VARIANTS[_name]
    sources.append(f"_pheval_csrc/src/{_variant['evaluator']}")
    sources.append(f"_pheval_csrc/src/{_variant['table']}")
    define_macros.append((_variant["macro"], "1"))

pheval_extension = Extension(
    "phevaluator._pheval",
    sources=sources,
    include_dirs=["_pheval_csrc/include"],
    define_macros=define_macros,
)

setup(ext_modules=[pheval_extension])
