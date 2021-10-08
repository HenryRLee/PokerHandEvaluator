from evaluator.dptables import DP
from evaluator.dptables import CHOOSE


def hash_quinary(q, length, k):
    sum_numb = 0

    for i in range(length):
        sum_numb += DP[q[i]][length - i - 1][k]

        k -= q[i]

        if k <= 0:
            break

    return sum_numb


def hash_binary(binary, k):
    sum_numb = 0
    length = 15

    for i in range(length):
        if binary & (1 << i):
            if length - i - 1 >= k:
                sum_numb += CHOOSE[length - i - 1][k]

            k -= 1

            if k == 0:
                break

    return sum_numb
