from __future__ import annotations

import csv
import unittest
from pathlib import Path
from typing import Iterator

from phevaluator import Card
from phevaluator import evaluate_cards

TEST_DATA_DIR = Path(__file__).resolve().parents[2] / "test"


def _iter_rows(csv_path: Path) -> Iterator[tuple[list[str], int]]:
    with csv_path.open(encoding="UTF-8", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            *cards, rank = row
            yield cards, int(rank)


class TestEvaluator(unittest.TestCase):
    def test_example(self) -> None:
        rank1 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "Qc", "6c")
        rank2 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "2c", "9h")

        self.assertEqual(rank1, 292)
        self.assertEqual(rank2, 236)
        self.assertLess(rank2, rank1)

    def _run_csv(self, subdir: str, filename: str, *, as_int: bool) -> None:
        csv_path = TEST_DATA_DIR / subdir / filename
        if not csv_path.is_file():
            self.skipTest(f"Missing test data file: {csv_path}")
        for cards, expected_rank in _iter_rows(csv_path):
            args = [int(c) for c in cards] if as_int else cards
            actual = evaluate_cards(*args)
            if actual != expected_rank:
                self.fail(
                    f"{csv_path.name}: cards={cards} "
                    f"expected={expected_rank} got={actual}"
                )

    def test_five_id(self) -> None:
        self._run_csv("five", "id_input_tests.csv", as_int=True)

    def test_five_string(self) -> None:
        self._run_csv("five", "string_input_tests.csv", as_int=False)

    def test_six_id(self) -> None:
        self._run_csv("six", "id_input_tests.csv", as_int=True)

    def test_six_string(self) -> None:
        self._run_csv("six", "string_input_tests.csv", as_int=False)

    def test_seven_id(self) -> None:
        self._run_csv("seven", "id_input_tests.csv", as_int=True)

    def test_seven_string(self) -> None:
        self._run_csv("seven", "string_input_tests.csv", as_int=False)

    def test_evaluator_interface(self) -> None:
        rank1 = evaluate_cards(1, 2, 3, 32, 48)
        rank2 = evaluate_cards("2d", "2h", "2s", "Tc", "Ac")
        rank3 = evaluate_cards("2D", "2H", "2S", "TC", "AC")
        rank4 = evaluate_cards(
            Card("2d"), Card("2h"), Card("2s"), Card("Tc"), Card("Ac")
        )
        rank5 = evaluate_cards(1, "2h", "2S", Card(32), Card("Ac"))

        self.assertEqual(rank1, rank2)
        self.assertEqual(rank1, rank3)
        self.assertEqual(rank1, rank4)
        self.assertEqual(rank1, rank5)
