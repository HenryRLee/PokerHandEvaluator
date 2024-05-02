"""Module evaluating cards in Omaha game."""

from __future__ import annotations

from .card import Card
from .hash import hash_binary
from .hash import hash_quinary
from .tables import BINARIES_BY_ID
from .tables import FLUSH
from .tables import FLUSH_OMAHA
from .tables import NO_FLUSH_OMAHA

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

    community_cards = int_cards[:COMMUNITY_CARD_COUNT]
    hole_cards = int_cards[COMMUNITY_CARD_COUNT:]
    return _evaluate_omaha_cards(community_cards, hole_cards)


# TODO(@azriel1rf): `_evaluate_omaha_cards` is too complex. Consider refactoring.
# https://github.com/HenryRLee/PokerHandEvaluator/issues/92
def _evaluate_omaha_cards(community_cards: list[int], hole_cards: list[int]) -> int:  # noqa: C901, PLR0912
    value_flush = 10000
    value_noflush = 10000
    suit_count_board = [0] * 4
    suit_count_hole = [0] * 4

    for community_card in community_cards:
        suit_count_board[community_card % 4] += 1

    for hole_card in hole_cards:
        suit_count_hole[hole_card % 4] += 1

    min_flush_count_board = 3
    min_flush_count_hole = 2

    flush_suit = -1
    for i in range(4):
        if (
            suit_count_board[i] >= min_flush_count_board
            and suit_count_hole[i] >= min_flush_count_hole
        ):
            flush_suit = i
            break

    if flush_suit != -1:
        flush_count_board = suit_count_board[flush_suit]
        flush_count_hole = suit_count_hole[flush_suit]

        suit_binary_board = 0
        for community_card in community_cards:
            if community_card % 4 == flush_suit:
                suit_binary_board |= BINARIES_BY_ID[community_card]

        suit_binary_hole = 0
        for hole_card in hole_cards:
            if hole_card % 4 == flush_suit:
                suit_binary_hole |= BINARIES_BY_ID[hole_card]

        if (
            flush_count_board == min_flush_count_board
            and flush_count_hole == min_flush_count_hole
        ):
            value_flush = FLUSH[suit_binary_board | suit_binary_hole]

        else:
            padding = [0x0000, 0x2000, 0x6000]

            suit_binary_board |= padding[COMMUNITY_CARD_COUNT - flush_count_board]
            suit_binary_hole |= padding[HOLE_CARD_COUNT - flush_count_hole]

            board_hash = hash_binary(suit_binary_board, COMMUNITY_CARD_COUNT)
            hole_hash = hash_binary(suit_binary_hole, HOLE_CARD_COUNT)

            value_flush = FLUSH_OMAHA[board_hash * 1365 + hole_hash]

    quinary_board = [0] * 13
    quinary_hole = [0] * 13

    for community_card in community_cards:
        quinary_board[community_card // 4] += 1

    for hole_card in hole_cards:
        quinary_hole[hole_card // 4] += 1

    board_hash = hash_quinary(quinary_board, COMMUNITY_CARD_COUNT)
    hole_hash = hash_quinary(quinary_hole, HOLE_CARD_COUNT)

    value_noflush = NO_FLUSH_OMAHA[board_hash * 1820 + hole_hash]

    return min(value_flush, value_noflush)
