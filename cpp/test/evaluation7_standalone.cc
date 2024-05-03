#include <phevaluator/phevaluator.h>

#include <algorithm>
#include <cassert>
#include <cstdio>

#include "kev/kev_eval.h"

using namespace phevaluator;

int percentage(long long numerator, long long denominator) {
  return numerator * 100 / denominator;
}

int main() {
  int count = 0;
  int progress = 0;
  const int total = 133784560;

  std::printf("Start testing seven cards\n");

  for (int a = 0; a < 46; a++) {
    for (int b = a + 1; b < 47; b++) {
      for (int c = b + 1; c < 48; c++) {
        for (int d = c + 1; d < 49; d++) {
          for (int e = d + 1; e < 50; e++) {
            for (int f = e + 1; f < 51; f++) {
              for (int g = f + 1; g < 52; g++) {
                int ph_eval = EvaluateCards(a, b, c, d, e, f, g).value();
                int kev_eval = kev_eval_7cards(a, b, c, d, e, f, g);

                assert(ph_eval == kev_eval);

                count++;

                if (percentage(count, total) > progress) {
                  progress = percentage(count, total);
                  if (progress % 10 == 0) {
                    std::printf("Test progress: %d%%\n", progress);
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  std::printf("Complete testing seven cards.\n");
  std::printf("Tested %d hands in total\n", count);
}
