import time
from itertools import combinations

from phevaluator import _evaluate_cards


def evaluate_all_five_card_hands():
    for cards in combinations(range(52), 5):
        _evaluate_cards(*cards)


def evaluate_all_six_card_hands():
    for cards in combinations(range(52), 6):
        _evaluate_cards(*cards)


def evaluate_all_seven_card_hands():
    for cards in combinations(range(52), 7):
        _evaluate_cards(*cards)


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
