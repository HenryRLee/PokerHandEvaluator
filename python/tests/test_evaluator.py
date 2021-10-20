import json
import os
import unittest

from phevaluator import Card, evaluate_cards, evaluate_omaha_cards

CARDS_FILE_5 = os.path.join(os.path.dirname(__file__), "cardfiles/5cards.json")
CARDS_FILE_6 = os.path.join(os.path.dirname(__file__), "cardfiles/6cards.json")
CARDS_FILE_7 = os.path.join(os.path.dirname(__file__), "cardfiles/7cards.json")


class TestEvaluator(unittest.TestCase):
    def test_example(self):
        rank1 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "Qc", "6c")
        rank2 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "2c", "9h")

        self.assertEqual(rank1, 292)
        self.assertEqual(rank2, 236)
        self.assertLess(rank2, rank1)

    def test_omaha_example(self):
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

    def test_5cards(self):
        with open(CARDS_FILE_5, "r", encoding="UTF-8") as read_file:
            hand_dict = json.load(read_file)
            for key, value in hand_dict.items():
                self.assertEqual(evaluate_cards(*key.split()), value)

    def test_6cards(self):
        with open(CARDS_FILE_6, "r", encoding="UTF-8") as read_file:
            hand_dict = json.load(read_file)
            for key, value in hand_dict.items():
                self.assertEqual(evaluate_cards(*key.split()), value)

    def test_7cards(self):
        with open(CARDS_FILE_7, "r", encoding="UTF-8") as read_file:
            hand_dict = json.load(read_file)
            for key, value in hand_dict.items():
                self.assertEqual(evaluate_cards(*key.split()), value)

    def test_evaluator_interface(self):
        # int, str and Card can be passed to evaluate_cards()
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
