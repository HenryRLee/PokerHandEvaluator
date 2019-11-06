import unittest

from test_tables.utils import BaseTestNoFLushTable
from src.hashtable import *


class TestNoFlush7Table(BaseTestNoFLushTable):
  TOCOMPARE = NOFLUSH7
  TABLE = [0] * len(TOCOMPARE)
  VISIT = [0] * len(TOCOMPARE)
  NUM_CARDS = 7

  def test_noflush7_table(self):
    self.assertListEqual(self.TABLE, self.TOCOMPARE)


if __name__ == "__main__":
  unittest.main()
