from evaluator.dptables import DP


def hash_quinary(q, length, k):
  sum_numb = 0

  for i in range(length):
    sum_numb += DP[q[i]][length - i - 1][k]

    k -= q[i]

    if k <= 0:
      break

  return sum_numb
