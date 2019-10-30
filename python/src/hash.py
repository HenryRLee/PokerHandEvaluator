from src.dptables import *


def hash_quinary(hand, lenbit, k):
  hash_ = 0
  for i in range(lenbit):
    hash_ += DP[hand[i]][lenbit-i-1][k]
    k -= hand[i]
    if k <= 0:
      break

  return hash_
