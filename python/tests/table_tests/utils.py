import unittest
from itertools import combinations, combinations_with_replacement, permutations

from phevaluator.hash import hash_quinary
from phevaluator.tables import NO_FLUSH_5


class BaseTestNoFlushTable(unittest.TestCase):
    TABLE: list[int] = NotImplemented
    VISIT: list[int] = NotImplemented
    NUM_CARDS: int = NotImplemented

    @classmethod
    def setUpClass(cls):
        cls.CACHE = []
        cls.USED = [0] * 13
        cls.QUINARIES = []

        cls.CACHE_ADDITIONAL = []
        cls.USED_ADDITIONAL = [0] * 13
        cls.QUINARIES_ADDITIONAL = []

        # Straight Flushes are not in this table
        cls.mark_four_of_a_kind()
        cls.mark_full_house()
        # Flushes are not in this table
        cls.mark_straight()
        cls.mark_three_of_a_kind()
        cls.mark_two_pair()
        cls.mark_one_pair()
        cls.mark_high_card()

    @staticmethod
    def quinary_permutations(n):
        return permutations(range(13)[::-1], n)

    @staticmethod
    def quinary_combinations(n):
        return combinations(range(13)[::-1], n)

    @staticmethod
    def quinary_combinations_with_replacement(n):
        return combinations_with_replacement(range(13)[::-1], n)

    @classmethod
    def gen_quinary(cls, ks, cur, additional):
        if cur == len(ks):
            cls.get_additional(additional)
            cls.QUINARIES.append((cls.CACHE[:], cls.QUINARIES_ADDITIONAL[:]))
            cls.QUINARIES_ADDITIONAL = []
        else:
            for i in range(12, -1, -1):
                if cls.USED[i] > 0:
                    continue
                cls.CACHE.append(i)
                cls.USED[i] = ks[cur]
                cls.gen_quinary(ks, cur + 1, additional)
                cls.CACHE.pop(-1)
                cls.USED[i] = 0

    @classmethod
    def get_additional(cls, n):
        if n == 0:
            cls.QUINARIES_ADDITIONAL.append(cls.CACHE_ADDITIONAL[:])
        else:
            for i in range(12, -1, -1):
                if cls.USED[i] + cls.USED_ADDITIONAL[i] >= 4:
                    continue
                cls.CACHE_ADDITIONAL.append(i)
                cls.USED_ADDITIONAL[i] += 1
                cls.get_additional(n - 1)
                cls.CACHE_ADDITIONAL.pop(-1)
                cls.USED_ADDITIONAL[i] -= 1

    @classmethod
    def mark_template(cls, ks):
        cls.gen_quinary(ks, 0, cls.NUM_CARDS - 5)
        for base, additionals in cls.QUINARIES:
            hand = [0] * 13
            for i, k in enumerate(ks):
                hand[base[i]] = k
            base_rank = NO_FLUSH_5[hash_quinary(hand, 5)]
            for additional in additionals:
                for i in additional:

                    hand[i] += 1

                hash_ = hash_quinary(hand, cls.NUM_CARDS)

                for i in additional:
                    hand[i] -= 1

                if cls.VISIT[hash_] > 0:
                    continue
                cls.TABLE[hash_] = base_rank
                cls.VISIT[hash_] = 1

        cls.QUINARIES = []

    @classmethod
    def mark_four_of_a_kind(cls):
        cls.mark_template((4, 1))

    @classmethod
    def mark_full_house(cls):
        cls.mark_template((3, 2))

    @classmethod
    def mark_three_of_a_kind(cls):
        cls.mark_template((3, 1, 1))

    @classmethod
    def mark_two_pair(cls):
        cls.mark_template((2, 2, 1))

    @classmethod
    def mark_one_pair(cls):
        for paired_card in range(13)[::-1]:
            for other_cards in cls.quinary_combinations(cls.NUM_CARDS - 2):
                if paired_card in other_cards:
                    continue
                hand = [0] * 13
                hand[paired_card] = 2
                for i in range(3):
                    hand[other_cards[i]] = 1
                base_hash = hash_quinary(hand, 5)
                base_rank = NO_FLUSH_5[base_hash]
                for i in range(3, cls.NUM_CARDS - 2):
                    hand[other_cards[i]] = 1
                hash_ = hash_quinary(hand, cls.NUM_CARDS)
                if cls.VISIT[hash_] == 0:
                    cls.VISIT[hash_] = 1
                    cls.TABLE[hash_] = base_rank

    @classmethod
    def mark_high_card(cls):
        for base in cls.quinary_combinations(cls.NUM_CARDS):
            hand = [0] * 13
            for i in range(5):
                hand[base[i]] = 1
            base_hash = hash_quinary(hand, 5)
            base_rank = NO_FLUSH_5[base_hash]
            for i in range(5, cls.NUM_CARDS):
                hand[base[i]] = 1
            hash_ = hash_quinary(hand, cls.NUM_CARDS)
            if cls.VISIT[hash_] == 0:
                cls.VISIT[hash_] = 1
                cls.TABLE[hash_] = base_rank

    @classmethod
    def mark_straight(cls):
        hands = []
        for lowest in range(9)[::-1]:  # From 10 to 2
            hand = [0] * 13
            for i in range(lowest, lowest + 5):
                hand[i] = 1
            hands.append(hand)
        # Five High Straight Flush
        base = [12, 3, 2, 1, 0]
        hand = [0] * 13
        for i in base:
            hand[i] = 1
        hands.append(hand)

        for hand in hands:
            base_rank = NO_FLUSH_5[hash_quinary(hand, 5)]
            for additional in cls.quinary_combinations_with_replacement(
                cls.NUM_CARDS - 5
            ):
                for i in additional:
                    hand[i] += 1

                hash_ = hash_quinary(hand, cls.NUM_CARDS)
                if cls.VISIT[hash_] == 0:
                    cls.TABLE[hash_] = base_rank
                    cls.VISIT[hash_] = 1

                for i in additional:
                    hand[i] -= 1
