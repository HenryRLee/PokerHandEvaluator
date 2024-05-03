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

#include "hash.h"
extern "C" {
#include "tables.h"
}
namespace phevaluator {

Rank EvaluateCards(const Card& a, const Card& b, const Card& c, const Card& d,
                   const Card& e, const Card& f) {
  return evaluate_6cards(a, b, c, d, e, f);
}

}  // namespace phevaluator
