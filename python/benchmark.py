import time
from itertools import combinations

from phevaluator import _evaluate_cards
from phevaluator import _evaluate_omaha_cards
from phevaluator import sample_cards


def evaluate_all_five_card_hands() -> None:
    for cards in combinations(range(52), 5):
        _evaluate_cards(*cards)


def evaluate_all_six_card_hands() -> None:
    for cards in combinations(range(52), 6):
        _evaluate_cards(*cards)


def evaluate_all_seven_card_hands() -> None:
    for cards in combinations(range(52), 7):
        _evaluate_cards(*cards)


def evaluate_random_omaha_card_hands() -> None:
    total = 100_000
    for _ in range(total):
        cards = sample_cards(9)
        _evaluate_omaha_cards(cards[:5], cards[5:])


def benchmark() -> None:
    print("--------------------------------------------------------------------")
    print("Benchmark                              Time")
    t = time.process_time()
    evaluate_random_omaha_card_hands()
    print("evaluate_random_omaha_card_hands           ", time.process_time() - t)
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
