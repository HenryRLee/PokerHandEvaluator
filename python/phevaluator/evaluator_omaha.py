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

    return _evaluate_omaha_cards(*int_cards)


def _evaluate_omaha_cards(
    c1: int, c2: int, c3: int, c4: int, c5: int, h1: int, h2: int, h3: int, h4: int
) -> int:
    value_flush = 10000
    value_noflush = 10000
    suit_count_board = [0, 0, 0, 0]
    suit_count_hole = [0, 0, 0, 0]

    suit_count_board[c1 & 0x3] += 1
    suit_count_board[c2 & 0x3] += 1
    suit_count_board[c3 & 0x3] += 1
    suit_count_board[c4 & 0x3] += 1
    suit_count_board[c5 & 0x3] += 1

    suit_count_hole[h1 & 0x3] += 1
    suit_count_hole[h2 & 0x3] += 1
    suit_count_hole[h3 & 0x3] += 1
    suit_count_hole[h4 & 0x3] += 1

    for i in range(4):
        if suit_count_board[i] >= 3 and suit_count_hole[i] >= 2:
            suit_binary_board = [0, 0, 0, 0]

            suit_binary_board[c1 & 0x3] |= BINARIES_BY_ID[c1]
            suit_binary_board[c2 & 0x3] |= BINARIES_BY_ID[c2]
            suit_binary_board[c3 & 0x3] |= BINARIES_BY_ID[c3]
            suit_binary_board[c4 & 0x3] |= BINARIES_BY_ID[c4]
            suit_binary_board[c5 & 0x3] |= BINARIES_BY_ID[c5]

            suit_binary_hole = [0, 0, 0, 0]
            suit_binary_hole[h1 & 0x3] |= BINARIES_BY_ID[h1]
            suit_binary_hole[h2 & 0x3] |= BINARIES_BY_ID[h2]
            suit_binary_hole[h3 & 0x3] |= BINARIES_BY_ID[h3]
            suit_binary_hole[h4 & 0x3] |= BINARIES_BY_ID[h4]

            if suit_count_board[i] == 3 and suit_count_hole[i] == 2:
                value_flush = FLUSH[suit_binary_board[i] | suit_binary_hole[i]]
            else:
                padding = [0x0000, 0x2000, 0x6000]

                suit_binary_board[i] |= padding[5 - suit_count_board[i]]
                suit_binary_hole[i] |= padding[4 - suit_count_hole[i]]

                board_hash = hash_binary(suit_binary_board[i], 5)
                hole_hash = hash_binary(suit_binary_hole[i], 4)

                value_flush = FLUSH_OMAHA[board_hash * 1365 + hole_hash]

            break

    quinary_board = [0] * 13
    quinary_hole = [0] * 13

    quinary_board[(c1 >> 2)] += 1
    quinary_board[(c2 >> 2)] += 1
    quinary_board[(c3 >> 2)] += 1
    quinary_board[(c4 >> 2)] += 1
    quinary_board[(c5 >> 2)] += 1

    quinary_hole[(h1 >> 2)] += 1
    quinary_hole[(h2 >> 2)] += 1
    quinary_hole[(h3 >> 2)] += 1
    quinary_hole[(h4 >> 2)] += 1

    board_hash = hash_quinary(quinary_board, 5)
    hole_hash = hash_quinary(quinary_hole, 4)

    value_noflush = NO_FLUSH_OMAHA[board_hash * 1820 + hole_hash]

    if value_flush < value_noflush:
        return value_flush
    else:
        return value_noflush
