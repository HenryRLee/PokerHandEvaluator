import unittest
from itertools import combinations

from src.hashtable import *


class TestFlushTable(unittest.TestCase):
  TABLE = [0] * len(FLUSH)
  VISIT = [0] * len(FLUSH)
  UPDATED = False
  CUR_RANK = 1

  CACHE = []
  BINARIES = []

  def gen_binary(self, highest, k, n):
    if k == 0:
      self.BINARIES.append(self.CACHE[:])
    else:
      for i in range(highest, -1, -1):
        self.CACHE.append(i)
        self.gen_binary(i - 1, k - 1, n)
        self.CACHE.remove(i)

  def mark_straight(self):
    for highest in range(12, 3, -1):  # From Ace to 6
      # k=5 case for base
      base = [highest - i for i in range(5)]
      base_idx = 0
      for pos in base:
        base_idx += (1 << pos)
      self.TABLE[base_idx] = self.CUR_RANK
      self.VISIT[base_idx] = 1
      self.mark_six_to_nine(base, base_idx)

      # setting up for the next loop
      self.CUR_RANK += 1

    # Five High Straight Flush
    base = [12, 3, 2, 1, 0]
    base_idx = 0
    for pos in base:
      base_idx += (1 << pos)
    self.TABLE[base_idx] = self.CUR_RANK
    self.VISIT[base_idx] = 1
    self.mark_six_to_nine(base, base_idx)
    self.CUR_RANK += 1

  def mark_non_straight(self):
    self.gen_binary(12, 5, 5)
    for base in self.BINARIES:
      base_idx = 0
      for pos in base:
        base_idx += (1 << pos)

      if self.VISIT[base_idx] > 0:
        continue

      self.TABLE[base_idx] = self.CUR_RANK
      self.VISIT[base_idx] = 1
      self.mark_six_to_nine(base, base_idx)

      # setting up for the next loop
      self.CUR_RANK += 1

  def mark_six_to_nine(self, base, base_idx):
    # k=6-9 cases
    pos_candidates = [i for i in range(13) if i not in base]
    for r in [1, 2, 3, 4]:  # Need to select additional cards
      for cb in combinations(pos_candidates, r):
        idx = base_idx
        for pos in cb:
          idx += (1 << pos)

        if self.VISIT[idx] > 0:
          continue

        self.TABLE[idx] = self.CUR_RANK
        self.VISIT[idx] = 1

  def mark_four_of_a_kind(self):
    # Four of a kind
    # The rank of the four cards: 13C1
    # The rank of the other card: 12C1
    self.CUR_RANK += 13 * 12

  def mark_full_house(self):
    # Full house
    # The rank of the cards of three of a kind: 13C1
    # The rank of the cards of a pair: 12C1
    self.CUR_RANK += 13 * 12

  def setUp(self):
    if not self.UPDATED:
      self.mark_straight()
      self.mark_four_of_a_kind()
      self.mark_full_house()
      self.mark_non_straight()
    self.UPDATED = True

  def test_flush_table(self):
    self.assertListEqual(self.TABLE, FLUSH)


if __name__ == "__main__":
  unittest.main()
