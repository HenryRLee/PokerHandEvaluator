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
"""

from __future__ import annotations

import shutil
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

# C sources implementing the evaluator and its lookup tables.
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


def _cpp_sources_available() -> bool:
    """Return whether the real C sources are present in the sibling ``cpp``.

    A mere ``cpp/src`` directory is not enough (stray/empty directories can
    exist in temporary build roots), so an actual source file is checked.
    """
    return (CPP_SRC / _CPP_SOURCES[0]).is_file()


def _vendored_sources_complete() -> bool:
    """Return whether every required C source and header is already vendored."""
    required = _CPP_SOURCES + _CPP_PRIVATE_HEADERS
    if not all((VENDOR_SRC / name).is_file() for name in required):
        return False
    return (VENDOR_INCLUDE / "phevaluator" / "phevaluator.h").is_file()


def _vendor_cpp_sources() -> None:
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
        return

    if _vendored_sources_complete():
        return

    msg = (
        f"Cannot find the C sources at {CPP_SRC}. Build the package from "
        "within the PokerHandEvaluator repository so the sibling 'cpp' "
        "directory is available, or build from an sdist that bundles them."
    )
    raise FileNotFoundError(msg)


_vendor_cpp_sources()

sources = ["phevaluator/_pheval.c"]
sources += [f"_pheval_csrc/src/{name}" for name in _CPP_SOURCES]

pheval_extension = Extension(
    "phevaluator._pheval",
    sources=sources,
    include_dirs=["_pheval_csrc/include"],
)

setup(ext_modules=[pheval_extension])
