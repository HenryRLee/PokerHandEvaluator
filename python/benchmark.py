import time

from phevaluator import _evaluate_cards


def evaluate_all_five_card_hands():
    for a in range(48):
        for b in range(a + 1, 49):
            for c in range(b + 1, 50):
                for d in range(c + 1, 51):
                    for e in range(d + 1, 52):
                        _evaluate_cards(a, b, c, d, e)


def evaluate_all_six_card_hands():
    for a in range(47):
        for b in range(a + 1, 48):
            for c in range(b + 1, 49):
                for d in range(c + 1, 50):
                    for e in range(d + 1, 51):
                        for f in range(e + 1, 52):
                            _evaluate_cards(a, b, c, d, e, f)


def evaluate_all_seven_card_hands():
    for a in range(46):
        for b in range(a + 1, 47):
            for c in range(b + 1, 48):
                for d in range(c + 1, 49):
                    for e in range(d + 1, 50):
                        for f in range(e + 1, 51):
                            for g in range(f + 1, 52):
                                _evaluate_cards(a, b, c, d, e, f, g)


def benchmark():
    print("--------------------------------------------------------------------")
    print("Benchmark                              Time")
    t = time.process_time()
    evaluate_all_five_card_hands()
    print("evaluate_all_five_card_hands           ", time.process_time() - t)
    t = time.process_time()
    evaluate_all_six_card_hands()
    print("evaluate_all_six_card_hands           ", time.process_time() - t)
    t = time.process_time()
    evaluate_all_seven_card_hands()
    print("evaluate_all_seven_card_hands           ", time.process_time() - t)


if __name__ == "__main__":
    benchmark()
