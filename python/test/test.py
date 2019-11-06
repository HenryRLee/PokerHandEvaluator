from ctypes import *
import os.path as osp
import unittest
from src.evaluator5 import evaluate_5cards
from src.evaluator6 import evaluate_6cards
from src.evaluator7 import evaluate_7cards
from src.evaluator8 import evaluate_8cards

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


class TestSevenCardHands(unittest.TestCase):
  TOTAL = 133784560

  def test_seven_card_hands(self):
    count = 0
    progress = 0

    print("Start testing seven-card hands")

    for a in range(46):
      for b in range(a + 1, 47):
        for c in range(b + 1, 48):
          for d in range(c + 1, 49):
            for e in range(d + 1, 50):
              for f in range(e + 1, 51):
                for g in range(f + 1, 52):
                  cpp_eval = ph_eval.evaluate_7cards(a, b, c, d, e, f, g)
                  py_eval = evaluate_7cards(a, b, c, d, e, f, g)

                  self.assertEqual(cpp_eval, py_eval)

                  count += 1

                  percentage = count * 100 / self.TOTAL
                  if percentage > progress:
                    progress = percentage
                    if progress % 10 == 0:
                      print("Test progress: {}%".format(progress))

    print("Complete testing seven-card handss.")
    print("Tested {} hands in total.".format(count))


class TestEightCardHands(unittest.TestCase):
  TOTAL = 752538150

  def test_eight_card_hands(self):
    count = 0
    progress = 0

    print("Start testing eight-card hands")

    for a in range(45):
      for b in range(a + 1, 46):
        for c in range(b + 1, 47):
          for d in range(c + 1, 48):
            for e in range(d + 1, 49):
              for f in range(e + 1, 50):
                for g in range(f + 1, 51):
                  for h in range(g + 1, 52):
                    cpp_eval = ph_eval.evaluate_8cards(a, b, c, d, e, f, g, h)
                    py_eval = evaluate_8cards(a, b, c, d, e, f, g, h)

                    self.assertEqual(cpp_eval, py_eval)

                    count += 1

                    percentage = count * 100 / self.TOTAL
                    if percentage > progress:
                      progress = percentage
                      if progress % 10 == 0:
                        print("Test progress: {}%".format(progress))

    print("Complete testing eight-card handss.")
    print("Tested {} hands in total.".format(count))


if __name__ == "__main__":
  unittest.main()
