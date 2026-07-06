from __future__ import annotations

import unittest

from phevaluator import Card
from phevaluator import _pheval
from phevaluator import evaluate_omaha_cards
from phevaluator import evaluate_plo4_cards
from phevaluator import evaluate_plo5_cards
from phevaluator import evaluate_plo6_cards

from ._csv_fixtures import TEST_DATA_DIR
from ._csv_fixtures import run_csv

_PLO5_BUILT = hasattr(_pheval, "evaluate_plo5_cards")
_PLO6_BUILT = hasattr(_pheval, "evaluate_plo6_cards")


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
        run_csv(self, csv_path, evaluate_omaha_cards, as_int=as_int)

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


class TestEvaluatorPlo(unittest.TestCase):
    def test_plo4_example(self) -> None:
        # evaluate_plo4_cards is equivalent to evaluate_omaha_cards.
        rank = evaluate_plo4_cards("4c", "5c", "6c", "7s", "8s", "2c", "9c", "As", "Kd")
        self.assertEqual(rank, 1578)
        self.assertEqual(
            rank,
            evaluate_omaha_cards("4c", "5c", "6c", "7s", "8s", "2c", "9c", "As", "Kd"),
        )

    @unittest.skipUnless(_PLO5_BUILT, "built without PLO5 support")
    def test_plo5_example(self) -> None:
        # fmt: off
        rank1 = evaluate_plo5_cards(
            "4c", "5c", "6c", "7s", "8s",  # community cards
            "2c", "9c", "As", "Kd", "Jh",  # player hole cards
        )
        rank2 = evaluate_plo5_cards(
            "4c", "5c", "6c", "7s", "8s",  # community cards
            "6s", "9s", "Ts", "Js", "2s",  # player hole cards
        )
        # fmt: on
        self.assertEqual(rank1, 1578)
        self.assertEqual(rank2, 1604)

    @unittest.skipUnless(_PLO5_BUILT, "built without PLO5 support")
    def test_plo5_id(self) -> None:
        csv_path = TEST_DATA_DIR / "plo5" / "id_input_tests.csv"
        run_csv(self, csv_path, evaluate_plo5_cards, as_int=True)

    @unittest.skipUnless(_PLO5_BUILT, "built without PLO5 support")
    def test_plo5_string(self) -> None:
        csv_path = TEST_DATA_DIR / "plo5" / "string_input_tests.csv"
        run_csv(self, csv_path, evaluate_plo5_cards, as_int=False)

    @unittest.skipUnless(_PLO6_BUILT, "built without PLO6 support")
    def test_plo6_example(self) -> None:
        # fmt: off
        rank1 = evaluate_plo6_cards(
            "4c", "5c", "6c", "7s", "8s",        # community cards
            "2c", "9c", "As", "Kd", "Jh", "8d",  # player hole cards
        )
        rank2 = evaluate_plo6_cards(
            "4c", "5c", "6c", "7s", "8s",        # community cards
            "6s", "9s", "Ts", "Js", "2s", "2d",  # player hole cards
        )
        # fmt: on
        self.assertEqual(rank1, 1578)
        self.assertEqual(rank2, 1604)

    @unittest.skipUnless(_PLO6_BUILT, "built without PLO6 support")
    def test_plo6_id(self) -> None:
        csv_path = TEST_DATA_DIR / "plo6" / "id_input_tests.csv"
        run_csv(self, csv_path, evaluate_plo6_cards, as_int=True)

    @unittest.skipUnless(_PLO6_BUILT, "built without PLO6 support")
    def test_plo6_string(self) -> None:
        csv_path = TEST_DATA_DIR / "plo6" / "string_input_tests.csv"
        run_csv(self, csv_path, evaluate_plo6_cards, as_int=False)
