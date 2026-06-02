from __future__ import annotations

import csv
import unittest  # noqa: TC003
from pathlib import Path
from typing import Callable
from typing import Iterator

TEST_DATA_DIR = Path(__file__).resolve().parents[2] / "test_data"


def _iter_rows(csv_path: Path) -> Iterator[tuple[list[str], int]]:
    with csv_path.open(encoding="UTF-8", newline="") as f:
        reader = csv.reader(f)
        try:
            next(reader)  # skip header
        except StopIteration:
            message = f"CSV file is empty (no header row): {csv_path}"
            raise ValueError(message) from None
        for row in reader:
            *cards, rank = row
            yield cards, int(rank)


def run_csv(
    test_case: unittest.TestCase,
    csv_path: Path,
    evaluate_cards: Callable[..., int],
    *,
    as_int: bool,
) -> None:
    """Run a CSV fixture file against an evaluator function."""
    if not csv_path.is_file():
        test_case.fail(f"Missing test data file: {csv_path}")
    for cards, expected_rank in _iter_rows(csv_path):
        args = [int(c) for c in cards] if as_int else cards
        actual = evaluate_cards(*args)
        if actual != expected_rank:
            test_case.fail(
                f"{csv_path.name}: cards={cards} expected={expected_rank} got={actual}"
            )
