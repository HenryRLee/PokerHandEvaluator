import unittest
from itertools import combinations

from phevaluator.tables import FLUSH


class TestFlushTable(unittest.TestCase):
    TABLE = [0] * len(FLUSH)
    VISIT = [0] * len(FLUSH)
    CUR_RANK = 1

    CACHE: list[int] = []
    BINARIES: list[int] = []

    @classmethod
    def setUpClass(cls):
        cls.mark_straight()
        cls.mark_four_of_a_kind()
        cls.mark_full_house()
        cls.mark_non_straight()

    @classmethod
    def gen_binary(cls, highest, k, n):
        if k == 0:
            cls.BINARIES.append(cls.CACHE[:])
        else:
            for i in range(highest, -1, -1):
                cls.CACHE.append(i)
                cls.gen_binary(i - 1, k - 1, n)
                cls.CACHE.remove(i)

    @classmethod
    def mark_straight(cls):
        for highest in range(12, 3, -1):  # From Ace to 6
            # k=5 case for base
            base = [highest - i for i in range(5)]
            base_idx = 0
            for pos in base:
                base_idx += 1 << pos
            cls.TABLE[base_idx] = cls.CUR_RANK
            cls.VISIT[base_idx] = 1
            cls.mark_six_to_nine(base, base_idx)

            # setting up for the next loop
            cls.CUR_RANK += 1

        # Five High Straight Flush
        base = [12, 3, 2, 1, 0]
        base_idx = 0
        for pos in base:
            base_idx += 1 << pos
        cls.TABLE[base_idx] = cls.CUR_RANK
        cls.VISIT[base_idx] = 1
        cls.mark_six_to_nine(base, base_idx)
        cls.CUR_RANK += 1

    @classmethod
    def mark_non_straight(cls):
        cls.gen_binary(12, 5, 5)
        for base in cls.BINARIES:
            base_idx = 0
            for pos in base:
                base_idx += 1 << pos

            if cls.VISIT[base_idx] > 0:
                continue

            cls.TABLE[base_idx] = cls.CUR_RANK
            cls.VISIT[base_idx] = 1
            cls.mark_six_to_nine(base, base_idx)

            # setting up for the next loop
            cls.CUR_RANK += 1

    @classmethod
    def mark_six_to_nine(cls, base, base_idx):
        # k=6-9 cases
        pos_candidates = [i for i in range(13) if i not in base]
        for r in [1, 2, 3, 4]:  # Need to select additional cards
            for comb in combinations(pos_candidates, r):
                idx = base_idx
                for pos in comb:
                    idx += 1 << pos

                if cls.VISIT[idx] > 0:
                    continue

                cls.TABLE[idx] = cls.CUR_RANK
                cls.VISIT[idx] = 1

    @classmethod
    def mark_four_of_a_kind(cls):
        # Four of a kind
        # The rank of the four cards: 13C1
        # The rank of the other card: 12C1
        cls.CUR_RANK += 13 * 12

    @classmethod
    def mark_full_house(cls):
        # Full house
        # The rank of the cards of three of a kind: 13C1
        # The rank of the cards of a pair: 12C1
        cls.CUR_RANK += 13 * 12

    def test_flush_table(self):
        self.assertListEqual(self.TABLE, FLUSH)


if __name__ == "__main__":
    unittest.main()
