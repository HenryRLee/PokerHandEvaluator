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

### pre-commit

You will need [pre-commit](https://pre-commit.com/) to format and lint your code.

* Install `pre-commit` using package manager such as `pip`, `apt` (Ubuntu), or `brew`
  (MacOS)
* Install `pre-commit` hooks with `pre-commit install`

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

We use GitHub Actions to automate various checks and tests for every Pull Request.
If the build, tests, type checking, or package installation fails, the workflow will
exit with a non-zero status code. Linting errors or files formatted by pre-commit
will cause the workflow to exit with status code 1. If any job exits with a non-zero
status code, merging or pushing to the repository will be blocked by GitHub Actions.

### Pre-commit Checks for Every Commit

The following pre-commit checks are performed:

* Prevent commits to the `master` or `develop` branches
* Check for merge conflicts
* Forbid submodules (if added)
* Lint files for encoding, line endings, tabs and more (for modified files)
* Display the differences between the original and formatted code, if any files
  are formatted by pre-commit

### CI Checks for C++

The following checks are performed:

* C++ build and unit tests
* Pre-commit checks:
  * Lint C++ code format according to the style specified in `.clang-format` (for
    modified files)

### CI Checks for Python

The following checks are performed:

* Python unit tests for Python 3.8 to 3.11
* Python type checking with `mypy` for Python 3.8
* Python package installation for Python 3.8 to 3.11
* Pre-commit checks:
  * Lint Python files with `Ruff` according to the configuration in `pyproject.toml`
    (if any Python files are modified, check all Python files)

### CI Checks for Certain File Types

Additional pre-commit checks are performed:

* Check YAML formatting (for modified files)
* Check TOML formatting (for modified files)
* Lint Markdown files with markdownlint (for modified files)

See more details:

* [GitHub Actions configurations](.github/workflows/ci.yml)
* [pre-commit configurations](.pre-commit-config.yaml)

If you have any questions, need further assistance, or want to report
a bug or suggest an enhancement, feel free to [open an issue](https://github.com/HenryRLee/PokerHandEvaluator/issues).
