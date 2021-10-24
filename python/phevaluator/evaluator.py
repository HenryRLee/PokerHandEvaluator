"""Module evaluating cards."""
from typing import Union

from .card import Card
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


def evaluate_cards(*cards: Union[int, str, Card]) -> int:
    """Evaluate cards for the best five cards.

    This function selects the best combination of the five cards from given cards and
    return its rank.
    The number of cards must be between 5 and 7.

    Args:
        cards(Union[int, str, Card]): List of cards

    Raises:
        ValueError: Unsupported size of the cards

    Returns:
        int: The rank of the given cards with the best five cards. Smaller is stronger.

    Examples:
        >>> rank1 = evaluate_cards("Ac", "Ad", "Ah", "As", "Kc")
        >>> rank2 = evaluate_cards("Ac", "Ad", "Ah", "As", "Kd")
        >>> rank3 = evaluate_cards("Ac", "Ad", "Ah", "As", "Kc", "Qh")
        >>> rank1 == rank2 == rank3 # Those three are evaluated by `A A A A K`
        True
    """
    int_cards = list(map(Card.to_id, cards))
    hand_size = len(cards)

    if not (MIN_CARDS <= hand_size <= MAX_CARDS) or (hand_size not in NO_FLUSHES):
        raise ValueError(
            f"The number of cards must be between {MIN_CARDS} and {MAX_CARDS}."
            f"passed size: {hand_size}"
        )

    return _evaluate_cards(*int_cards)


def _evaluate_cards(*cards: int) -> int:
    hand_size = len(cards)
    no_flush = NO_FLUSHES[hand_size]

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

    return no_flush[hash_quinary(hand_quinary, hand_size)]
