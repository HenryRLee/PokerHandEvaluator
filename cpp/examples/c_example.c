#include <assert.h>
#include <phevaluator/phevaluator.h>
#include <phevaluator/rank.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * This C code is a demonstration of how to calculate the card id, which will
 * be used as the parameter in the evaluator. It also shows how to use the
 * return value to determine which hand is the stronger one.
 */
int main() {
  /*
   * In this example we use a scenario in the game Texas Holdem:
   * Community cards: 9c 4c 4s 9d 4h (both players share these cards)
   * Player 1: Qc 6c
   * Player 2: 2c 9h
   *
   * Both players have full houses, but player 1 has only a four full house
   * while player 2 has a nine full house.
   *
   * The result is player 2 has a stronger hand than player 1.
   */

  /*
   * To calculate the value of each card, we can either use the Card Id
   * mapping table, or use the formula rank * 4 + suit to get the value
   *
   * More specifically, the ranks are:
   *
   * deuce = 0, trey = 1, four = 2, five = 3, six = 4, seven = 5, eight = 6,
   * nine = 7, ten = 8, jack = 9, queen = 10, king = 11, ace = 12.
   *
   * And the suits are:
   * club = 0, diamond = 1, heart = 2, spade = 3
   */
  // Community cards
  int a = 7 * 4 + 0;  // 9c
  int b = 2 * 4 + 0;  // 4c
  int c = 2 * 4 + 3;  // 4s
  int d = 7 * 4 + 1;  // 9d
  int e = 2 * 4 + 2;  // 4h

  // Player 1
  int f = 10 * 4 + 0;  // Qc
  int g = 4 * 4 + 0;   // 6c

  // Player 2
  int h = 0 * 4 + 0;  // 2c
  int i = 7 * 4 + 2;  // 9h

  // Evaluating the hand of player 1
  int rank1 = evaluate_7cards(a, b, c, d, e, f, g);
  // Evaluating the hand of player 2
  int rank2 = evaluate_7cards(a, b, c, d, e, h, i);

  assert(rank1 == 292);
  assert(rank2 == 236);

  printf("The rank of the hand in player 1 is %d\n", rank1);  // expected 292
  printf("The rank of the hand in player 2 is %d\n", rank2);  // expected 236
  printf("Player 2 has a stronger hand\n");

  // Since the return value of the hand in player 2 is less than player 1,
  // it's considered to be a higher rank and stronger hand.
  // So player 2 beats player 1.

  enum rank_category category = get_rank_category(rank2);
  assert(category == FULL_HOUSE);
  const char* rank_category_description = describe_rank_category(category);
  assert(strcmp(rank_category_description, "Full House") == 0);
  printf("Player 2 has a %s\n", rank_category_description);

  const char* rank_description = describe_rank(rank2);
  printf("More specifically, player 2 has a %s\n", rank_description);
  assert(strcmp(rank_description, "Nines Full over Fours") == 0);

  const char* rank_sample_hand = describe_sample_hand(rank2);
  printf("The best hand from player 2 is %s %s\n", rank_sample_hand,
         is_flush(rank2) ? "flush" : "");
  assert(strcmp(rank_sample_hand, "99944") == 0);
  assert(!is_flush(rank2));

  return 0;
}
