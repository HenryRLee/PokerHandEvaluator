import unittest

from .utils import BaseTestNoFlushTable
from phevaluator.hashtable6 import NO_FLUSH_6


class TestNoFlush6Table(BaseTestNoFlushTable):
    TOCOMPARE = NO_FLUSH_6
    TABLE = [0] * len(TOCOMPARE)
    VISIT = [0] * len(TOCOMPARE)
    NUM_CARDS = 6

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_noflush6_table(self):
        self.assertListEqual(self.TABLE, self.TOCOMPARE)


if __name__ == "__main__":
    unittest.main()
