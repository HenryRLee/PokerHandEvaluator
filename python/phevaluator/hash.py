"""Module hashing cards."""
from .tables import CHOOSE, DP


def hash_quinary(quinary: list[int], num_cards: int) -> int:
    """Hash list of cards.

    Args:
        quinary (list[int]): List of the count of the cards.
        num_cards (int): The number of cards.

    Returns:
        int: hash value

    Examples:
        The cards `6 5 4 3 2` is expressed as {
            "quinary": [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            "num_cards": 5
        }

        The cards `A A K K Q Q` is expressed as {
            "quinary": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
            "num_cards": 6
        }
    """
    sum_numb = 0
    length = len(quinary)

    for rank, cnt in enumerate(quinary):
        if cnt:
            sum_numb += DP[cnt][length - rank - 1][num_cards]
            num_cards -= cnt

    return sum_numb


def hash_binary(binary: int, num_cards: int) -> int:
    """Hash binary.

    Args:
        binary (int): The binary expressing combination of the cards.
        num_cards (int): The number of the cards.

    Returns:
        int: hash value

    Examples:
        The cards `6 5 4 3 2` is expressed as {
            "binary": 0b11111,
            "num_cards": 5
        }

        The cards `A K Q J T 2` is expressed as {
            "binary": 0b1111100000001,
            "num_cards": 6
        }
    """
    sum_numb = 0
    length = 15

    for rank in range(length):

        if (binary >> rank) % 2:
            sum_numb += CHOOSE[length - rank - 1][num_cards]
            num_cards -= 1

    return sum_numb
