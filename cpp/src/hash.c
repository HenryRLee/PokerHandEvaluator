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

#include "hash.h"

#include <stdio.h>

#include "tables.h"

int hash_quinary(const unsigned char q[], int k) {
  int sum = 0;
  const int len = 13;
  int i;

  for (i = 0; i < len; i++) {
    sum += dp[q[i]][len - i - 1][k];

    k -= q[i];

    if (k <= 0) {
      break;
    }
  }

  return sum;
}
