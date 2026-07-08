"""Module evaluating cards."""

from __future__ import annotations

from . import _pheval
from .card import Card

MIN_CARDS = 5
MAX_CARDS = 7

# Map the number of cards to the matching native evaluator function.
_EVALUATORS = {
    5: _pheval.evaluate_5cards,
    6: _pheval.evaluate_6cards,
    7: _pheval.evaluate_7cards,
}


def evaluate_cards(*cards: int | str | Card) -> int:
    """Evaluate cards for the best five cards.

    This function selects the best combination of the five cards from given cards and
    return its rank.
    The number of cards must be between 5 and 7.

    Args:
        cards(int | str | Card): List of cards

    Raises:
        ValueError: Unsupported size of the cards

    Returns:
        int: The rank of the given cards with the best five cards. Smaller is stronger.

    Examples:
        >>> rank1 = evaluate_cards("Ac", "Ad", "Ah", "As", "Kc")
        >>> rank2 = evaluate_cards("Ac", "Ad", "Ah", "As", "Kd")
        >>> rank3 = evaluate_cards("Ac", "Ad", "Ah", "As", "Kc", "Qh")
        >>> rank1 == rank2 == rank3  # Those three are evaluated by `A A A A K`
        True
    """
    int_cards = list(map(Card.to_id, cards))
    hand_size = len(cards)

    if not (MIN_CARDS <= hand_size <= MAX_CARDS) or (hand_size not in _EVALUATORS):
        msg = (
            f"The number of cards must be between {MIN_CARDS} and {MAX_CARDS}."
            f"passed size: {hand_size}"
        )
        raise ValueError(msg)

    return _EVALUATORS[hand_size](*int_cards)


def evaluate_5cards(
    a: int | str | Card,
    b: int | str | Card,
    c: int | str | Card,
    d: int | str | Card,
    e: int | str | Card,
) -> int:
    """Evaluate exactly five cards and return their rank.

    Args:
        a, b, c, d, e (int | str | Card): The five cards.

    Returns:
        int: The rank of the hand. Smaller is stronger (1 is the strongest).

    Examples:
        >>> evaluate_5cards("Ac", "Ad", "Ah", "As", "Kc")
        11
    """
    return _pheval.evaluate_5cards(
        Card.to_id(a), Card.to_id(b), Card.to_id(c), Card.to_id(d), Card.to_id(e)
    )


def evaluate_6cards(  # noqa: PLR0913
    a: int | str | Card,
    b: int | str | Card,
    c: int | str | Card,
    d: int | str | Card,
    e: int | str | Card,
    f: int | str | Card,
) -> int:
    """Evaluate the best five of six cards and return their rank.

    Args:
        a, b, c, d, e, f (int | str | Card): The six cards.

    Returns:
        int: The rank of the best five-card hand. Smaller is stronger.
    """
    return _pheval.evaluate_6cards(
        Card.to_id(a),
        Card.to_id(b),
        Card.to_id(c),
        Card.to_id(d),
        Card.to_id(e),
        Card.to_id(f),
    )


def evaluate_7cards(  # noqa: PLR0913
    a: int | str | Card,
    b: int | str | Card,
    c: int | str | Card,
    d: int | str | Card,
    e: int | str | Card,
    f: int | str | Card,
    g: int | str | Card,
) -> int:
    """Evaluate the best five of seven cards and return their rank.

    Args:
        a, b, c, d, e, f, g (int | str | Card): The seven cards.

    Returns:
        int: The rank of the best five-card hand. Smaller is stronger.
    """
    return _pheval.evaluate_7cards(
        Card.to_id(a),
        Card.to_id(b),
        Card.to_id(c),
        Card.to_id(d),
        Card.to_id(e),
        Card.to_id(f),
        Card.to_id(g),
    )
