#include <phevaluator/card_sampler.h>

#include <array>
#include <chrono>
#include <numeric>
#include <random>
#include <utility>
#include <vector>

namespace card_sampler {
static unsigned seed =
    std::chrono::system_clock::now().time_since_epoch().count();
static std::default_random_engine generator(seed);

CardSampler::CardSampler(void) { std::iota(deck.begin(), deck.end(), 0); }

std::vector<int> CardSampler::sample(int size) {
  std::vector<int> ret;
  int residual_cards = deck.size();
  for (int i = 0; i < size; i++) {
    int target_index = generator() % residual_cards;
    int tail_index = residual_cards - 1;
    std::swap(deck[target_index], deck[tail_index]);
    ret.push_back(deck[tail_index]);
    residual_cards--;
  }
  return ret;
}
}  // namespace card_sampler
