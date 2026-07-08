import time
from itertools import combinations

from phevaluator import evaluate_5cards
from phevaluator import evaluate_6cards
from phevaluator import evaluate_7cards
from phevaluator import evaluate_omaha_cards
from phevaluator import sample_cards


def evaluate_all_five_card_hands() -> None:
    for cards in combinations(range(52), 5):
        evaluate_5cards(*cards)


def evaluate_all_six_card_hands() -> None:
    for cards in combinations(range(52), 6):
        evaluate_6cards(*cards)


def evaluate_all_seven_card_hands() -> None:
    for cards in combinations(range(52), 7):
        evaluate_7cards(*cards)


def evaluate_random_omaha_card_hands() -> None:
    total = 100_000
    for _ in range(total):
        cards = sample_cards(9)
        evaluate_omaha_cards(*cards)


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
