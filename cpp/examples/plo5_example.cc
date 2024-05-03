#include <phevaluator/phevaluator.h>
#include <phevaluator/rank.h>

#include <cassert>
#include <iostream>

int main() {
  /*
   * Community cards: 4c 5c 6c 7s 8s
   * Player 1: 2c 9c As Kd Jh
   * Player 2: 6s 9s Ts Js 2s
   */
  phevaluator::Rank rank1 = phevaluator::EvaluatePlo5Cards(
      "4c", "5c", "6c", "7s", "8s",   // community cards
      "2c", "9c", "As", "Kd", "Jh");  // player hole cards
  phevaluator::Rank rank2 = phevaluator::EvaluatePlo5Cards(
      "4c", "5c", "6c", "7s", "8s",   // community cards
      "6s", "9s", "Ts", "Js", "2s");  // player hole cards

  /*
   * It seems that Player 2 can make a straight-flush, but that's not true.
   * Because each player can only select 3 cards from the community cards and 2
   * cards from his own hole cards, so Player 2 cannot get a straight-flush in
   * this example.
   *
   * Therefore the result is, Player 1 can make a 9-high flush in clubs, and
   * Player 2 can only make a 10-high straight.
   */
  assert(rank1.value() == 1578);
  std::cout << "Player 1 has:" << std::endl;
  std::cout << rank1.describeCategory() << std::endl;
  std::cout << rank1.describeRank() << std::endl;
  std::cout << rank1.describeSampleHand() << std::endl;

  std::cout << std::endl;

  assert(rank2.value() == 1604);
  std::cout << "Player 2 has:" << std::endl;
  std::cout << rank2.describeCategory() << std::endl;
  std::cout << rank2.describeRank() << std::endl;
  std::cout << rank2.describeSampleHand() << std::endl;

  return 0;
}
