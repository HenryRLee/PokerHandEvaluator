import unittest

from phevaluator.tables import NO_FLUSH_7

from .utils import BaseTestNoFlushTable


class TestNoFlush7Table(BaseTestNoFlushTable):
    TOCOMPARE = NO_FLUSH_7
    TABLE = [0] * len(TOCOMPARE)
    VISIT = [0] * len(TOCOMPARE)
    NUM_CARDS = 7

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_noflush7_table(self):
        self.assertListEqual(self.TABLE, self.TOCOMPARE)


if __name__ == "__main__":
    unittest.main()
