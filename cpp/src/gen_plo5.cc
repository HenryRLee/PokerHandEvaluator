// g++ -std=c++17 gen_plo5.cc hash.c evaluator_omaha.c dptables.c tables_omaha.c hashtable.c

#include <cstdio>
#include <cassert>
#include <algorithm>
#include <thread>
#include <mutex>
#include <vector>
#include <fstream>

static int percentage(long long numerator, long long denominator) {
  return numerator * 10000 / denominator;
}

#include "hash.h"
#include "tables.h"

static int hash_binary(const int binary, int k)
{
  int sum = 0;
  int i;
  const int len = 16;

  for (i=0; i<len; i++)
  {
    if (binary & (1 << i))
    {
      if (len-i-1 >= k)
        sum += choose[len-i-1][k];

      k--;

      if (k == 0)
      {
        break;
      }
    }
  }

  return sum;
}

extern "C" {
extern int evaluate_omaha_cards(int c1, int c2, int c3, int c4, int c5,
                                int h1, int h2, int h3, int h4);
}

static short binaries_by_id[52] = {
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
};

short my_noflush_plo5[6175 * 6175] = {0};
short my_flush_plo5[4368 * 4368] = {0};

/*
 * Card id, ranged from 0 to 51.
 * The two least significant bits represent the suit, ranged from 0-3.
 * The rest of it represent the rank, ranged from 0-12.
 * 13 * 4 gives 52 ids.
 *
 * The first five parameters are the community cards on the board
 * The last five parameters are the hole cards of the player
 */
void AssignPlo5Value(int c1, int c2, int c3, int c4, int c5,
                     int h1, int h2, int h3, int h4, int h5, short best) {
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

  if (best <= 10 || (best > 322 && best <= 1599)) {
    // flush
    for (int i = 0; i < 4; i++) {
      if (suit_count_board[i] >= 3 && suit_count_hole[i] >= 2) {
        int suit_binary_board[4] = {0};

        suit_binary_board[c1 & 0x3] |= binaries_by_id[c1];
        suit_binary_board[c2 & 0x3] |= binaries_by_id[c2];
        suit_binary_board[c3 & 0x3] |= binaries_by_id[c3];
        suit_binary_board[c4 & 0x3] |= binaries_by_id[c4];
        suit_binary_board[c5 & 0x3] |= binaries_by_id[c5];

        int suit_binary_hole[4] = {0};
        suit_binary_hole[h1 & 0x3] |= binaries_by_id[h1];
        suit_binary_hole[h2 & 0x3] |= binaries_by_id[h2];
        suit_binary_hole[h3 & 0x3] |= binaries_by_id[h3];
        suit_binary_hole[h4 & 0x3] |= binaries_by_id[h4];
        suit_binary_hole[h5 & 0x3] |= binaries_by_id[h5];

        if (suit_count_board[i] == 3 && suit_count_hole[i] == 2) {
          //value_flush = flush[suit_binary_board[i] | suit_binary_hole[i]];
        } else {
          const int padding[4] = {0x0000, 0x2000, 0x6000, 0xe000};

          suit_binary_board[i] |= padding[5 - suit_count_board[i]];
          suit_binary_hole[i] |= padding[5 - suit_count_hole[i]];

          const int board_hash = hash_binary(suit_binary_board[i], 5);
          const int hole_hash = hash_binary(suit_binary_hole[i], 5);
          const long long final_hash = board_hash * 4368 +  hole_hash;
          assert(board_hash < 4368);
          assert(hole_hash < 4368);
          assert(final_hash < (4368 * 4368));
          if (my_flush_plo5[final_hash] != 0)
            assert(my_flush_plo5[final_hash] == best);
          else
            my_flush_plo5[final_hash] = best;
          //value_flush = flush_plo5[final_hash];
        }

        break;
      }
    }
  } else {
    // no flush
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

    const int board_hash = hash_quinary(quinary_board, 5);
    const int hole_hash = hash_quinary(quinary_hole, 5);
    const int final_hash = board_hash * 6175 + hole_hash;
    assert(board_hash < 6175);
    assert(hole_hash < 6175);
    assert(final_hash < (6175 * 6175));

    if (my_noflush_plo5[final_hash] != 0)
      assert(my_noflush_plo5[final_hash] == best);
    else
      my_noflush_plo5[final_hash] = best;
  }
}

void IterateBestHands(int a, int b, int c, int d, int e,
                      int f, int g, int h, int i, int j) {
  int best = 20000;

  const int v0 = evaluate_omaha_cards(a, b, c, d, e, f, g, h, i);
  const int v1 = evaluate_omaha_cards(a, b, c, d, e, f, g, h, j);
  const int v2 = evaluate_omaha_cards(a, b, c, d, e, f, g, j, i);
  const int v3 = evaluate_omaha_cards(a, b, c, d, e, f, j, h, i);
  const int v4 = evaluate_omaha_cards(a, b, c, d, e, j, g, h, i);

  if (v0 < best) best = v0;
  if (v1 < best) best = v1;
  if (v2 < best) best = v2;
  if (v3 < best) best = v3;
  if (v4 < best) best = v4;

  AssignPlo5Value(a, b, c, d, e, f, g, h, i, j, best);
}

long long count = 0;
int progress = 0;
const long long total = (long long)3679075400 * 126;
std::mutex m;

const int ThreadNumber = 32;

void ThreadFunction(int thread) {
  std::fprintf(stderr, "Start thread %d\n", thread);

  for(int a = 0; a < 43; a++)
  {
    for(int b = a + 1; b < 44; b++)
    {
      for(int c = b + 1; c < 45; c++)
      {
        for(int d = c + 1; d < 46; d++)
        {
          for(int e = d + 1; e < 47; e++)
          {
            for(int f = e + 1; f < 48; f++)
            {
              int innerCount = 0;
              for(int g = f + 1; g < 49; g++)
              {
                for(int h = g + 1; h < 50; h++)
                {
                  for(int i = h + 1; i < 51; i++)
                  {
                    for(int j = i + 1; j < 52; j++)
                    {
                      int ten_choose_five[252][10] = {
                        {a, b, c, d, e, f, g, h, i, j},
                        {a, b, c, d, f, e, g, h, i, j},
                        {a, b, c, d, g, e, f, h, i, j},
                        {a, b, c, d, h, e, f, g, i, j},
                        {a, b, c, d, i, e, f, g, h, j},
                        {a, b, c, d, j, e, f, g, h, i},
                        {a, b, c, e, f, d, g, h, i, j},
                        {a, b, c, e, g, d, f, h, i, j},
                        {a, b, c, e, h, d, f, g, i, j},
                        {a, b, c, e, i, d, f, g, h, j},
                        {a, b, c, e, j, d, f, g, h, i},
                        {a, b, c, f, g, d, e, h, i, j},
                        {a, b, c, f, h, d, e, g, i, j},
                        {a, b, c, f, i, d, e, g, h, j},
                        {a, b, c, f, j, d, e, g, h, i},
                        {a, b, c, g, h, d, e, f, i, j},
                        {a, b, c, g, i, d, e, f, h, j},
                        {a, b, c, g, j, d, e, f, h, i},
                        {a, b, c, h, i, d, e, f, g, j},
                        {a, b, c, h, j, d, e, f, g, i},
                        {a, b, c, i, j, d, e, f, g, h},
                        {a, b, d, e, f, c, g, h, i, j},
                        {a, b, d, e, g, c, f, h, i, j},
                        {a, b, d, e, h, c, f, g, i, j},
                        {a, b, d, e, i, c, f, g, h, j},
                        {a, b, d, e, j, c, f, g, h, i},
                        {a, b, d, f, g, c, e, h, i, j},
                        {a, b, d, f, h, c, e, g, i, j},
                        {a, b, d, f, i, c, e, g, h, j},
                        {a, b, d, f, j, c, e, g, h, i},
                        {a, b, d, g, h, c, e, f, i, j},
                        {a, b, d, g, i, c, e, f, h, j},
                        {a, b, d, g, j, c, e, f, h, i},
                        {a, b, d, h, i, c, e, f, g, j},
                        {a, b, d, h, j, c, e, f, g, i},
                        {a, b, d, i, j, c, e, f, g, h},
                        {a, b, e, f, g, c, d, h, i, j},
                        {a, b, e, f, h, c, d, g, i, j},
                        {a, b, e, f, i, c, d, g, h, j},
                        {a, b, e, f, j, c, d, g, h, i},
                        {a, b, e, g, h, c, d, f, i, j},
                        {a, b, e, g, i, c, d, f, h, j},
                        {a, b, e, g, j, c, d, f, h, i},
                        {a, b, e, h, i, c, d, f, g, j},
                        {a, b, e, h, j, c, d, f, g, i},
                        {a, b, e, i, j, c, d, f, g, h},
                        {a, b, f, g, h, c, d, e, i, j},
                        {a, b, f, g, i, c, d, e, h, j},
                        {a, b, f, g, j, c, d, e, h, i},
                        {a, b, f, h, i, c, d, e, g, j},
                        {a, b, f, h, j, c, d, e, g, i},
                        {a, b, f, i, j, c, d, e, g, h},
                        {a, b, g, h, i, c, d, e, f, j},
                        {a, b, g, h, j, c, d, e, f, i},
                        {a, b, g, i, j, c, d, e, f, h},
                        {a, b, h, i, j, c, d, e, f, g},
                        {a, c, d, e, f, b, g, h, i, j},
                        {a, c, d, e, g, b, f, h, i, j},
                        {a, c, d, e, h, b, f, g, i, j},
                        {a, c, d, e, i, b, f, g, h, j},
                        {a, c, d, e, j, b, f, g, h, i},
                        {a, c, d, f, g, b, e, h, i, j},
                        {a, c, d, f, h, b, e, g, i, j},
                        {a, c, d, f, i, b, e, g, h, j},
                        {a, c, d, f, j, b, e, g, h, i},
                        {a, c, d, g, h, b, e, f, i, j},
                        {a, c, d, g, i, b, e, f, h, j},
                        {a, c, d, g, j, b, e, f, h, i},
                        {a, c, d, h, i, b, e, f, g, j},
                        {a, c, d, h, j, b, e, f, g, i},
                        {a, c, d, i, j, b, e, f, g, h},
                        {a, c, e, f, g, b, d, h, i, j},
                        {a, c, e, f, h, b, d, g, i, j},
                        {a, c, e, f, i, b, d, g, h, j},
                        {a, c, e, f, j, b, d, g, h, i},
                        {a, c, e, g, h, b, d, f, i, j},
                        {a, c, e, g, i, b, d, f, h, j},
                        {a, c, e, g, j, b, d, f, h, i},
                        {a, c, e, h, i, b, d, f, g, j},
                        {a, c, e, h, j, b, d, f, g, i},
                        {a, c, e, i, j, b, d, f, g, h},
                        {a, c, f, g, h, b, d, e, i, j},
                        {a, c, f, g, i, b, d, e, h, j},
                        {a, c, f, g, j, b, d, e, h, i},
                        {a, c, f, h, i, b, d, e, g, j},
                        {a, c, f, h, j, b, d, e, g, i},
                        {a, c, f, i, j, b, d, e, g, h},
                        {a, c, g, h, i, b, d, e, f, j},
                        {a, c, g, h, j, b, d, e, f, i},
                        {a, c, g, i, j, b, d, e, f, h},
                        {a, c, h, i, j, b, d, e, f, g},
                        {a, d, e, f, g, b, c, h, i, j},
                        {a, d, e, f, h, b, c, g, i, j},
                        {a, d, e, f, i, b, c, g, h, j},
                        {a, d, e, f, j, b, c, g, h, i},
                        {a, d, e, g, h, b, c, f, i, j},
                        {a, d, e, g, i, b, c, f, h, j},
                        {a, d, e, g, j, b, c, f, h, i},
                        {a, d, e, h, i, b, c, f, g, j},
                        {a, d, e, h, j, b, c, f, g, i},
                        {a, d, e, i, j, b, c, f, g, h},
                        {a, d, f, g, h, b, c, e, i, j},
                        {a, d, f, g, i, b, c, e, h, j},
                        {a, d, f, g, j, b, c, e, h, i},
                        {a, d, f, h, i, b, c, e, g, j},
                        {a, d, f, h, j, b, c, e, g, i},
                        {a, d, f, i, j, b, c, e, g, h},
                        {a, d, g, h, i, b, c, e, f, j},
                        {a, d, g, h, j, b, c, e, f, i},
                        {a, d, g, i, j, b, c, e, f, h},
                        {a, d, h, i, j, b, c, e, f, g},
                        {a, e, f, g, h, b, c, d, i, j},
                        {a, e, f, g, i, b, c, d, h, j},
                        {a, e, f, g, j, b, c, d, h, i},
                        {a, e, f, h, i, b, c, d, g, j},
                        {a, e, f, h, j, b, c, d, g, i},
                        {a, e, f, i, j, b, c, d, g, h},
                        {a, e, g, h, i, b, c, d, f, j},
                        {a, e, g, h, j, b, c, d, f, i},
                        {a, e, g, i, j, b, c, d, f, h},
                        {a, e, h, i, j, b, c, d, f, g},
                        {a, f, g, h, i, b, c, d, e, j},
                        {a, f, g, h, j, b, c, d, e, i},
                        {a, f, g, i, j, b, c, d, e, h},
                        {a, f, h, i, j, b, c, d, e, g},
                        {a, g, h, i, j, b, c, d, e, f},
                        {b, c, d, e, f, a, g, h, i, j},
                        {b, c, d, e, g, a, f, h, i, j},
                        {b, c, d, e, h, a, f, g, i, j},
                        {b, c, d, e, i, a, f, g, h, j},
                        {b, c, d, e, j, a, f, g, h, i},
                        {b, c, d, f, g, a, e, h, i, j},
                        {b, c, d, f, h, a, e, g, i, j},
                        {b, c, d, f, i, a, e, g, h, j},
                        {b, c, d, f, j, a, e, g, h, i},
                        {b, c, d, g, h, a, e, f, i, j},
                        {b, c, d, g, i, a, e, f, h, j},
                        {b, c, d, g, j, a, e, f, h, i},
                        {b, c, d, h, i, a, e, f, g, j},
                        {b, c, d, h, j, a, e, f, g, i},
                        {b, c, d, i, j, a, e, f, g, h},
                        {b, c, e, f, g, a, d, h, i, j},
                        {b, c, e, f, h, a, d, g, i, j},
                        {b, c, e, f, i, a, d, g, h, j},
                        {b, c, e, f, j, a, d, g, h, i},
                        {b, c, e, g, h, a, d, f, i, j},
                        {b, c, e, g, i, a, d, f, h, j},
                        {b, c, e, g, j, a, d, f, h, i},
                        {b, c, e, h, i, a, d, f, g, j},
                        {b, c, e, h, j, a, d, f, g, i},
                        {b, c, e, i, j, a, d, f, g, h},
                        {b, c, f, g, h, a, d, e, i, j},
                        {b, c, f, g, i, a, d, e, h, j},
                        {b, c, f, g, j, a, d, e, h, i},
                        {b, c, f, h, i, a, d, e, g, j},
                        {b, c, f, h, j, a, d, e, g, i},
                        {b, c, f, i, j, a, d, e, g, h},
                        {b, c, g, h, i, a, d, e, f, j},
                        {b, c, g, h, j, a, d, e, f, i},
                        {b, c, g, i, j, a, d, e, f, h},
                        {b, c, h, i, j, a, d, e, f, g},
                        {b, d, e, f, g, a, c, h, i, j},
                        {b, d, e, f, h, a, c, g, i, j},
                        {b, d, e, f, i, a, c, g, h, j},
                        {b, d, e, f, j, a, c, g, h, i},
                        {b, d, e, g, h, a, c, f, i, j},
                        {b, d, e, g, i, a, c, f, h, j},
                        {b, d, e, g, j, a, c, f, h, i},
                        {b, d, e, h, i, a, c, f, g, j},
                        {b, d, e, h, j, a, c, f, g, i},
                        {b, d, e, i, j, a, c, f, g, h},
                        {b, d, f, g, h, a, c, e, i, j},
                        {b, d, f, g, i, a, c, e, h, j},
                        {b, d, f, g, j, a, c, e, h, i},
                        {b, d, f, h, i, a, c, e, g, j},
                        {b, d, f, h, j, a, c, e, g, i},
                        {b, d, f, i, j, a, c, e, g, h},
                        {b, d, g, h, i, a, c, e, f, j},
                        {b, d, g, h, j, a, c, e, f, i},
                        {b, d, g, i, j, a, c, e, f, h},
                        {b, d, h, i, j, a, c, e, f, g},
                        {b, e, f, g, h, a, c, d, i, j},
                        {b, e, f, g, i, a, c, d, h, j},
                        {b, e, f, g, j, a, c, d, h, i},
                        {b, e, f, h, i, a, c, d, g, j},
                        {b, e, f, h, j, a, c, d, g, i},
                        {b, e, f, i, j, a, c, d, g, h},
                        {b, e, g, h, i, a, c, d, f, j},
                        {b, e, g, h, j, a, c, d, f, i},
                        {b, e, g, i, j, a, c, d, f, h},
                        {b, e, h, i, j, a, c, d, f, g},
                        {b, f, g, h, i, a, c, d, e, j},
                        {b, f, g, h, j, a, c, d, e, i},
                        {b, f, g, i, j, a, c, d, e, h},
                        {b, f, h, i, j, a, c, d, e, g},
                        {b, g, h, i, j, a, c, d, e, f},
                        {c, d, e, f, g, a, b, h, i, j},
                        {c, d, e, f, h, a, b, g, i, j},
                        {c, d, e, f, i, a, b, g, h, j},
                        {c, d, e, f, j, a, b, g, h, i},
                        {c, d, e, g, h, a, b, f, i, j},
                        {c, d, e, g, i, a, b, f, h, j},
                        {c, d, e, g, j, a, b, f, h, i},
                        {c, d, e, h, i, a, b, f, g, j},
                        {c, d, e, h, j, a, b, f, g, i},
                        {c, d, e, i, j, a, b, f, g, h},
                        {c, d, f, g, h, a, b, e, i, j},
                        {c, d, f, g, i, a, b, e, h, j},
                        {c, d, f, g, j, a, b, e, h, i},
                        {c, d, f, h, i, a, b, e, g, j},
                        {c, d, f, h, j, a, b, e, g, i},
                        {c, d, f, i, j, a, b, e, g, h},
                        {c, d, g, h, i, a, b, e, f, j},
                        {c, d, g, h, j, a, b, e, f, i},
                        {c, d, g, i, j, a, b, e, f, h},
                        {c, d, h, i, j, a, b, e, f, g},
                        {c, e, f, g, h, a, b, d, i, j},
                        {c, e, f, g, i, a, b, d, h, j},
                        {c, e, f, g, j, a, b, d, h, i},
                        {c, e, f, h, i, a, b, d, g, j},
                        {c, e, f, h, j, a, b, d, g, i},
                        {c, e, f, i, j, a, b, d, g, h},
                        {c, e, g, h, i, a, b, d, f, j},
                        {c, e, g, h, j, a, b, d, f, i},
                        {c, e, g, i, j, a, b, d, f, h},
                        {c, e, h, i, j, a, b, d, f, g},
                        {c, f, g, h, i, a, b, d, e, j},
                        {c, f, g, h, j, a, b, d, e, i},
                        {c, f, g, i, j, a, b, d, e, h},
                        {c, f, h, i, j, a, b, d, e, g},
                        {c, g, h, i, j, a, b, d, e, f},
                        {d, e, f, g, h, a, b, c, i, j},
                        {d, e, f, g, i, a, b, c, h, j},
                        {d, e, f, g, j, a, b, c, h, i},
                        {d, e, f, h, i, a, b, c, g, j},
                        {d, e, f, h, j, a, b, c, g, i},
                        {d, e, f, i, j, a, b, c, g, h},
                        {d, e, g, h, i, a, b, c, f, j},
                        {d, e, g, h, j, a, b, c, f, i},
                        {d, e, g, i, j, a, b, c, f, h},
                        {d, e, h, i, j, a, b, c, f, g},
                        {d, f, g, h, i, a, b, c, e, j},
                        {d, f, g, h, j, a, b, c, e, i},
                        {d, f, g, i, j, a, b, c, e, h},
                        {d, f, h, i, j, a, b, c, e, g},
                        {d, g, h, i, j, a, b, c, e, f},
                        {e, f, g, h, i, a, b, c, d, j},
                        {e, f, g, h, j, a, b, c, d, i},
                        {e, f, g, i, j, a, b, c, d, h},
                        {e, f, h, i, j, a, b, c, d, g},
                        {e, g, h, i, j, a, b, c, d, f},
                        {f, g, h, i, j, a, b, c, d, e},
                      };

                      const int Range = 8;
                      for (int k = thread * Range; k < thread * Range + Range && k < 252; k++) {
                        IterateBestHands(ten_choose_five[k][0],
                            ten_choose_five[k][1],
                            ten_choose_five[k][2],
                            ten_choose_five[k][3],
                            ten_choose_five[k][4],
                            ten_choose_five[k][5],
                            ten_choose_five[k][6],
                            ten_choose_five[k][7],
                            ten_choose_five[k][8],
                            ten_choose_five[k][9]);

                        innerCount++;
                      }
                    }
                  }
                }
              }

              std::lock_guard<std::mutex> lock(m);
              count += innerCount;

              if (percentage(count, total) > progress) {
                progress = percentage(count, total);
                std::fprintf(stderr, "Progress: %3.2f%%\n", 0.01 * progress);
              }
            }
          }
        }
      }
    }
  }

  std::fprintf(stderr, "Thread %d completes\n", thread);
}

int main() {
  std::vector<std::thread> threads(ThreadNumber);
  for (int i = 0; i < ThreadNumber; i++) {
    threads[i] = std::thread(ThreadFunction, i);
  }
  for (int i = 0; i < ThreadNumber; i++) {
    threads[i].join();
  }

  std::ofstream output;
  output.open("tables_plo5.c");

  std::printf("Complete %lld hands in total\n", count);

  output << "const short flush_plo5[4368 * 4368] = {";
  for (int i = 0; i < 4368 * 4368; i++) {
    if (i % 8 == 0) output << "\n";
    output << "  " << my_flush_plo5[i] << ",";
  }
  output << "};\n";

  output << "const short noflush_plo5[6175 * 6175] = {";
  for (int i = 0; i < 6175 * 6175; i++) {
    if (i % 8 == 0) output << "\n";
    output << "  " << my_noflush_plo5[i] << ",";
  }
  output << "};\n";
}
