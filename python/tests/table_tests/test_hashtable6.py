import unittest

from phevaluator.tables import NO_FLUSH_6

from .utils import BaseTestNoFlushTable


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
