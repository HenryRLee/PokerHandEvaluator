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
  const int total = 20358520;

  std::printf("Start testing six cards\n");

  for (int a = 0; a < 47; a++) {
    for (int b = a + 1; b < 48; b++) {
      for (int c = b + 1; c < 49; c++) {
        for (int d = c + 1; d < 50; d++) {
          for (int e = d + 1; e < 51; e++) {
            for (int f = e + 1; f < 52; f++) {
              int ph_eval =
                  EvaluateCards(a, b, c, d, e, f).value();       // C++ method
              int kev_eval = kev_eval_6cards(a, b, c, d, e, f);  // Kev's method

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

  std::printf("Complete testing six cards.\n");
  std::printf("Tested %d hands in total\n", count);
}
