#pragma once
#include <array>
#include <vector>

#ifdef __cplusplus
extern "C" {
#endif

namespace card_sampler {
class CardSampler {
  std::array<int, 52> deck;

 public:
  CardSampler(void);
  std::vector<int> sample(int size);
};
}  // namespace card_sampler

#ifdef __cplusplus
}  // closing brace for extern "C"
#endif
