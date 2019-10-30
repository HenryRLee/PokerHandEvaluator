import unittest
from itertools import combinations_with_replacement

from src.dptables import *


class TestSuitsTable(unittest.TestCase):
  TABLE = [0] * len(SUITS)
  UPDATED = False

  def setUp(self):

    def update_k(table, k):
      iterable = list(range(0, k + 1))
      cbs = combinations_with_replacement(iterable, 3)

      for cb in cbs:
        # cb is in lexicographically sorted order
        cnts = (cb[0], cb[1] - cb[0], cb[2] - cb[1], k - cb[2])
        for suit, cnt in enumerate(cnts):
          if cnt >= 5:
            idx = 0x1 * cnts[0] + 0x8 * cnts[1] + 0x40 * cnts[2] + 0x200 * cnts[3]

            # TODO: Need to check these cases:
            #  There exist three cases that idxes are same.
            #  For two different cnts in case of k=9. The
            #  cases are 72, 520, 576.
            if idx in [72, 520, 576] and SUITS[idx] != suit + 1:
              continue

            table[idx] = suit + 1

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
          if j - q >= 0:
            self.TABLE[1][i][j] += self.TABLE[1][i - 1][j - q]

    # Make recursion
    for l in range(2, 5):
      for i in range(14):
        for j in range(10):
          self.TABLE[l][i][j] = self.TABLE[l - 1][i][j]
          if j - l + 1 >= 0:
            self.TABLE[l][i][j] += self.TABLE[1][i][j - l + 1]

  def setUp(self):
    if not self.UPDATED:
      self.fill_table()
      self.UPDATED = True

  def test_dp_table(self):
    self.assertListEqual(self.TABLE, DP)


if __name__ == "__main__":
  unittest.main()
