import warnings
from typing import Iterable, Union

from .card import Card
from .evaluator_omaha import evaluate_omaha_cards
from .hash import hash_quinary
from .tables import (
    BINARIES_BY_ID,
    FLUSH,
    NO_FLUSH_5,
    NO_FLUSH_6,
    NO_FLUSH_7,
    SUITBIT_BY_ID,
    SUITS,
)

MIN_CARDS = 5
MAX_CARDS = 7

NO_FLUSHES = {5: NO_FLUSH_5, 6: NO_FLUSH_6, 7: NO_FLUSH_7}

warnings.filterwarnings("default", category=DeprecationWarning)


def evaluate_cards(*cards: Iterable[Union[int, str, Card]]) -> int:
    cards = list(map(Card, cards))
    hand_size = len(cards)

    if hand_size == 9:
        warnings.warn( "Use evaluate_omaha_cards instead.", DeprecationWarning)
        return evaluate_omaha_cards(*cards)

    elif (not (MIN_CARDS <= hand_size <= MAX_CARDS)) or (hand_size not in NO_FLUSHES):
        raise ValueError(
            f"The number of cards must be between {MIN_CARDS} and {MAX_CARDS}."
            f"passed size: {hand_size}"
        )

    NO_FLUSH = NO_FLUSHES[hand_size]

    suit_hash = 0
    for card in cards:
        suit_hash += SUITBIT_BY_ID[card]

    flush_suit = SUITS[suit_hash] - 1

    if flush_suit != -1:
        hand_binary = 0

        for card in cards:
            if card % 4 == flush_suit:
                hand_binary |= BINARIES_BY_ID[card]

        return FLUSH[hand_binary]

    hand_quinary = [0] * 13
    for card in cards:
        hand_quinary[card // 4] += 1

    return NO_FLUSH[hash_quinary(hand_quinary, hand_size)]


def evaluate_5cards(*cards: Iterable[int]) -> int:
    warnings.warn(
        "evaluate_5cards will be deprecated. Use evaluate_cards instead.",
        DeprecationWarning,
    )
    return evaluate_cards(*cards)


def evaluate_6cards(*cards: Iterable[int]) -> int:
    warnings.warn(
        "evaluate_6cards will be deprecated. Use evaluate_cards instead.",
        DeprecationWarning,
    )
    return evaluate_cards(*cards)


def evaluate_7cards(*cards: Iterable[int]) -> int:
    warnings.warn(
        "evaluate_7cards will be deprecated. Use evaluate_cards instead.",
        DeprecationWarning,
    )
    return evaluate_cards(*cards)
