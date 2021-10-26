"""Module evaluating cards in Omaha game."""
from typing import Union

from .card import Card
from .hash import hash_binary, hash_quinary
from .tables import BINARIES_BY_ID, FLUSH, FLUSH_OMAHA, NO_FLUSH_OMAHA


def evaluate_omaha_cards(*cards: Union[int, str, Card]) -> int:
    """Evaluate cards in Omaha game.

    In the Omaha rule, players can make hand with 3 cards from the 5 community cards and
    2 cards from their own 4 hole cards, then totally 5 cards.
    This function selects the best combination and return its rank.

    Args:
        cards(Union[int, str, Card]): List of cards
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

        >>> rank1 == rank2 # Both of them are evaluated by `A K 9 9 6`
        True
    """
    int_cards = list(map(Card.to_id, cards))
    hand_size = len(cards)

    if hand_size != 9:
        raise ValueError(f"The number of cards must be 9. passed size: {hand_size}")

    community_cards = int_cards[:5]
    hole_cards = int_cards[5:]
    return _evaluate_omaha_cards(community_cards, hole_cards)


def _evaluate_omaha_cards(community_cards: list[int], hole_cards: list[int]) -> int:
    value_flush = 10000
    value_noflush = 10000
    suit_count_board = [0] * 4
    suit_count_hole = [0] * 4

    for community_card in community_cards:
        suit_count_board[community_card % 4] += 1

    for hole_card in hole_cards:
        suit_count_hole[hole_card % 4] += 1

    flush_suit = -1
    for i in range(4):
        if suit_count_board[i] >= 3 and suit_count_hole[i] >= 2:
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

        if flush_count_board == 3 and flush_count_hole == 2:
            value_flush = FLUSH[suit_binary_board | suit_binary_hole]

        else:
            padding = [0x0000, 0x2000, 0x6000]

            suit_binary_board |= padding[5 - flush_count_board]
            suit_binary_hole |= padding[4 - flush_count_hole]

            board_hash = hash_binary(suit_binary_board, 5)
            hole_hash = hash_binary(suit_binary_hole, 4)

            value_flush = FLUSH_OMAHA[board_hash * 1365 + hole_hash]

    quinary_board = [0] * 13
    quinary_hole = [0] * 13

    for community_card in community_cards:
        quinary_board[community_card // 4] += 1

    for hole_card in hole_cards:
        quinary_hole[hole_card // 4] += 1

    board_hash = hash_quinary(quinary_board, 5)
    hole_hash = hash_quinary(quinary_hole, 4)

    value_noflush = NO_FLUSH_OMAHA[board_hash * 1820 + hole_hash]

    return min(value_flush, value_noflush)
