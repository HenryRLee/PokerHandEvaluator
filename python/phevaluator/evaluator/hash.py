from evaluator.dptables import DP, CHOOSE


def hash_quinary(q, length, k):
  sum_numb = 0

  for i in range(0, length):
    sum_numb += DP[q[i]][length - i - 1][k]

    k -= q[i]

    if k <= 0:
      break

  return sum_numb

def hash_binary(q, length, k):
  sum_numb = 0

  for i in range(0, length):
    if q[i]:
      if length - i - 1 >= k:
        sum_numb += CHOOSE[length - i - 1][k]

      k -= 1
    
    if k == 0:
      break

  return sum_numb
