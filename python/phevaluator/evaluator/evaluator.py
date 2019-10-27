import numpy as np

from evaluator.card import Card
from evaluator.dptables import CHOOSE, DP, SUITS
from evaluator.hash import hash_quinary
from evaluator.hashtable import FLUSH
from evaluator.hashtable5 import NO_FLUSH_5
from evaluator.hashtable6 import NO_FLUSH_6
from evaluator.hashtable7 import NO_FLUSH_7
from evaluator.hashtable8 import NO_FLUSH_8
from evaluator.hashtable9 import NO_FLUSH_9


binaries_by_id = np.power(2, np.repeat(range(13), 4), dtype=np.short)
suitbit_by_id = np.power(8, list(range(4)) * 13, dtype=np.short)

def evaluate_cards(*args):
  cards = np.vectorize(Card)(args)
  suit_hash = 0
  value_flush = 10000
  value_noflush = 10000

  if len(cards) == 9:
    suit_counter = np.zeros(4, dtype=np.byte)
    for card in cards:
      suit_counter[np.bitwise_and(card, 0x3)] += 1
    
    for i in range(4):
      if suit_counter[i] >= 5:
        suit_binary = np.zeros(4, dtype=np.int)
        for card in cards:
          suit_bits = np.bitwise_and(card, 0x3)
          suit_binary[suit_bits] = np.bitwise_or(suit_binary[suit_bits], binaries_by_id[card])

        value_flush = FLUSH[suit_binary[i]]
        break

  else:
    for card in cards:
      suit_hash += suitbit_by_id[card]

    if SUITS[suit_hash]:
      suit_binary = np.zeros(4, dtype=np.int)
      for card in cards:
        suit_bits = np.bitwise_and(card, 0x3)
        suit_binary[suit_bits] = np.bitwise_or(suit_binary[suit_bits], binaries_by_id[card])

      value_flush = FLUSH[suit_binary[SUITS[suit_hash]-1]]
      
      if len(cards) < 8:
        return value_flush

  quinary = np.zeros(13, dtype=np.byte)

  for card in cards:
    quinary[np.right_shift(card, 2)] += 1

  hash_val = hash_quinary(quinary, 13, len(cards))

  if len(cards) == 5:
    return NO_FLUSH_5[hash_val]
  elif len(cards) == 6:
    return NO_FLUSH_6[hash_val]
  elif len(cards) == 7:
    return NO_FLUSH_7[hash_val]
  elif len(cards) == 8:
    value_noflush = NO_FLUSH_8[hash_val]
  elif len(cards) == 9:
    value_noflush = NO_FLUSH_9[hash_val]

  if value_flush < value_noflush:
    return value_flush
  else:
    return value_noflush
