# Contributing

Thank you for contributing to `PHEvaluator`! Here are some advices might be useful
for passing the code review.

## Basics

* Check out the latest code in `develop` branch. Also target your Pull Request on
  the `develop` branch.
* Follow these coding style guidelines:
  * For C++, follow the [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html).
  * For Python:
    * Follow the [Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html).
    * Write type hints following [PEP 484](https://www.python.org/dev/peps/pep-0484/).
    * Include docstrings following [PEP 257](https://www.python.org/dev/peps/pep-0257/).
  * For Markdown files, follow the [markdownlint rules](https://github.com/DavidAnson/markdownlint).
  * Ensure YAML and TOML files are valid and properly formatted.
  * An [.editorconfig](.editorconfig)
    file is provided, which [most editors support natively](https://editorconfig.org/),
    to help maintain consistent formatting.
* Split your work into multiple Pull Request if they are irrelevant, so that we can
  merge them independently (usually with squash merge).
* If you are planning to work on a large feature, it'd be helpful if we can
  understand your idea first, prior to getting your hands on the implementation.
  You may create a new issue or a new discussion.
* The GitHub Actions workflow automatically test your code and run linters before
  merging your Pull Request.
  If any issues are detected, the workflow logs will display detailed information
  about the problems and the necessary changes to resolve them.
* We recommend you to format, lint, build, and test your code locally before pushing
  your changes. This helps identify and fix issues quickly.

## Development Setup

Formatting and linting are enforced by GitHub Actions on every Pull Request (see
[Continuous Integration](#continuous-integration-ci-with-github-actions) below).
When a check finds an auto-fixable problem, the workflow posts an inline
suggestion on your Pull Request that you can apply with a single click. You can
also run the same tools locally before pushing, as described in the sections
below.

## C++ development

See more details: [README.md for C++](cpp/README.md)

Requirements:

* make, CMake, C++11 compiler, [clang-format](https://clang.llvm.org/docs/ClangFormat.html)

Code style:

* Specified in [.clang-format](cpp/.clang-format)
* Format code with `clang-format -i <file-path>`

Build:

```shell
cd cpp
mkdir -p build
cd build
cmake ..
make
```

Test:

```shell
cd cpp/build
./unit_tests
```

## Python development

See more details: [README.md for Python](python/README.md#contributing)

Requirements:

* Python 3.8, [Ruff](https://docs.astral.sh/ruff/), [mypy](https://mypy-lang.org/)

Code style:

* Specified in [pyproject.toml](python/pyproject.toml)
* Lint code with `ruff check`
* Format code with `ruff format`

Type check:

```shell
mypy .
```

Test:

```shell
python3 -m unittest discover -v
```

## Continuous Integration (CI) with GitHub Actions

We use GitHub Actions to automate various checks and tests for every Pull
Request. If the build, tests, type checking, or package installation fails, the
workflow will exit with a non-zero status code. Formatting and linting problems
also cause the workflow to fail. If any job exits with a non-zero status code,
merging your Pull Request will be blocked by GitHub Actions.

The [`Lint & Suggest`](.github/workflows/lint-suggest.yml) workflow runs the
formatters and linters and posts the required changes as inline
**suggestions** you can apply with one click. Pull Requests opened from forks
receive the same suggestions from a separate
[`Lint & Suggest (forks)`](.github/workflows/lint-suggest-fork.yml) workflow.
All checks still run and block on failure for fork Pull Requests.

### Lint & Suggest checks

* **File hygiene** (all text files): byte-order-marker removal, line endings
  normalised to LF, tabs replaced with spaces (Makefiles excluded), trailing
  whitespace removal, and a final newline at end of file.
* **TOML & YAML**: validity checks.
* **C++**: `clang-format` according to [.clang-format](cpp/.clang-format)
  (excluding the generated `cpp/src/hashtable*` and `cpp/src/tables*` files).
* **Markdown**: `markdownlint` according to [.markdownlint.yaml](.markdownlint.yaml).
* **Python**: `ruff check` and `ruff format` according to
  [pyproject.toml](python/pyproject.toml).
* **Python type checking**: `mypy`.
* **Repo guards**: merge-conflict detection, private-key detection, and
  forbidding submodules.

The C++, Markdown, and Python formatting/lint jobs only inspect the files
changed in your Pull Request.

### CI checks

The [`CI`](.github/workflows/ci.yml) workflow additionally performs:

* C++ build and unit tests
* Python unit tests for Python 3.8 to 3.11
* Python package installation for Python 3.8 to 3.11

See more details:

* [GitHub Actions configurations](.github/workflows/ci.yml)
* [Lint & Suggest configurations](.github/workflows/lint-suggest.yml)

If you have any questions, need further assistance, or want to report
a bug or suggest an enhancement, feel free to [open an issue](https://github.com/HenryRLee/PokerHandEvaluator/issues).
