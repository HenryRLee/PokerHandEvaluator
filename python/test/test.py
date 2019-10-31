from ctypes import *
import os.path as osp
import unittest
from src.evaluator5 import evaluate_5cards
from src.evaluator6 import evaluate_6cards

path_dylib = osp.join(osp.dirname(__file__), '..', '..', 'cpp', 'build', 'libpheval.dylib')
# TODO: Find a proper way to include
ph_eval = cdll.LoadLibrary(path_dylib)


class TestFiveCardHands(unittest.TestCase):
  TOTAL = 2598960

  def test_five_card_hands(self):
    count = 0
    progress = 0

    print("Start testing five-card hands")

    for a in range(48):
      for b in range(a + 1, 49):
        for c in range(b + 1, 50):
          for d in range(c + 1, 51):
            for e in range(d + 1, 52):
              cpp_eval = ph_eval.evaluate_5cards(a, b, c, d, e)
              py_eval = evaluate_5cards(a, b, c, d, e)

              self.assertEqual(cpp_eval, py_eval)

              count += 1

              percentage = count * 100 / self.TOTAL
              if percentage > progress:
                progress = percentage
                if progress % 10 == 0:
                  print("Test progress: {}%".format(progress))

    print("Complete testing five-card handss.")
    print("Tested {} hands in total.".format(count))


class TestSixCardHands(unittest.TestCase):
  TOTAL = 20358520

  def test_six_card_hands(self):
    count = 0
    progress = 0

    print("Start testing six-card hands")

    for a in range(47):
      for b in range(a + 1, 48):
        for c in range(b + 1, 49):
          for d in range(c + 1, 50):
            for e in range(d + 1, 51):
              for f in range(e + 1, 52):
                cpp_eval = ph_eval.evaluate_6cards(a, b, c, d, e, f)
                py_eval = evaluate_6cards(a, b, c, d, e, f)

                self.assertEqual(cpp_eval, py_eval)

                count += 1

                percentage = count * 100 / self.TOTAL
                if percentage > progress:
                  progress = percentage
                  if progress % 10 == 0:
                    print("Test progress: {}%".format(progress))

    print("Complete testing six-card handss.")
    print("Tested {} hands in total.".format(count))


if __name__ == "__main__":
  unittest.main()
