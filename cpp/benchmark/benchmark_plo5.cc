#include "benchmark/benchmark.h"
#include "phevaluator/card_sampler.h"
#include "phevaluator/phevaluator.h"

using namespace phevaluator;

const int SIZE = 100;

static void EvaluateRandomPlo5Cards(benchmark::State& state) {
  std::vector<std::vector<int>> hands;
  card_sampler::CardSampler cs{};

  for (int i = 0; i < SIZE; i++) {
    hands.push_back(cs.sample(10));
  }

  for (auto _ : state) {
    for (int i = 0; i < SIZE; i++) {
      EvaluatePlo5Cards(hands[i][0], hands[i][1], hands[i][2], hands[i][3],
                        hands[i][4], hands[i][5], hands[i][6], hands[i][7],
                        hands[i][8], hands[i][9]);
    }
  }
}
BENCHMARK(EvaluateRandomPlo5Cards);
