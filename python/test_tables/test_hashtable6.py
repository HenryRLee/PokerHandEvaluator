import unittest

from test_tables.utils import BaseTestNoFLushTable
from src.hashtable import *


class TestNoFlush6Table(BaseTestNoFLushTable):
  TOCOMPARE = NOFLUSH6
  TABLE = [0] * len(TOCOMPARE)
  VISIT = [0] * len(TOCOMPARE)
  NUM_CARDS = 6

  def test_noflush6_table(self):
    self.assertListEqual(self.TABLE, self.TOCOMPARE)


if __name__ == "__main__":
  unittest.main()
