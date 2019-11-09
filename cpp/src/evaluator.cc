/*
 *  Copyright 2016-2019 Henry Lee
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

#include "phevaluator/phevaluator.h"

namespace phevaluator {

int EvaluateCards(Card a, Card b, Card c, Card d, Card e) {
  return evaluate_5cards(a, b, c, d, e);
}

int EvaluateCards(Card a, Card b, Card c, Card d, Card e, Card f) {
  return evaluate_6cards(a, b, c, d, e, f);
}

int EvaluateCards(Card a, Card b, Card c, Card d, Card e, Card f, Card g) {
  return evaluate_7cards(a, b, c, d, e, f, g);
}

int EvaluateCards(Card a, Card b, Card c, Card d, Card e, Card f, Card g, Card h) {
  return evaluate_8cards(a, b, c, d, e, f, g, h);
}

int EvaluateCards(Card a, Card b, Card c, Card d, Card e, Card f, Card g, Card h, Card i) {
  return evaluate_9cards(a, b, c, d, e, f, g, h, i);
}

} // namespace phevaluator

