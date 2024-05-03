#include <phevaluator/phevaluator.h>

#include <cassert>
#include <iostream>

/*
 * This example uses library pheval6.
 * The library only contains the 6-card evaluator, which evaluates how strong
 * a hand is.
 * It doesn't include any rank describing methods, in order to save memory.
 * If you want to use the rank describing methods, use library pheval instead,
 * and follow `examples/cpp_example.cc`.
 */

int main() {
  phevaluator::Rank rank1 =
      phevaluator::EvaluateCards("9c", "4c", "4s", "9d", "4h", "7d");
  phevaluator::Rank rank2 =
      phevaluator::EvaluateCards("8c", "7c", "6s", "5d", "4s", "2s");

  assert(rank1.value() == 292);
  std::cout << "The rank of the hand in player 1 is " << rank1.value()
            << std::endl;

  assert(rank2.value() == 1606);
  std::cout << "The rank of the hand in player 2 is " << rank2.value()
            << std::endl;

  assert(rank1.value() < rank2.value());
  std::cout
      << "Due to rank1.value() < rank2.value(), player 1 has a stronger hand"
      << std::endl;
}
