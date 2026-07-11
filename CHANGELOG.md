# Changelog

All notable changes to this project are documented in this file.

## [0.6.1] - Unreleased

_No changes so far._

## [0.6.0] - 2026-07-11

### C/C++

- Added PLO5 and PLO6 evaluators.
- Fixed a bug in the C++ hand (`Rank`) comparison operators.
- Removed the `Hand` class (`phevaluator/hand.h` header) and the `EvaluateHand`
  function.

New public functions and types:

- C:
  - `evaluate_plo4_cards` (alias of `evaluate_omaha_cards`)
  - `evaluate_plo5_cards`
  - `evaluate_plo6_cards`
- C++:
  - `EvaluatePlo4Cards` (alias of `EvaluateOmahaCards`)
  - `EvaluatePlo5Cards`
  - `EvaluatePlo6Cards`

Removed public functions and types:

- C++: `EvaluateHand`, `Hand` class.

### Python

- Evaluation code is now backed by the C-compiled library.
- Added PLO5 and PLO6 evaluation.
- Supported Python versions changed to Python 3.10 - 3.14.

New public functions:

- `evaluate_5cards`
- `evaluate_6cards`
- `evaluate_7cards`
- `evaluate_plo4_cards` (alias of `evaluate_omaha_cards`)
- `evaluate_plo5_cards`
- `evaluate_plo6_cards`

## [0.5.3.1] - 2024-03-21

### Python

- Update the example usage in README.md and the website.

## [0.5.3] - 2024-03-14

### Python

- Separate package to improve memory usage.

## [0.5.2] - 2023-03-10

### Python

- Fix the hint of list type in Python 3.7.

## [0.5.1] - 2022-04-22

### Python

- Fix package not containing entire codes and omaha data.

## [0.5.0.4] - 2021-10-31

### Python

- Fix package not containing entire codes and omaha data.

## [0.5.0] - 2021-10-19

### Python

- Remove Omaha hand evaluation from method `evaluate_cards`.
- Remove methods `evaluate_5cards`, `evaluate_6cards` and `evaluate_7cards`.

## [0.4.0.3] - 2021-10-18

### Python

- Build with setuptools.

## [0.4.0.2] - 2021-10-16

### Python

- Create PyPI package phevaluator.

## [0.4.0.1] - 2021-10-11

### Python

- New source code structure and packaging methods (no functional changes).

## [0.4.0] - 2021-10-06

### C/C++

- Add `describeCard`, `describeSuit`, and `describeRank` methods for `Card`.
- Change `describeSampleHand` to return a string with no space delimiters.

### Python

- Remove 8-card and 9-card evaluations.
- Add Omaha evaluation.
- Add `describe_rank`, `describe_suit`, and `describe_card` for the Card class.
- Fix and improve the `table_tests` scripts.

### Misc

- Use GitHub workflow as CI.

## [0.3.1] - 2020-05-25

### C/C++

- Use O3 optimization.

## [0.3.0] - 2020-05-24

### C/C++

- Add evaluation for Omaha hands.

## [0.2.0] - 2019-11-25

### C++

- Add Hand and Rank types.
- Add the `EvaluateHand` method.
- Add multiple methods to describe a Rank.

### C

- Add multiple methods to describe a Rank.
- Add the 7462 table.

### Python

- Refactor the table test code.

## [0.1.0] - 2019-11-20

- Supports Poker Hand Evaluation from 5 to 9 cards.
- Supports C, C++ and Python languages.
