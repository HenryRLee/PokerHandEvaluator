# PH Evaluator Python package (phevaluator)

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/HenryRLee/PokerHandEvaluator/Build%20and%20Test?color=green&logo=github)](https://github.com/HenryRLee/PokerHandEvaluator/actions/workflows/build-and-test.yml)
[![PyPI version](https://img.shields.io/pypi/v/phevaluator)](https://pypi.org/project/phevaluator/)
[![PyPI downloads](https://img.shields.io/pypi/dm/phevaluator)](https://shields.io/category/downloads)
[![Apache_2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/HenryRLee/PokerHandEvaluator/blob/master/python/LICENSE)

## Description

[PH Evaluator](https://github.com/HenryRLee/PokerHandEvaluator) is designed
for evaluating poker hands with more than 5 cards. Instead of traversing all
the combinations, it uses a perfect hash algorithm to get the hand strength
from a pre-computed hash table, which only costs very few CPU cycles and
considerably small memory (~100kb for the 7 card evaluation). With slight
modification, the same algorithm can be also applied to evaluating Omaha
poker hands.

The full API documentation is published at
<https://henryrlee.github.io/PokerHandEvaluator/python>.

## Installation

The library requires Python 3.10 or newer.

The evaluator is implemented as a C extension (`phevaluator._pheval`) that
wraps the C sources in the repository's [`cpp`](../cpp) directory, so a C
compiler and **pip 21.3 or newer** are required to build from source. Older
pip versions build out-of-tree and cannot reach the `cpp` directory.

* from release on PyPI

  ```shell
  pip install phevaluator
  ```

* from source code

  Build from within the repository (the sibling `cpp` directory is used to
  compile the extension):

  ```shell
  pip install .
  ```

  If you are using pip older than 21.3, either upgrade pip:

  ```shell
  pip install --upgrade pip
  ```

  or pass the `--use-feature=in-tree-build` flag so the build can access the
  `cpp` sources:

  ```shell
  pip install --use-feature=in-tree-build .
  ```

## Using the library

The main function is the `evaluate_cards` function.

```python
from phevaluator.evaluator import evaluate_cards

p1 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "Qc", "6c")
p2 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "2c", "9h")

# The rank is an integer from 1 (strongest) to 7462 (weakest), so a smaller
# value means a stronger hand. Player 2 has a stronger hand here.
print(f"The rank of the hand in player 1 is {p1}") # 292
print(f"The rank of the hand in player 2 is {p2}") # 236
```

The returned value is the rank of the hand among all 7462 distinct
five-card hands. It is identical to the return value of Cactus Kev's
evaluator: `1` is the best possible hand (a Royal Straight Flush) and `7462`
is the worst. A smaller value is always a stronger hand, so you can compare
two hands directly (e.g. `p2 < p1` means player 2 wins).

The function can take both numbers and card strings (with a format like: 'Ah' or
'2C'). Usage examples can be seen in [`examples.py`](examples.py).

### Omaha and Pot Limit Omaha

Omaha-style hands (five community cards followed by the hole cards) can be
evaluated with the dedicated functions:

```python
from phevaluator import evaluate_omaha_cards  # 4 hole cards
from phevaluator import evaluate_plo4_cards   # 4 hole cards (alias of Omaha)
from phevaluator import evaluate_plo5_cards   # 5 hole cards
from phevaluator import evaluate_plo6_cards   # 6 hole cards

# 5 community cards + 4 hole cards. The return value is a rank in the same
# 1 (strongest) to 7462 (weakest) scale as evaluate_cards, computed from the
# best five-card hand allowed by the Omaha rules.
evaluate_omaha_cards("4c", "5c", "6c", "7s", "8s", "2c", "9c", "As", "Kd")
```

`evaluate_plo5_cards` and `evaluate_plo6_cards` require the package to be built
with PLO5/PLO6 support. Their lookup tables are very large (hundreds of MB of
generated C source each), so they are **opt-in**: set the
`PHEVALUATOR_BUILD_PLO` environment variable when installing from the
repository.

```shell
# Build with PLO5 and PLO6 support (also accepts "5", "6", or "all")
PHEVALUATOR_BUILD_PLO=5,6 pip install .
```

Calling `evaluate_plo5_cards`/`evaluate_plo6_cards` on a package built without
the corresponding support raises `NotImplementedError`. `evaluate_plo4_cards`
(and `evaluate_omaha_cards`) are always available.

## Card Id

We can use an integer to represent a card. The two least significant bits
represent the 4 suits, ranging from 0-3. The rest of it represents the 13
ranks, ranging from 0-12.

More specifically, the ranks are:

deuce = 0, trey = 1, four = 2, five = 3, six = 4, seven = 5, eight = 6,
nine = 7, ten = 8, jack = 9, queen = 10, king = 11, ace = 12.

And the suits are:
club = 0, diamond = 1, heart = 2, spade = 3

So that you can use `rank * 4 + suit` to get the card ID.

Technically, it is fine to swap the suit values, as long as the suits are
uniquely mapped to the values 0, 1, 2, and 3. If you do swap the suit values,
make sure to update the mapping in the source code as well (`suit_map` in
[card.py](phevaluator/card.py)).

The complete card Id mapping can be found below. The rows are the ranks
from 2 to Ace, and the columns are the suits: club, diamond, heart and spade.

|      |    C |    D |    H |    S |
| ---: | ---: | ---: | ---: | ---: |
|    2 |    0 |    1 |    2 |    3 |
|    3 |    4 |    5 |    6 |    7 |
|    4 |    8 |    9 |   10 |   11 |
|    5 |   12 |   13 |   14 |   15 |
|    6 |   16 |   17 |   18 |   19 |
|    7 |   20 |   21 |   22 |   23 |
|    8 |   24 |   25 |   26 |   27 |
|    9 |   28 |   29 |   30 |   31 |
|    T |   32 |   33 |   34 |   35 |
|    J |   36 |   37 |   38 |   39 |
|    Q |   40 |   41 |   42 |   43 |
|    K |   44 |   45 |   46 |   47 |
|    A |   48 |   49 |   50 |   51 |

## Test

* The functionality of the evaluators is tested against CSV test data in the
  `test_data/` folder (generated by the C++ evaluator), covering five-card,
  six-card, seven-card, and PLO4 (Omaha) evaluations.
* The Card module is tested against the Card Id table documented above.

The tests import the compiled `phevaluator._pheval` extension, so build it
first (for example with an editable install, `pip install -e .`) and run the
tests from the repository root of the Python package:

```shell
python -m unittest discover -v
```

## Contributing

Thank you for your interest in contributing to the Python package of PHEvaluator!
To ensure a smooth contribution process, please follow the guidelines below.

### Requirements

* Python 3.10 or newer
* A C compiler (the evaluator is built as a C extension)

### Code style

* Follow the [Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html).
* Write type hints following [PEP 484](https://www.python.org/dev/peps/pep-0484/).
* Include docstrings following [PEP 257](https://www.python.org/dev/peps/pep-0257/).
* Lint and format code using `Ruff`.

### Development Setup

Install development dependencies:

```shell
pip install '.[dev]'
```

### Checking Changes

You can install the package from the source code in `editable` mode:

```shell
pip install -e .
```

This allows the installed package to automatically reflect changes made in the `phevaluator`
folder.

### Building the Package

To build the package, run the following command:

```shell
python -m build
```

This will create a `dist` folder containing the built package.

Install the built package for testing:

```shell
pip install dist/*.whl
```

Check whether your distribution's long description will render correctly on PyPI:

```shell
python -m twine check dist/*
```
