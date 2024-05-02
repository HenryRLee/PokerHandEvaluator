from __future__ import annotations

import unittest
from itertools import combinations
from itertools import permutations
from typing import ClassVar
from typing import Iterable

from phevaluator.hash import hash_quinary
from phevaluator.tables import NO_FLUSH_5


class TestNoFlush5Table(unittest.TestCase):
    TABLE: ClassVar[list[int]] = [0] * len(NO_FLUSH_5)
    VISIT: ClassVar[list[int]] = [0] * len(NO_FLUSH_5)
    CUR_RANK: ClassVar[int] = 1
    NUM_CARDS: ClassVar[int] = 5

    @classmethod
    def setUpClass(cls) -> None:
        cls.mark_straight_flush()
        cls.mark_four_of_a_kind()
        cls.mark_full_house()
        cls.mark_flush()
        cls.mark_straight()
        cls.mark_three_of_a_kind()
        cls.mark_two_pair()
        cls.mark_one_pair()
        cls.mark_high_card()

    @staticmethod
    def quinaries(n: int) -> Iterable[tuple[int, ...]]:
        return permutations(range(13)[::-1], n)

    @staticmethod
    def quinaries_without_duplication() -> Iterable[tuple[int, ...]]:
        return combinations(range(13)[::-1], 5)

    @classmethod
    def mark_four_of_a_kind(cls) -> None:
        # Order 13C2 lexicographically
        for base in cls.quinaries(2):
            hand = [0] * 13
            hand[base[0]] = 4
            hand[base[1]] = 1
            hash_ = hash_quinary(hand, cls.NUM_CARDS)
            cls.TABLE[hash_] = cls.CUR_RANK
            cls.VISIT[hash_] = 1
            cls.CUR_RANK += 1

    @classmethod
    def mark_full_house(cls) -> None:
        for base in cls.quinaries(2):
            hand = [0] * 13
            hand[base[0]] = 3
            hand[base[1]] = 2
            hash_ = hash_quinary(hand, cls.NUM_CARDS)
            cls.TABLE[hash_] = cls.CUR_RANK
            cls.VISIT[hash_] = 1
            cls.CUR_RANK += 1

    @classmethod
    def mark_straight(cls) -> None:
        for lowest in range(9)[::-1]:  # From 10 to 2
            hand = [0] * 13
            for i in range(lowest, lowest + 5):
                hand[i] = 1
            hash_ = hash_quinary(hand, cls.NUM_CARDS)
            cls.TABLE[hash_] = cls.CUR_RANK
            cls.VISIT[hash_] = 1
            cls.CUR_RANK += 1

        # Five High Straight Flush
        base = [12, 3, 2, 1, 0]
        hand = [0] * 13
        for pos in base:
            hand[pos] = 1

        hash_ = hash_quinary(hand, cls.NUM_CARDS)
        cls.TABLE[hash_] = cls.CUR_RANK
        cls.VISIT[hash_] = 1
        cls.CUR_RANK += 1

    @classmethod
    def mark_three_of_a_kind(cls) -> None:
        for base in cls.quinaries(3):
            hand = [0] * 13
            hand[base[0]] = 3
            hand[base[1]] = 1
            hand[base[2]] = 1
            hash_ = hash_quinary(hand, cls.NUM_CARDS)
            if cls.VISIT[hash_] == 0:
                cls.TABLE[hash_] = cls.CUR_RANK
                cls.VISIT[hash_] = 1
                cls.CUR_RANK += 1

    @classmethod
    def mark_two_pair(cls) -> None:
        for base in cls.quinaries(3):
            hand = [0] * 13
            hand[base[0]] = 2
            hand[base[1]] = 2
            hand[base[2]] = 1
            hash_ = hash_quinary(hand, cls.NUM_CARDS)
            if cls.VISIT[hash_] == 0:
                cls.TABLE[hash_] = cls.CUR_RANK
                cls.VISIT[hash_] = 1
                cls.CUR_RANK += 1

    @classmethod
    def mark_one_pair(cls) -> None:
        for base in cls.quinaries(4):
            hand = [0] * 13
            hand[base[0]] = 2
            hand[base[1]] = 1
            hand[base[2]] = 1
            hand[base[3]] = 1
            hash_ = hash_quinary(hand, cls.NUM_CARDS)
            if cls.VISIT[hash_] == 0:
                cls.TABLE[hash_] = cls.CUR_RANK
                cls.VISIT[hash_] = 1
                cls.CUR_RANK += 1

    @classmethod
    def mark_high_card(cls) -> None:
        for base in cls.quinaries_without_duplication():
            hand = [0] * 13
            hand[base[0]] = 1
            hand[base[1]] = 1
            hand[base[2]] = 1
            hand[base[3]] = 1
            hand[base[4]] = 1
            hash_ = hash_quinary(hand, cls.NUM_CARDS)
            if cls.VISIT[hash_] == 0:
                cls.TABLE[hash_] = cls.CUR_RANK
                cls.VISIT[hash_] = 1
                cls.CUR_RANK += 1

    @classmethod
    def mark_straight_flush(cls) -> None:
        # A-5 High Straight Flush: 10
        cls.CUR_RANK += 10

    @classmethod
    def mark_flush(cls) -> None:
        # Selecting 5 cards in 13: 13C5
        # Need to exclude straight: -10
        cls.CUR_RANK += int(13 * 12 * 11 * 10 * 9 / (5 * 4 * 3 * 2)) - 10

    def test_noflush5_table(self) -> None:
        self.assertListEqual(self.TABLE, NO_FLUSH_5)


if __name__ == "__main__":
    unittest.main()
