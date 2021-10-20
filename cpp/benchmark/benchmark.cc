#include <algorithm>
#include <vector>
#include <set>
#include <chrono>
#include <random>
#include <ranges>
#include "phevaluator/phevaluator.h"
#include "benchmark/benchmark.h"

using namespace phevaluator;

static void EvaluateAllFiveCards(benchmark::State& state) {
  for (auto _ : state) {
    for (int a = 0; a < 48; a++) {
      for (int b = a + 1; b < 49; b++) {
        for (int c = b + 1; c < 50; c++) {
          for (int d = c + 1; d < 51; d++) {
            for (int e = d + 1; e < 52; e++) {
              EvaluateCards(a, b, c, d, e);
            }
          }
        }
      }
    }
  }
}
BENCHMARK(EvaluateAllFiveCards);

static void EvaluateAllSixCards(benchmark::State& state) {
  for (auto _ : state) {
    for (int a = 0; a < 47; a++) {
      for (int b = a + 1; b < 48; b++) {
        for (int c = b + 1; c < 49; c++) {
          for (int d = c + 1; d < 50; d++) {
            for (int e = d + 1; e < 51; e++) {
              for (int f = e + 1; f < 52; f++) {
                EvaluateCards(a, b, c, d, e, f);
              }
            }
          }
        }
      }
    }
  }
}
BENCHMARK(EvaluateAllSixCards);

static void EvaluateAllSevenCards(benchmark::State& state) {
  for (auto _ : state) {
    for (int a = 0; a < 46; a++) {
      for (int b = a + 1; b < 47; b++) {
        for (int c = b + 1; c < 48; c++) {
          for (int d = c + 1; d < 49; d++) {
            for (int e = d + 1; e < 50; e++) {
              for (int f = e + 1; f < 51; f++) {
                for (int g = f + 1; g < 52; g++) {
                  EvaluateCards(a, b, c, d, e, f, g);
                }
              }
            }
          }
        }
      }
    }
  }
}
BENCHMARK(EvaluateAllSevenCards);

static unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
static std::default_random_engine generator(seed);

static std::vector<int> RandomCardSample(int size) {
  constexpr std::ranges::iota_view card_view(0, 52);
  auto ret = std::vector<int>(size);
  // must sample from view. if it's sampled from array/vector, return will be sorted in ascending order
  std::ranges::sample(card_view, ret.begin(), size, generator);
  return ret;
}

const int SIZE = 100;

static void EvaluateRandomFiveCards(benchmark::State& state) {
  std::vector<std::vector<int>> hands;

  for (int i = 0; i < SIZE; i++) {
    hands.push_back(RandomCardSample(5));
  }
  for (auto _ : state) {
    for (int i = 0; i < SIZE; i++) {
      EvaluateCards(hands[i][0],
                    hands[i][1],
                    hands[i][2],
                    hands[i][3],
                    hands[i][4]);
    }
  }
}
BENCHMARK(EvaluateRandomFiveCards);

static void EvaluateRandomSixCards(benchmark::State& state) {
  std::vector<std::vector<int>> hands;

  for (int i = 0; i < SIZE; i++) {
    hands.push_back(RandomCardSample(6));
  }

  for (auto _ : state) {
    for (int i = 0; i < SIZE; i++) {
      EvaluateCards(hands[i][0],
                    hands[i][1],
                    hands[i][2],
                    hands[i][3],
                    hands[i][4],
                    hands[i][5]);
    }
  }
}
BENCHMARK(EvaluateRandomSixCards);

static void EvaluateRandomSevenCards(benchmark::State& state) {
  std::vector<std::vector<int>> hands;

  for (int i = 0; i < SIZE; i++) {
    hands.push_back(RandomCardSample(7));
  }

  for (auto _ : state) {
    for (int i = 0; i < SIZE; i++) {
      EvaluateCards(hands[i][0],
                    hands[i][1],
                    hands[i][2],
                    hands[i][3],
                    hands[i][4],
                    hands[i][5],
                    hands[i][6]);
    }
  }
}
BENCHMARK(EvaluateRandomSevenCards);

static void EvaluateRandomOmahaCards(benchmark::State& state) {
  std::vector<std::vector<int>> hands;

  for (int i = 0; i < SIZE; i++) {
    hands.push_back(RandomCardSample(9));
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

BENCHMARK_MAIN();

