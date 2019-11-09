import unittest

from test_tables.utils import BaseTestNoFLushTable
from src.hashtable import *


class TestNoFlush8Table(BaseTestNoFLushTable):
  TOCOMPARE = NOFLUSH8
  TABLE = [0] * len(TOCOMPARE)
  VISIT = [0] * len(TOCOMPARE)
  NUM_CARDS = 8

  def test_noflush8_table(self):
    self.assertListEqual(self.TABLE, self.TOCOMPARE)


if __name__ == "__main__":
  unittest.main()
