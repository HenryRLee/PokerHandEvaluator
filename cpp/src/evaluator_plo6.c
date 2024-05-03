/*
 *  Copyright 2016-2023 Henry Lee
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

#include "hash.h"
#include "tables.h"

/*
 * Card id, ranged from 0 to 51.
 * The two least significant bits represent the suit, ranged from 0-3.
 * The rest of it represent the rank, ranged from 0-12.
 * 13 * 4 gives 52 ids.
 *
 * The first five parameters are the community cards on the board
 * The last six parameters are the hole cards of the player
 */
int evaluate_plo6_cards(int c1, int c2, int c3, int c4, int c5, int h1, int h2,
                        int h3, int h4, int h5, int h6) {
  int value_flush = 10000;
  int value_noflush = 10000;
  int suit_count_board[4] = {0};
  int suit_count_hole[4] = {0};

  suit_count_board[c1 & 0x3]++;
  suit_count_board[c2 & 0x3]++;
  suit_count_board[c3 & 0x3]++;
  suit_count_board[c4 & 0x3]++;
  suit_count_board[c5 & 0x3]++;

  suit_count_hole[h1 & 0x3]++;
  suit_count_hole[h2 & 0x3]++;
  suit_count_hole[h3 & 0x3]++;
  suit_count_hole[h4 & 0x3]++;
  suit_count_hole[h5 & 0x3]++;
  suit_count_hole[h6 & 0x3]++;

  for (int i = 0; i < 4; i++) {
    if (suit_count_board[i] >= 3 && suit_count_hole[i] >= 2) {
      // flush
      int suit_binary_board[4] = {0};
      suit_binary_board[c1 & 0x3] |= bit_of_div_4[c1];  // (1 << (c1 / 4))
      suit_binary_board[c2 & 0x3] |= bit_of_div_4[c2];  // (1 << (c2 / 4))
      suit_binary_board[c3 & 0x3] |= bit_of_div_4[c3];  // (1 << (c3 / 4))
      suit_binary_board[c4 & 0x3] |= bit_of_div_4[c4];  // (1 << (c4 / 4))
      suit_binary_board[c5 & 0x3] |= bit_of_div_4[c5];  // (1 << (c5 / 4))

      int suit_binary_hole[4] = {0};
      suit_binary_hole[h1 & 0x3] |= bit_of_div_4[h1];  // (1 << (h1 / 4))
      suit_binary_hole[h2 & 0x3] |= bit_of_div_4[h2];  // (1 << (h2 / 4))
      suit_binary_hole[h3 & 0x3] |= bit_of_div_4[h3];  // (1 << (h3 / 4))
      suit_binary_hole[h4 & 0x3] |= bit_of_div_4[h4];  // (1 << (h4 / 4))
      suit_binary_hole[h5 & 0x3] |= bit_of_div_4[h5];  // (1 << (h5 / 4))
      suit_binary_hole[h6 & 0x3] |= bit_of_div_4[h6];  // (1 << (h6 / 4))

      if (suit_count_board[i] == 3 && suit_count_hole[i] == 2) {
        value_flush = flush[suit_binary_board[i] | suit_binary_hole[i]];
      } else {
        const long long final_hash =
            suit_binary_board[i] * 8192 + suit_binary_hole[i];
        value_flush = flush_plo6[final_hash];
      }
      break;
    }
  }

  unsigned char quinary_board[13] = {0};
  unsigned char quinary_hole[13] = {0};

  quinary_board[(c1 >> 2)]++;
  quinary_board[(c2 >> 2)]++;
  quinary_board[(c3 >> 2)]++;
  quinary_board[(c4 >> 2)]++;
  quinary_board[(c5 >> 2)]++;

  quinary_hole[(h1 >> 2)]++;
  quinary_hole[(h2 >> 2)]++;
  quinary_hole[(h3 >> 2)]++;
  quinary_hole[(h4 >> 2)]++;
  quinary_hole[(h5 >> 2)]++;
  quinary_hole[(h6 >> 2)]++;

  const int board_hash = hash_quinary(quinary_board, 5);
  const int hole_hash = hash_quinary(quinary_hole, 6);

  value_noflush = noflush_plo6[board_hash * 18395 + hole_hash];

  if (value_flush < value_noflush)
    return value_flush;
  else
    return value_noflush;
}
