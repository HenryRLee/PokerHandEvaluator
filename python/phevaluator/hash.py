from .tables import CHOOSE, DP


def hash_quinary(quinary: list[int], k: int) -> int:
    sum_numb = 0
    length = len(quinary)

    for rank, cnt in enumerate(quinary):
        if cnt == 0:
            continue

        sum_numb += DP[cnt][length - rank - 1][k]

        k -= cnt
        if k <= 0:
            break

    return sum_numb


def hash_binary(binary: int, num_cards: int) -> int:
    sum_numb = 0
    length = 15

    for rank in range(length):
        if (binary >> rank) % 2:
            sum_numb += CHOOSE[length - rank - 1][num_cards]
            num_cards -= 1

    return sum_numb
