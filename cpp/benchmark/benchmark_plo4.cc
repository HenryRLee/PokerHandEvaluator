#include "benchmark/benchmark.h"
#include "phevaluator/card_sampler.h"
#include "phevaluator/phevaluator.h"

using namespace phevaluator;

const int SIZE = 100;

static void EvaluateRandomPlo4Cards(benchmark::State& state) {
  std::vector<std::vector<int>> hands;
  card_sampler::CardSampler cs{};

  for (int i = 0; i < SIZE; i++) {
    hands.push_back(cs.sample(9));
  }

  for (auto _ : state) {
    for (int i = 0; i < SIZE; i++) {
      EvaluatePlo4Cards(hands[i][0], hands[i][1], hands[i][2], hands[i][3],
                        hands[i][4], hands[i][5], hands[i][6], hands[i][7],
                        hands[i][8]);
    }
  }
}
BENCHMARK(EvaluateRandomPlo4Cards);
