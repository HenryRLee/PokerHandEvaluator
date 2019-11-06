import unittest

from src.hash import hash_quinary
from src.hashtable5 import NOFLUSH5


class BaseTestNoFLushTable(unittest.TestCase):
  TABLE = NotImplementedError
  VISIT = NotImplementedError
  UPDATED = False
  NUM_CARDS = NotImplementedError

  CACHE = []
  USED = [0] * 13
  QUINARIES = []
  def gen_quinary(self, ks, cur, additional):
    if cur == len(ks):
      self.get_additional(additional)
      self.QUINARIES.append((self.CACHE[:], self.QUINARIES_ADDITIONAL[:]))
      self.QUINARIES_ADDITIONAL = []
    else:
      for i in range(12, -1, -1):
        if self.USED[i] > 0:
          continue
        self.CACHE.append(i)
        self.USED[i] = ks[cur]
        self.gen_quinary(ks, cur+1, additional)
        self.CACHE.pop(-1)
        self.USED[i] = 0

  CACHE_ADDITIONAL = []
  USED_ADDITIONAL = [0] * 13
  QUINARIES_ADDITIONAL = []
  def get_additional(self, n):
    if n == 0:
      self.QUINARIES_ADDITIONAL.append(self.CACHE_ADDITIONAL[:])
    else:
      for i in range(12, -1, -1):
        if self.USED[i] + self.USED_ADDITIONAL[i] >= 4:
          continue
        self.CACHE_ADDITIONAL.append(i)
        self.USED_ADDITIONAL[i] += 1
        self.get_additional(n-1)
        self.CACHE_ADDITIONAL.pop(-1)
        self.USED_ADDITIONAL[i] -= 1

  def mark_template(self, ks):
    self.gen_quinary(ks, 0, self.NUM_CARDS - 5)
    for base, additionals in self.QUINARIES:
      base_idx = 0
      for i in range(len(ks)):
        base_idx += (10 ** base[i]) * ks[i]
      base_rank = NOFLUSH5[hash_quinary(base_idx, 13, 5)]
      for additional in additionals:
        idx = base_idx
        for i in additional:
          idx += 10 ** i
        hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
        if self.VISIT[hash_] > 0:
          continue
        self.TABLE[hash_] = base_rank
        self.VISIT[hash_] = 1

    self.QUINARIES = []

  def mark_four_of_a_kind(self):
    self.mark_template((4, 1))

  def mark_full_house(self):
    self.mark_template((3, 2))

  def mark_three_of_a_kind(self):
    self.mark_template((3, 1, 1))

  def mark_two_pair(self):
    self.mark_template((2, 2, 1))

  def mark_one_pair(self):
    self.mark_template((2, 1, 1, 1))

  def mark_high_card(self):
    self.mark_template((1, 1, 1, 1, 1))

  def mark_straight(self):
    cases = [[highest - i for i in range(5)] for highest in range(12, 3, -1)]
    cases.append([12, 3, 2, 1, 0])
    for base in cases:
      base_idx = 0
      for pos in base:
        base_idx += (10 ** pos)
        self.USED[pos] = 1
      base_rank = NOFLUSH5[hash_quinary(base_idx, 13, 5)]
      self.get_additional(self.NUM_CARDS - 5)
      additionals = self.QUINARIES_ADDITIONAL[:]
      self.QUINARIES_ADDITIONAL = []
      self.USED = [0] * 13
      for additional in additionals:
        idx = base_idx
        for i in additional:
          idx += 10 ** i
        hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
        if self.VISIT[hash_] > 0:
          continue
        self.TABLE[hash_] = base_rank
        self.VISIT[hash_] = 1

  def setUp(self):
    if not self.UPDATED:
      # Straight Flushes are not in this table
      self.mark_four_of_a_kind()
      self.mark_full_house()
      # Flushes are not in this table
      self.mark_straight()
      self.mark_three_of_a_kind()
      self.mark_two_pair()
      self.mark_one_pair()
      self.mark_high_card()
      self.UPDATED = True
