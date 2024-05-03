#include <phevaluator/card_sampler.h>
#include <phevaluator/phevaluator.h>
#include <phevaluator/rank.h>

#include <algorithm>
#include <cstdio>
#include <string>
#include <vector>

#include "gtest/gtest.h"
#include "kev/kev_eval.h"

using namespace phevaluator;

static int percentage(long long numerator, long long denominator) {
  return numerator * 100 / denominator;
}

static card_sampler::CardSampler cs{};

static short IterateKevEval(int a, int b, int c, int d, int e, int f, int g,
                            int h, int i, int j, int k) {
  short best = 20000;

  int board[10][3] = {
      {a, b, c}, {a, b, d}, {a, b, e}, {a, c, d}, {a, c, e},
      {a, d, e}, {b, c, d}, {b, c, e}, {b, d, e}, {c, d, e},
  };
  int hole[15][2] = {
      {f, g}, {f, h}, {f, i}, {f, j}, {f, k}, {g, h}, {g, i}, {g, j},
      {g, k}, {h, i}, {h, j}, {h, k}, {i, j}, {i, k}, {j, k},
  };

  for (int j = 0; j < 10; j++) {
    for (int k = 0; k < 15; k++) {
      best = std::min(kev_eval_5cards(board[j][0], board[j][1], board[j][2],
                                      hole[k][0], hole[k][1]),
                      best);
    }
  }

  return best;
}

TEST(EvaluationTest, TestPlo6Cards) {
  int progress = 0;
  const long long total = 100 * 1000 * 1000;

  std::printf("Start testing Plo6 cards\n");

  for (long long count = 0; count < total; count++) {
    std::vector<int> sample = cs.sample(11);

    int ph_eval = EvaluatePlo6Cards(sample[0], sample[1], sample[2], sample[3],
                                    sample[4], sample[5], sample[6], sample[7],
                                    sample[8], sample[9], sample[10])
                      .value();

    int kev_eval = IterateKevEval(sample[0], sample[1], sample[2], sample[3],
                                  sample[4], sample[5], sample[6], sample[7],
                                  sample[8], sample[9], sample[10]);

    EXPECT_EQ(ph_eval, kev_eval)
        << "Cards are: " << sample[0] << ", " << sample[1] << ", " << sample[2]
        << ", " << sample[3] << ", " << sample[4] << ", " << sample[5] << ", "
        << sample[6] << ", " << sample[7] << ", " << sample[8] << ", "
        << sample[9] << ", " << sample[10];

    if (percentage(count, total) > progress) {
      progress = percentage(count, total);
      if (progress % 10 == 0) {
        std::printf("Test progress: %d%%\n", progress);
      }
    }
  }

  std::printf("Complete testing Plo6 cards\n");
  std::printf("Tested %lld random hands in total\n", total);
}
