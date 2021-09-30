import unittest

from table_tests.utils import BaseTestNoFlushTable
from evaluator.hashtable7 import NO_FLUSH_7


class TestNoFlush7Table(BaseTestNoFlushTable):
    TOCOMPARE = NO_FLUSH_7
    TABLE = [0] * len(TOCOMPARE)
    VISIT = [0] * len(TOCOMPARE)
    NUM_CARDS = 7

    def test_noflush7_table(self):
        self.assertListEqual(self.TABLE, self.TOCOMPARE)


if __name__ == "__main__":
    unittest.main()
