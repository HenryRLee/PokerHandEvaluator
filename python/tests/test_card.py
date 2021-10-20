import unittest

from phevaluator import Card


class TestCard(unittest.TestCase):
    # lowercase name, capitalcase name, value
    testcases = [
        ["2c", "2C", 0],
        ["2d", "2D", 1],
        ["2h", "2H", 2],
        ["2s", "2S", 3],
        ["Tc", "TC", 32],
        ["Ac", "AC", 48],
    ]

    def test_card_equality(self):
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

    def test_card_immutability(self):
        # Once a Card is assigned or constructed from another Card,
        # it's not affected by any changes to source variable
        c_source = Card(1)
        c_assign = c_source
        c_construct = Card(c_source)

        c_source = Card(2)

        self.assertNotEqual(c_source, Card(1))
        self.assertEqual(c_assign, Card(1))
        self.assertEqual(c_construct, Card(1))

    def test_card_describe(self):
        for name, capital_name, number in self.testcases:
            rank, suit = name
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
