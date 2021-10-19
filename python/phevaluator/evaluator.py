import warnings
from typing import Iterable, Union

from .card import Card
from .evaluator_omaha import evaluate_omaha_cards
from .evaluator_texas import MAX_CARDS as TEXAS_MAX_CARDS
from .evaluator_texas import MIN_CARDS as TEXAS_MIN_CARDS
from .evaluator_texas import evaluate_texas_cards

warnings.filterwarnings("default", category=DeprecationWarning)

def evaluate_cards(*cards: Iterable[Union[int, str, Card]]) -> int:
    cards = list(map(Card, cards))
    hand_size = len(cards)

    if 5 <= hand_size <= 7:
        return evaluate_texas_cards(*cards)

    elif hand_size == 9:
        return evaluate_omaha_cards(*cards)

    else:
        raise ValueError(
            f"The number of cards must be between {TEXAS_MIN_CARDS} and "
            f"{TEXAS_MAX_CARDS} for Texas Hold'em and 9 for Omaha Hold'em. "
            f"passed size: {hand_size}"
        )


def evaluate_5cards(*cards: Iterable[int]) -> int:
    warnings.warn(
        "evaluate_5cards will be deprecated. Use evaluate_texas_cards instead.",
        DeprecationWarning,
    )
    return evaluate_texas_cards(*cards)


def evaluate_6cards(*cards: Iterable[int]) -> int:
    warnings.warn(
        "evaluate_6cards will be deprecated. Use evaluate_texas_cards instead.",
        DeprecationWarning,
    )
    return evaluate_texas_cards(*cards)


def evaluate_7cards(*cards: Iterable[int]) -> int:
    warnings.warn(
        "evaluate_7cards will be deprecated. Use evaluate_texas_cards instead.",
        DeprecationWarning,
    )
    return evaluate_texas_cards(*cards)
