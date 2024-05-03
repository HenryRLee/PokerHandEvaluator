#include <phevaluator/phevaluator.h>

#include <cassert>
#include <iostream>

/*
 * This example uses library pheval7.
 * The library only contains the 7-card evaluator, which evaluates how strong
 * a hand is.
 * It doesn't include any rank describing methods, in order to save memory.
 * If you want to use the rank describing methods, use library pheval instead,
 * and follow `examples/cpp_example.cc`.
 */

int main() {
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

  assert(rank2.value() < rank1.value());
  std::cout
      << "Due to rank2.value() < rank1.value(), player 2 has a better hand"
      << std::endl;
}
