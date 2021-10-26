import random
import unittest
from itertools import combinations

from phevaluator import (
    Card,
    _evaluate_cards,
    _evaluate_omaha_cards,
    evaluate_omaha_cards,
)


def sample_card(size: int) -> list[int]:
    """Sample random cards with size."""
    return random.sample(range(52), k=size)


def evaluate_omaha_exhaustive(*cards: int) -> int:
    """Evaluate omaha cards with `_evaluate_cards`."""
    community_cards = cards[:5]
    hole_cards = cards[5:]
    best_rank = min(
        _evaluate_cards(*selected_c_cards, *selected_h_cards)
        for selected_c_cards in combinations(community_cards, 3)
        for selected_h_cards in combinations(hole_cards, 2)
    )
    return best_rank


class TestEvaluatorOmaha(unittest.TestCase):
    def test_omaha(self):
        """Compare the evaluation between `_evaluate_omaha_cards` and `_evaluate_cards`"""
        total = 10000
        for _ in range(total):
            cards = sample_card(9)
            with self.subTest(cards):
                self.assertEqual(
                    _evaluate_omaha_cards(*cards), evaluate_omaha_exhaustive(*cards)
                )

    def test_evaluator_interface(self):
        # int, str and Card can be passed to evaluate_omaha_cards()
        # fmt: off
        rank1 = evaluate_omaha_cards(
            48, 49, 47, 43, 35, # community cards
            51, 50, 39, 34      # hole cards
        )
        rank2 = evaluate_omaha_cards(
            "Ac", "Ad", "Ks", "Qs", "Ts", # community cards
            "As", "Ah", "Js", "Th"        # hole cards
        )
        rank3 = evaluate_omaha_cards(
            "AC", "AD", "KS", "QS", "TS", # community cards
            "AS", "AH", "JS", "TH"        # hole cards
        )
        rank4 = evaluate_omaha_cards(
            Card("Ac"), Card("Ad"), Card("Ks"), Card("Qs"), Card("Ts"), # community cards
            Card("As"), Card("Ah"), Card("Js"), Card("Th")              # hole cards
        )
        rank5 = evaluate_omaha_cards(
            48, "Ad", "KS", Card(43), Card("Ts"), # community cards
            Card("AS"), 50, "Js", "TH"            # hole cards
        )
        # fmt: on
        self.assertEqual(rank1, rank2)
        self.assertEqual(rank1, rank3)
        self.assertEqual(rank1, rank4)
        self.assertEqual(rank1, rank5)
