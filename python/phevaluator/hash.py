from .tables import CHOOSE, DP


def hash_quinary(q: list[int], k: int) -> int:
    sum_numb = 0
    length = len(q)

    for rank, cnt in enumerate(q):
        if cnt == 0:
            continue

        sum_numb += DP[cnt][length - rank - 1][k]

        k -= cnt
        if k <= 0:
            break

    return sum_numb


def hash_binary(binary: int, k: int) -> int:
    sum_numb = 0
    length = 15

    for rank in range(length):
        if binary & (1 << rank):
            if length - rank - 1 >= k:
                sum_numb += CHOOSE[length - rank - 1][k]

            k -= 1
            if k == 0:
                break

    return sum_numb
