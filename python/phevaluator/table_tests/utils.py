import unittest

from evaluator.hash import hash_quinary
from evaluator.hashtable5 import NO_FLUSH_5


class BaseTestNoFlushTable(unittest.TestCase):
    TABLE = NotImplementedError
    VISIT = NotImplementedError
    NUM_CARDS = NotImplementedError

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
            base_idx = 0
            for i in range(len(ks)):
                base_idx += (10 ** base[i]) * ks[i]
            hand = list(map(int, reversed("{:013d}".format(base_idx))))
            base_rank = NO_FLUSH_5[hash_quinary(hand, 13, 5)]
            for additional in additionals:
                idx = base_idx
                for i in additional:
                    idx += 10 ** i
                hand = list(map(int, reversed("{:013d}".format(idx))))
                hash_ = hash_quinary(hand, 13, cls.NUM_CARDS)
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
        cls.mark_template((2, 1, 1, 1))

    @classmethod
    def mark_high_card(cls):
        cls.mark_template((1, 1, 1, 1, 1))

    @classmethod
    def mark_straight(cls):
        cases = [[highest - i for i in range(5)] for highest in range(12, 3, -1)]
        cases.append([12, 3, 2, 1, 0])
        for base in cases:
            base_idx = 0
            for pos in base:
                base_idx += 10 ** pos
                cls.USED[pos] = 1
            hand = list(map(int, reversed("{:013d}".format(base_idx))))
            base_rank = NO_FLUSH_5[hash_quinary(hand, 13, 5)]
            cls.get_additional(cls.NUM_CARDS - 5)
            additionals = cls.QUINARIES_ADDITIONAL[:]
            cls.QUINARIES_ADDITIONAL = []
            cls.USED = [0] * 13
            for additional in additionals:
                idx = base_idx
                for i in additional:
                    idx += 10 ** i
                hand = list(map(int, reversed("{:013d}".format(idx))))
                hash_ = hash_quinary(hand, 13, cls.NUM_CARDS)
                if cls.VISIT[hash_] > 0:
                    continue
                cls.TABLE[hash_] = base_rank
                cls.VISIT[hash_] = 1
