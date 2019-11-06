from evaluator.hashtable import FLUSH
from evaluator.hashtable9 import NO_FLUSH_9
from evaluator.hash import hash_quinary

binaries_by_id = [
  0x1,  0x1,  0x1,  0x1,
  0x2,  0x2,  0x2,  0x2,
  0x4,  0x4,  0x4,  0x4,
  0x8,  0x8,  0x8,  0x8,
  0x10,  0x10,  0x10,  0x10,
  0x20,  0x20,  0x20,  0x20,
  0x40,  0x40,  0x40,  0x40,
  0x80,  0x80,  0x80,  0x80,
  0x100,  0x100,  0x100,  0x100,
  0x200,  0x200,  0x200,  0x200,
  0x400,  0x400,  0x400,  0x400,
  0x800,  0x800,  0x800,  0x800,
  0x1000,  0x1000,  0x1000,  0x1000,
]
suitbit_by_id = [0x1,  0x8,  0x40,  0x200,] * 13

def evaluate_9cards(a, b, c, d, e, f, g, h, i):
  suit_hash = 0
  value_flush = 10000
  value_no_flush = 10000
  suit_counter = [0] * 4

  suit_counter[a & 0x3] += 1
  suit_counter[b & 0x3] += 1
  suit_counter[c & 0x3] += 1
  suit_counter[d & 0x3] += 1
  suit_counter[e & 0x3] += 1
  suit_counter[f & 0x3] += 1
  suit_counter[g & 0x3] += 1
  suit_counter[h & 0x3] += 1
  suit_counter[i & 0x3] += 1

  for l in range(4):
    if suit_counter[l] >= 5:
      suit_binary = [0] * 4

      suit_binary[a & 0x3] |= binaries_by_id[a]
      suit_binary[b & 0x3] |= binaries_by_id[b]
      suit_binary[c & 0x3] |= binaries_by_id[c]
      suit_binary[d & 0x3] |= binaries_by_id[d]
      suit_binary[e & 0x3] |= binaries_by_id[e]
      suit_binary[f & 0x3] |= binaries_by_id[f]
      suit_binary[g & 0x3] |= binaries_by_id[g]
      suit_binary[h & 0x3] |= binaries_by_id[h]
      suit_binary[i & 0x3] |= binaries_by_id[i]

      value_flush = FLUSH[suit_binary[l]]
      break

  quinary = [0] * 13

  quinary[a >> 2] += 1
  quinary[b >> 2] += 1
  quinary[c >> 2] += 1
  quinary[d >> 2] += 1
  quinary[e >> 2] += 1
  quinary[f >> 2] += 1
  quinary[g >> 2] += 1
  quinary[h >> 2] += 1
  quinary[i >> 2] += 1

  hash_value = hash_quinary(quinary, 13, 9)

  value_no_flush = NO_FLUSH_9[hash_value]

  if value_flush < value_no_flush:
    return value_flush
  else:
    return value_no_flush
