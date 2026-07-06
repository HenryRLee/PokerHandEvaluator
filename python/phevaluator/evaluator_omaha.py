"""Module evaluating cards in Omaha game."""

from __future__ import annotations

from . import _pheval
from .card import Card

COMMUNITY_CARD_COUNT = 5
HOLE_CARD_COUNT = 4
TOTAL_CARD_COUNT = COMMUNITY_CARD_COUNT + HOLE_CARD_COUNT

# Total number of cards for each Pot Limit Omaha variant (5 community cards plus
# the variant's hole cards).
PLO4_CARD_COUNT = COMMUNITY_CARD_COUNT + 4
PLO5_CARD_COUNT = COMMUNITY_CARD_COUNT + 5
PLO6_CARD_COUNT = COMMUNITY_CARD_COUNT + 6


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


def _evaluate_plo_cards(
    cards: tuple[int | str | Card, ...], expected_count: int, func_name: str
) -> int:
    """Convert cards and dispatch to a native PLO evaluator.

    Args:
        cards: The community cards followed by the hole cards.
        expected_count: The required total number of cards.
        func_name: The native ``_pheval`` function to call.

    Raises:
        ValueError: The number of cards is not ``expected_count``.
        NotImplementedError: The variant was not compiled into the extension.

    Returns:
        int: The rank of the hand. Smaller is stronger.
    """
    if len(cards) != expected_count:
        msg = f"The number of cards must be {expected_count}. passed size: {len(cards)}"
        raise ValueError(msg)

    func = getattr(_pheval, func_name, None)
    if func is None:
        msg = (
            f"{func_name} is unavailable because the required lookup tables were "
            "not compiled. Rebuild the package from the repository with the "
            "PHEVALUATOR_BUILD_PLO environment variable set, e.g. "
            "`PHEVALUATOR_BUILD_PLO=5,6 pip install .`."
        )
        raise NotImplementedError(msg)

    return func(*map(Card.to_id, cards))


def evaluate_plo4_cards(*cards: int | str | Card) -> int:
    """Evaluate a Pot Limit Omaha (4 hole cards) hand.

    This is equivalent to :func:`evaluate_omaha_cards`.

    Args:
        cards(int | str | Card): Five community cards followed by four hole cards.

    Raises:
        ValueError: The number of cards is not 9.

    Returns:
        int: The rank of the hand. Smaller is stronger.
    """
    return _evaluate_plo_cards(cards, PLO4_CARD_COUNT, "evaluate_plo4_cards")


def evaluate_plo5_cards(*cards: int | str | Card) -> int:
    """Evaluate a 5-card Pot Limit Omaha (PLO5) hand.

    Requires the package to be built with PLO5 support (see
    ``PHEVALUATOR_BUILD_PLO``).

    Args:
        cards(int | str | Card): Five community cards followed by five hole cards.

    Raises:
        ValueError: The number of cards is not 10.
        NotImplementedError: The package was not built with PLO5 support.

    Returns:
        int: The rank of the hand. Smaller is stronger.
    """
    return _evaluate_plo_cards(cards, PLO5_CARD_COUNT, "evaluate_plo5_cards")


def evaluate_plo6_cards(*cards: int | str | Card) -> int:
    """Evaluate a 6-card Pot Limit Omaha (PLO6) hand.

    Requires the package to be built with PLO6 support (see
    ``PHEVALUATOR_BUILD_PLO``).

    Args:
        cards(int | str | Card): Five community cards followed by six hole cards.

    Raises:
        ValueError: The number of cards is not 11.
        NotImplementedError: The package was not built with PLO6 support.

    Returns:
        int: The rank of the hand. Smaller is stronger.
    """
    return _evaluate_plo_cards(cards, PLO6_CARD_COUNT, "evaluate_plo6_cards")
