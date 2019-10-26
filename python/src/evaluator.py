import numpy as np

from src.dptables import CHOOSE, DP, SUITS
from src.hash import hash_binary, hash_quinary
from src.hashtable import FLUSH
from src.hashtable5 import NO_FLUSH_5
from src.hashtable6 import NO_FLUSH_6
from src.hashtable7 import NO_FLUSH_7
from src.hashtable8 import NO_FLUSH_8
from src.hashtable9 import NO_FLUSH_9


binaries_by_id = np.power(2, np.repeat(range(13), 4), dtype=np.short)
suitbit_by_id = np.power(8, list(range(4)) * 13, dtype=np.short)

def evaluate_cards(*args):
  if len(args) == 9:
    return evaluate_9cards(args)

  suit_hash = 0
  value_flush = 10000
  value_noflush = 10000

  for card in args:
    suit_hash += suitbit_by_id[card]

  if SUITS[suit_hash]:
    suit_binary = np.zeros(4, dtype=np.int)
    for card in args:
      suit_bits = np.bitwise_and(card, 0x3)
      suit_binary[suit_bits] = np.bitwise_or(suit_binary[suit_bits], binaries_by_id[card])

    value_flush = FLUSH[suit_binary[SUITS[suit_hash]-1]]
    
    if len(args) < 8:
      return value_flush

  quinary = np.zeros(13, dtype=np.byte)

  for card in args:
    quinary[np.right_shift(card, 2)] += 1

  hash_val = hash_quinary(quinary, 13, len(args))

  if len(args) == 5:
    return NO_FLUSH_5[hash_val]
  elif len(args) == 6:
    return NO_FLUSH_6[hash_val]
  elif len(args) == 7:
    return NO_FLUSH_7[hash_val]
  elif len(args) == 8:
    value_noflush = NO_FLUSH_8[hash_val]

    if value_flush < value_noflush:
      return value_flush
    else:
      return value_noflush

def evaluate_9cards(*args):
  pass

