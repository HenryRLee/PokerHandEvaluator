import unittest

from src.hash import hash_quinary
from src.hashtable5 import *


class TestNoFlush5Table(unittest.TestCase):
  TABLE = [0] * len(NOFLUSH5)
  VISIT = [0] * len(NOFLUSH5)
  UPDATED = False
  CUR_RANK = 1
  NUM_CARDS = 5

  CACHE = []
  USED = [0] * 13
  QUINARIES = []

  def gen_quinary(self, k, n):
    if k == 0:
      self.QUINARIES.append(self.CACHE[:])
    else:
      for i in range(12, -1, -1):
        if self.USED[i] > 0:
          continue
        self.CACHE.append(i)
        self.USED[i] = 1
        self.gen_quinary(k - 1, n)
        self.CACHE.remove(i)
        self.USED[i] = 0

  def mark_four_of_a_kind(self):
    # Order 13C2 lexicographically
    self.gen_quinary(2, 2)
    for base in self.QUINARIES:
      idx = 0
      idx += (10 ** base[0]) * 4
      idx += 10 ** base[1]
      hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
      self.TABLE[hash_] = self.CUR_RANK
      self.VISIT[hash_] = 1
      self.CUR_RANK += 1

    self.QUINARIES = []

  def mark_full_house(self):
    self.gen_quinary(2, 2)
    for base in self.QUINARIES:
      idx = 0
      idx += (10 ** base[0]) * 3
      idx += (10 ** base[1]) * 2
      hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
      self.TABLE[hash_] = self.CUR_RANK
      self.VISIT[hash_] = 1
      self.CUR_RANK += 1

    self.QUINARIES = []

  def mark_straight(self):
    for highest in range(12, 3, -1):  # From Ace to 6
      # k=5 case for base
      base = [highest - i for i in range(5)]
      idx = 0
      for pos in base:
        idx += (10 ** pos)
      hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
      self.TABLE[hash_] = self.CUR_RANK
      self.VISIT[hash_] = 1
      self.CUR_RANK += 1

    # Five High Straight Flush
    base = [12, 3, 2, 1, 0]
    idx = 0
    for pos in base:
      idx += (10 ** pos)
    hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
    self.TABLE[hash_] = self.CUR_RANK
    self.VISIT[hash_] = 1
    self.CUR_RANK += 1

  def mark_three_of_a_kind(self):
    self.gen_quinary(3, 3)
    for base in self.QUINARIES:
      idx = 0
      idx += (10 ** base[0]) * 3
      idx += (10 ** base[1])
      idx += (10 ** base[2])
      hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
      if self.VISIT[hash_] == 0:
        self.TABLE[hash_] = self.CUR_RANK
        self.VISIT[hash_] = 1
        self.CUR_RANK += 1

    self.QUINARIES = []

  def mark_two_pair(self):
    self.gen_quinary(3, 3)
    for base in self.QUINARIES:
      idx = 0
      idx += (10 ** base[0]) * 2
      idx += (10 ** base[1]) * 2
      idx += (10 ** base[2])
      hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
      if self.VISIT[hash_] == 0:
        self.TABLE[hash_] = self.CUR_RANK
        self.VISIT[hash_] = 1
        self.CUR_RANK += 1

    self.QUINARIES = []

  def mark_one_pair(self):
    self.gen_quinary(4, 4)
    for base in self.QUINARIES:
      idx = 0
      idx += (10 ** base[0]) * 2
      idx += (10 ** base[1])
      idx += (10 ** base[2])
      idx += (10 ** base[3])
      hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
      if self.VISIT[hash_] == 0:
        self.TABLE[hash_] = self.CUR_RANK
        self.VISIT[hash_] = 1
        self.CUR_RANK += 1

    self.QUINARIES = []

  def mark_high_card(self):
    self.gen_quinary(5, 5)
    for base in self.QUINARIES:
      idx = 0
      idx += (10 ** base[0])
      idx += (10 ** base[1])
      idx += (10 ** base[2])
      idx += (10 ** base[3])
      idx += (10 ** base[4])
      hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
      if self.VISIT[hash_] == 0:
        self.TABLE[hash_] = self.CUR_RANK
        self.VISIT[hash_] = 1
        self.CUR_RANK += 1

    self.QUINARIES = []

  def mark_straight_flush(self):
    # A-5 High Straight Flush: 10
    self.CUR_RANK += 10

  def mark_flush(self):
    # Selecting 5 cards in 13: 13C5
    # Need to exclude straight: -10
    self.CUR_RANK += int(13 * 12 * 11 * 10 * 9 / (5 * 4 * 3 * 2)) - 10

  def setUp(self):
    if not self.UPDATED:
      self.mark_straight_flush()
      self.mark_four_of_a_kind()
      self.mark_full_house()
      self.mark_flush()
      self.mark_straight()
      self.mark_three_of_a_kind()
      self.mark_two_pair()
      self.mark_one_pair()
      self.mark_high_card()
      self.UPDATED = True

  def test_noflush5_table(self):
    self.assertListEqual(self.TABLE, NOFLUSH5)


if __name__ == "__main__":
  unittest.main()
