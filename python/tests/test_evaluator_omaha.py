from __future__ import annotations

import csv
import unittest
from pathlib import Path
from typing import Iterator

from phevaluator import Card
from phevaluator import evaluate_omaha_cards

TEST_DATA_DIR = Path(__file__).resolve().parents[2] / "test"


def _iter_rows(csv_path: Path) -> Iterator[tuple[list[str], int]]:
    with csv_path.open(encoding="UTF-8", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            *cards, rank = row
            yield cards, int(rank)


class TestEvaluatorOmaha(unittest.TestCase):
    def test_omaha_example(self) -> None:
        # fmt: off
        rank1 = evaluate_omaha_cards(
            "4c", "5c", "6c", "7s", "8s", # community cards
            "2c", "9c", "As", "Kd",       # player hole cards
        )

        rank2 = evaluate_omaha_cards(
            "4c", "5c", "6c", "7s", "8s", # community cards
            "6s", "9s", "Ts", "Js",       # player hole cards
        )
        # fmt: on

        self.assertEqual(rank1, 1578)
        self.assertEqual(rank2, 1604)

    def _run_csv(self, filename: str, *, as_int: bool) -> None:
        csv_path = TEST_DATA_DIR / "plo4" / filename
        if not csv_path.is_file():
            self.skipTest(f"Missing test data file: {csv_path}")
        for cards, expected_rank in _iter_rows(csv_path):
            args = [int(c) for c in cards] if as_int else cards
            actual = evaluate_omaha_cards(*args)
            if actual != expected_rank:
                self.fail(
                    f"{csv_path.name}: cards={cards} "
                    f"expected={expected_rank} got={actual}"
                )

    def test_plo4_id(self) -> None:
        self._run_csv("id_input_tests.csv", as_int=True)

    def test_plo4_string(self) -> None:
        self._run_csv("string_input_tests.csv", as_int=False)

    def test_evaluator_interface(self) -> None:
        # int, str and Card can be passed to evaluate_omaha_cards()
        # fmt: off
        rank1 = evaluate_omaha_cards(
            48, 49, 47, 43, 35, # community cards
            51, 50, 39, 34,     # hole cards
        )
        rank2 = evaluate_omaha_cards(
            "Ac", "Ad", "Ks", "Qs", "Ts", # community cards
            "As", "Ah", "Js", "Th",       # hole cards
        )
        rank3 = evaluate_omaha_cards(
            "AC", "AD", "KS", "QS", "TS", # community cards
            "AS", "AH", "JS", "TH",       # hole cards
        )
        rank4 = evaluate_omaha_cards(
            Card("Ac"), Card("Ad"), Card("Ks"), Card("Qs"), Card("Ts"), # community cards  # noqa: E501
            Card("As"), Card("Ah"), Card("Js"), Card("Th"),             # hole cards
        )
        rank5 = evaluate_omaha_cards(
            48, "Ad", "KS", Card(43), Card("Ts"), # community cards
            Card("AS"), 50, "Js", "TH",           # hole cards
        )
        # fmt: on
        self.assertEqual(rank1, rank2)
        self.assertEqual(rank1, rank3)
        self.assertEqual(rank1, rank4)
        self.assertEqual(rank1, rank5)
