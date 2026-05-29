from __future__ import annotations

import unittest
from typing import ClassVar

from phevaluator import Card


class TestCard(unittest.TestCase):
    # The Card Id table from README.md. Each card has a lowercase name, an
    # uppercase name, and an integer id. Rows are ranks (2..A), columns are
    # suits (C, D, H, S).
    # fmt: off
    testcases: ClassVar[list[tuple[str, str, int]]] = [
        ("2c", "2C",  0), ("2d", "2D",  1), ("2h", "2H",  2), ("2s", "2S",  3),
        ("3c", "3C",  4), ("3d", "3D",  5), ("3h", "3H",  6), ("3s", "3S",  7),
        ("4c", "4C",  8), ("4d", "4D",  9), ("4h", "4H", 10), ("4s", "4S", 11),
        ("5c", "5C", 12), ("5d", "5D", 13), ("5h", "5H", 14), ("5s", "5S", 15),
        ("6c", "6C", 16), ("6d", "6D", 17), ("6h", "6H", 18), ("6s", "6S", 19),
        ("7c", "7C", 20), ("7d", "7D", 21), ("7h", "7H", 22), ("7s", "7S", 23),
        ("8c", "8C", 24), ("8d", "8D", 25), ("8h", "8H", 26), ("8s", "8S", 27),
        ("9c", "9C", 28), ("9d", "9D", 29), ("9h", "9H", 30), ("9s", "9S", 31),
        ("Tc", "TC", 32), ("Td", "TD", 33), ("Th", "TH", 34), ("Ts", "TS", 35),
        ("Jc", "JC", 36), ("Jd", "JD", 37), ("Jh", "JH", 38), ("Js", "JS", 39),
        ("Qc", "QC", 40), ("Qd", "QD", 41), ("Qh", "QH", 42), ("Qs", "QS", 43),
        ("Kc", "KC", 44), ("Kd", "KD", 45), ("Kh", "KH", 46), ("Ks", "KS", 47),
        ("Ac", "AC", 48), ("Ad", "AD", 49), ("Ah", "AH", 50), ("As", "AS", 51),
    ]
    # fmt: on

    def test_card_equality(self) -> None:
        for name, capital_name, number in self.testcases:
            # equality between cards
            # e.g. Card("2c") == Card(0)
            self.assertEqual(Card(name), Card(number))
            # e.g. Card("2C") == Card(0)
            self.assertEqual(Card(capital_name), Card(number))
            # e.g. Card(Card(0)) == Card(0)
            self.assertEqual(Card(Card(number)), Card(number))

            # equality between Card and int
            self.assertEqual(Card(number), number)  # e.g. Card(0) == 0

    def test_card_immutability(self) -> None:
        # Once a Card is assigned or constructed from another Card,
        # it's not affected by any changes to source variable
        c_source = Card(1)
        c_assign = c_source
        c_construct = Card(c_source)

        c_source = Card(2)

        self.assertNotEqual(c_source, Card(1))
        self.assertEqual(c_assign, Card(1))
        self.assertEqual(c_construct, Card(1))

    def test_card_describe(self) -> None:
        for name, capital_name, number in self.testcases:
            rank, suit, *_ = tuple(name)
            c_name = Card(name)
            c_capital_name = Card(capital_name)
            c_number = Card(number)
            c_construct = Card(c_number)

            # Card("2c").describe_rank() == "2"
            self.assertEqual(c_name.describe_rank(), rank)
            # Card("2c").describe_suit() == "c"
            self.assertEqual(c_name.describe_suit(), suit)

            # Card("2c").describe_card() == "2c"
            self.assertEqual(c_name.describe_card(), name)

            # Card("2C").describe_card() == "2c"
            self.assertEqual(c_capital_name.describe_card(), name)
            # Card("2C").describe_card() != "2C"
            self.assertNotEqual(c_capital_name.describe_card(), capital_name)

            # Card(0).describe_card() == "2c"
            self.assertEqual(c_number.describe_card(), name)

            # Card(Card(0)).describe_card() == "2c"
            self.assertEqual(c_construct.describe_card(), name)

            # str(Card("2c")) == "2c"
            self.assertEqual(str(c_name), name)
            # repr(Card("2c")) == 'Card("2c")'
            self.assertEqual(repr(c_name), f'Card("{name}")')
