from evaluator.evaluator5 import evaluate_5cards
from evaluator.evaluator import evaluate_cards

import time

def evaluate_all_five_card_hands():
  for a in range(48):
    for b in range(a+1, 49):
      for c in range(b+1, 50):
        for d in range(c+1, 51):
          for e in range(d+1, 52):
            evaluate_cards(a, b, c, d, e)


def evaluate_all_six_card_hands():
  for a in range(47):
    for b in range(a+1, 48):
      for c in range(b+1, 49):
        for d in range(c+1, 50):
          for e in range(d+1, 51):
            for f in range(e+1, 52):
              evaluate_cards(a, b, c, d, e, f)


def evaluate_all_seven_card_hands():
  for a in range(46):
    for b in range(a+1, 47):
      for c in range(b+1, 48):
        for d in range(c+1, 49):
          for e in range(d+1, 50):
            for f in range(e+1, 51):
              for g in range(f+1, 52):
                evaluate_cards(a, b, c, d, e, f, g)


def evaluate_all_eight_card_hands():
  for a in range(45):
    for b in range(a+1, 46):
      for c in range(b+1, 47):
        for d in range(c+1, 48):
          for e in range(d+1, 49):
            for f in range(e+1, 50):
              for g in range(f+1, 51):
                for h in range(g+1, 52):
                  evaluate_cards(a, b, c, d, e, f, g, h)


def evaluate_all_nine_card_hands():
  for a in range(44):
    for b in range(a+1, 45):
      for c in range(b+1, 46):
        for d in range(c+1, 47):
          for e in range(d+1, 48):
            for f in range(e+1, 49):
              for g in range(f+1, 50):
                for h in range(g+1, 51):
                  for i in range(h+1, 52):
                    evaluate_cards(a, b, c, d, e, f, g, h, i)

def benchmark():
  print('--------------------------------------------------------------------')
  print('Benchmark                              Time')
  t = time.process_time()
  evaluate_all_five_card_hands()
  print('evaluate_all_five_card_hands           ', time.process_time() - t)
  t = time.process_time()
  evaluate_all_six_card_hands()
  print('evaluate_all_six_card_hands           ', time.process_time() - t)
  t = time.process_time()
  evaluate_all_seven_card_hands()
  print('evaluate_all_seven_card_hands           ', time.process_time() - t)
  t = time.process_time()
  evaluate_all_eight_card_hands()
  print('evaluate_all_eight_card_hands           ', time.process_time() - t)
  t = time.process_time()
  evaluate_all_nine_card_hands()
  print('evaluate_all_nine_card_hands           ', time.process_time() - t)



if __name__ == "__main__":
    benchmark()
