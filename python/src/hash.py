from src.dptables import *


def hash_quinary(hand, lenbit, k):
  if isinstance(hand, int):
    hand = list(map(int, reversed("{:013d}".format(hand))))
  hash_ = 0
  for i in range(lenbit):
    hash_ += DP[hand[i]][lenbit-i-1][k]
    k -= hand[i]
    if k <= 0:
      break

  return hash_
