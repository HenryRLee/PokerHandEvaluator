/*
 *  Copyright 2016-2023 Henry Lee
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

#include <phevaluator/phevaluator.h>

namespace phevaluator {

Rank EvaluatePlo6Cards(const Card& c1, const Card& c2, const Card& c3,
                       const Card& c4, const Card& c5, const Card& h1,
                       const Card& h2, const Card& h3, const Card& h4,
                       const Card& h5, const Card& h6) {
  return evaluate_plo6_cards(c1, c2, c3, c4, c5, h1, h2, h3, h4, h5, h6);
}

}  // namespace phevaluator
