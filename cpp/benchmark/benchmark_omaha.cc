#include "phevaluator/phevaluator.h"
#include "benchmark/benchmark.h"
#include "card_sampler.h"

using namespace phevaluator;

const int SIZE = 100;

static void EvaluateRandomOmahaCards(benchmark::State& state) {
  std::vector<std::vector<int>> hands;
  CardSampler cs{};

  for (int i = 0; i < SIZE; i++) {
    hands.push_back(cs.sample(9));
  }

  for (auto _ : state) {
    for (int i = 0; i < SIZE; i++) {
      EvaluateOmahaCards(hands[i][0],
                         hands[i][1],
                         hands[i][2],
                         hands[i][3],
                         hands[i][4],
                         hands[i][5],
                         hands[i][6],
                         hands[i][7],
                         hands[i][8]);
    }
  }
}
BENCHMARK(EvaluateRandomOmahaCards);
