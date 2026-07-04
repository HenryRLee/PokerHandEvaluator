"""Module evaluating cards in Omaha game."""

from __future__ import annotations

from . import _pheval
from .card import Card

COMMUNITY_CARD_COUNT = 5
HOLE_CARD_COUNT = 4
TOTAL_CARD_COUNT = COMMUNITY_CARD_COUNT + HOLE_CARD_COUNT


def evaluate_omaha_cards(*cards: int | str | Card) -> int:
    """Evaluate cards in Omaha game.

    In the Omaha rule, players can make hand with 3 cards from the 5 community cards and
    2 cards from their own 4 hole cards, then totally 5 cards.
    This function selects the best combination and return its rank.

    Args:
        cards(int | str | Card]): List of cards
            The first five parameters are the community cards.
            The later four parameters are the player hole cards.

    Raises:
        ValueError: Unsupported size of the cards

    Returns:
        int: The rank of the given cards with the best five cards.

    Examples:
        >>> rank1 = evaluate_omaha_cards(
                "3c", "9c", "3h", "9h", "6h", # ["9c", "9h", "6h"]
                "Ac", "Kc", "Qc", "Jc"        # ["Ac", "Kc"]
            )

        >>> rank2 = evaluate_omaha_cards(
                "3c", "9c", "3h", "9h", "6h", # ["9c", "9h", "6h"]
                "Ad", "Kd", "Qd", "Jd"        # ["Ad", "Kd"]
            )

        >>> rank1 == rank2  # Both of them are evaluated by `A K 9 9 6`
        True
    """
    int_cards = list(map(Card.to_id, cards))
    hand_size = len(cards)

    if hand_size != TOTAL_CARD_COUNT:
        msg = (
            f"The number of cards must be {TOTAL_CARD_COUNT}.",
            f"passed size: {hand_size}",
        )
        raise ValueError(msg)

    return _pheval.evaluate_omaha_cards(*int_cards)
