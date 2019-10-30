import unittest
from itertools import combinations, combinations_with_replacement

from src.dptables import *
from src.hashtable import *


class TestSuitsTable(unittest.TestCase):

  TABLE = [0] * len(SUITS)
  UPDATED = False

  def setUp(self):

    def update_k(table, k):
      iterable = list(range(0, k+1))
      cbs = combinations_with_replacement(iterable, 3)
      
      for cb in cbs:
        # cb is in lexicographically sorted order
        cnts = (cb[0], cb[1]-cb[0], cb[2]-cb[1], k-cb[2])
        for suit, cnt in enumerate(cnts):
          if cnt >= 5:
            idx = 0x1 * cnts[0] + 0x8 * cnts[1] + 0x40 * cnts[2] + 0x200 * cnts[3]

            # TODO: Need to check these cases:
            #  There exist three cases that idxes are same.
            #  For two different cnts in case of k=9. The
            #  cases are 72, 520, 576.
            if idx in [72, 520, 576] and SUITS[idx] != suit+1:
              continue

            table[idx] = suit+1

    if not self.UPDATED:
      for k in [5, 6, 7, 8, 9]:
        update_k(self.TABLE, k)
      self.UPDATED = True

  def test_suits_table(self):
    self.assertListEqual(self.TABLE, SUITS)


class TestChooseTable(unittest.TestCase):

  TABLE = [[0] * len(CHOOSE[idx]) for idx in range(len(CHOOSE))]
  VISIT = [[0] * len(CHOOSE[idx]) for idx in range(len(CHOOSE))]
  UPDATED = False

  def nCr(self, n, r):
    if n < r:
      return 0
    elif r == 0:
      self.TABLE[n][r] = 1
      return 1
    else:
      if self.VISIT[n][r] == 0:
        self.TABLE[n][r] = self.nCr(n-1, r) + self.nCr(n-1, r-1)
        self.VISIT[n][r] = 1
      return self.TABLE[n][r]

  def setUp(self):
    if not self.UPDATED:
      for row in range(len(CHOOSE)):
        for col in range(len(CHOOSE[row])):
          self.nCr(row, col)
      self.UPDATED = True

  def test_choose_table(self):
    self.assertListEqual(self.TABLE, CHOOSE)


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
        self.gen_binary(i-1, k-1, n)
        self.CACHE.remove(i)

  def mark_straight(self):
    for highest in range(12, 3, -1):  # From Ace to 6
      # k=5 case for base
      base = [highest-i for i in range(5)]
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


class TestDpTable(unittest.TestCase):

  TABLE = [[[0] * len(DP[i][j]) for j in range(len(DP[i]))] for i in range(len(DP))]
  UPDATED = False

  def fill_table(self):
    # Recursion formula:
    # dp[l][i][j] = dp[l-1][i][j] + dp[1][i][j-l+1]
    #
    # We need base cases of dp[1][i][j] to calculate.
    #
    # Base cases:
    # dp[1][i][j] is something like combination with 
    # replacement(iHj), but each bag cannot be bigger than 4.
    # (1) dp[1][1][j] = 1 for 0 <= j <= 4, 0 for j > 4  
    #     dp[1][0][j] = 0 for i = 0 (invalid)
    # (2) dp[1][i>1][j] = SUM { dp[1][i-1][j-q] }
    #     for q from 0 to 4 where j-q >= 0.
    #     This is like setting the most left number to q.
    # We need (2) because of the restriction.

    # Make base cases
    for j in range(0, 5):
      self.TABLE[1][1][j] = 1
    for i in range(2, 14):
      for j in range(10):
        for q in range(5):
          if j-q >= 0:
            self.TABLE[1][i][j] += self.TABLE[1][i-1][j-q]

    # Make recursion
    for l in range(2, 5):
      for i in range(14):
        for j in range(10):
          self.TABLE[l][i][j] = self.TABLE[l-1][i][j]
          if j-l+1 >= 0:
            self.TABLE[l][i][j] += self.TABLE[1][i][j-l+1]

  def setUp(self):
    if not self.UPDATED:
      self.fill_table()
      self.UPDATED = True
  
  def test_dp_table(self):
    self.assertListEqual(self.TABLE, DP)
           

def hash_quinary(hand, lenbit, k):
  hash_ = 0
  hand = list(reversed(str(hand)))  # Reversed lexicographical order
  for i in range(lenbit):
    cur_cnt = int(hand[i])
    hash_ += DP[cur_cnt][lenbit-i-1][k]
    k -= cur_cnt
    if k <= 0:
      break

  return hash_


class TestNoFlush5Table(unittest.TestCase):
  
  TABLE = [0] * len(NOFLUSH5)
  VISIT = [0] * len(NOFLUSH5)
  UPDATED = False
  CUR_RANK = 1
  NUM_CARDS = 5

  CACHE = []
  USED = [0] * 13
  BINARIES = []
  def gen_binary(self, k, n, highest=None):
    if k == 0:
      self.BINARIES.append(self.CACHE[:])
    else:
      start = 12 if highest is None else highest
      for i in range(start, -1, -1):
        if self.USED[i] > 0:
          continue
        self.CACHE.append(i)
        self.USED[i] = 1
        self.gen_binary(k-1, n, None if highest is None else i-1)
        self.CACHE.remove(i)
        self.USED[i] = 0

  def mark_four_of_a_kind(self):
    # Order 13C2 lexicograhically
    self.gen_binary(2, 2)
    for base in self.BINARIES:
      idx = 0
      idx += (10 ** base[0]) * 4
      idx += 10 ** base[1]
      hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
      self.TABLE[hash_] = self.CUR_RANK
      self.VISIT[hash_] = 1
      self.CUR_RANK += 1

    self.BINARIES = []

  def mark_full_house(self):
    self.gen_binary(2, 2)
    for base in self.BINARIES:
      idx = 0
      idx += (10 ** base[0]) * 3
      idx += (10 ** base[1]) * 2
      hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
      self.TABLE[hash_] = self.CUR_RANK
      self.VISIT[hash_] = 1
      self.CUR_RANK += 1

    self.BINARIES = []

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
    self.gen_binary(3, 3)
    for base in self.BINARIES:
      idx = 0
      idx += (10 ** base[0]) * 3
      idx += (10 ** base[1])
      idx += (10 ** base[2])
      hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
      if self.VISIT[hash_] == 0:
        self.TABLE[hash_] = self.CUR_RANK
        self.VISIT[hash_] = 1
        self.CUR_RANK += 1

    self.BINARIES = []

  def mark_two_pair(self):
    self.gen_binary(3, 3)
    for base in self.BINARIES:
      idx = 0
      idx += (10 ** base[0]) * 2
      idx += (10 ** base[1]) * 2
      idx += (10 ** base[2])
      hash_ = hash_quinary(idx, 13, self.NUM_CARDS)
      if self.VISIT[hash_] == 0:
        self.TABLE[hash_] = self.CUR_RANK
        self.VISIT[hash_] = 1
        self.CUR_RANK += 1

    self.BINARIES = []

  def mark_one_pair(self):
    self.gen_binary(4, 4)
    for base in self.BINARIES:
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

    self.BINARIES = []

  def mark_high_card(self):
    self.gen_binary(5, 5)
    for base in self.BINARIES:
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

    self.BINARIES = []

  def mark_straight_flush(self):
    # A-5 High Straight Flush: 10
    self.CUR_RANK += 10

  def mark_flush(self):
    # Selecting 5 cards in 13: 13C5
    # Need to exclude straight: -10
    self.CUR_RANK += 13*12*11*10*9 / (5*4*3*2) - 10

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
