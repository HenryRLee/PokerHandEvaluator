#include <phevaluator/phevaluator.h>

#include <cassert>
#include <iostream>

int main() {
  /*
   * This demonstrated scenario is the same as the one shown in example 1.
   * Community cards: 9c 4c 4s 9d 4h (both players share these cards)
   * Player 1: Qc 6c
   * Player 2: 2c 9h
   */
  phevaluator::Rank rank1 =
      phevaluator::EvaluateCards("9c", "4c", "4s", "9d", "4h", "Qc", "6c");
  phevaluator::Rank rank2 =
      phevaluator::EvaluateCards("9c", "4c", "4s", "9d", "4h", "2c", "9h");

  // expected 292
  assert(rank1.value() == 292);
  std::cout << "The rank of the hand in player 1 is " << rank1.value()
            << std::endl;
  // expected 236
  assert(rank2.value() == 236);
  std::cout << "The rank of the hand in player 2 is " << rank2.value()
            << std::endl;

  assert(rank1 < rank2);
  std::cout << "Player 2 has a stronger hand" << std::endl;

  assert(rank2.category() == FULL_HOUSE);
  assert(rank2.describeCategory() == "Full House");
  std::cout << "Player 2 has a " << rank2.describeCategory() << std::endl;

  assert(rank2.describeRank() == "Nines Full over Fours");
  std::cout << "More specifically, player 2 has a " << rank2.describeRank()
            << std::endl;

  assert(rank2.describeSampleHand() == "99944");
  assert(!rank2.isFlush());
  std::cout << "The best hand from player 2 is " << rank2.describeSampleHand()
            << (rank2.isFlush() ? " in flush" : "") << std::endl;
}
