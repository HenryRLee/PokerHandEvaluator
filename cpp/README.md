# C/C++ Library

## Compile and test

This library can be built using CMake. A recommended way of building it is:

```
mkdir -p build
cd build
cmake ..
make
```

This will generate a dynamic linked library `libpheval.dylib`, as well as
a unit test binary `unit_tests`.

Run the `unit_tests` to perform the unit tests:

```
./unit_tests
```

## Use the library

After building the library `libpheval.dylib`, you can add the `./include`
directory to your includes path, and link the library to your source
code. In addition, at least C++11 standard is required.

For example:

```bash
g++ -I include/ -std=c++11 libpheval.dylib your_source_code.cc your_binary
```

In the [examples](examples) directory, there is a small example on how to
use the library in both C and C++ languages. Run `make` can build the library
and link the library with the example source files.

### C methods

PH Evaluator was originally coded in C, so it still preserves the C functions.

```cpp
int evaluate_5cards(int a, int b, int c, int d, int e);
int evaluate_6cards(int a, int b, int c, int d, int e, int f);
int evaluate_7cards(int a, int b, int c, int d, int e, int f, int g);
```

However using these functions, user needs to convert his card into an integer
ranged `[0, 52)`. You can find the mapping in the section [Card Id](#cardid).

The return value is an integer indicating the rank of the hand, in the range
`[1, 7452]` with the strongest hands (Royal straight flush) returning 1, the
second strongest hands (King high straight flush) returning 2, and the weakest
hands returning 7462.

As a result, a lower return value indicates a stronger hand.

Both the input and output is identical to the Cactus Kev's evaluator.

### C++ methods

In addition to the C methods, more handy C++ methods can be used to get the
same result.

```cpp
int EvaluateCards(Card a, Card b, Card c, Card d, Card e);
int EvaluateCards(Card a, Card b, Card c, Card d, Card e, Card f);
int EvaluateCards(Card a, Card b, Card c, Card d, Card e, Card f, Card g);
```

The Card can be constructed with either a [card id](#cardid), or a string
representation. For example:

```cpp
Card a(3); // 2 in Spades
Card b("AH"); // Ace in Hearts
```

The return value is the same to the C version, which is an integer in the
range `[1, 7452]` indicating the rank of the hand, where a smaller number
is stronger.

## Examples

In this example we use a scenario in the game Texas Holdem:

Community cards: 9c 4c 4s 9d 4h (both players share this cards)

Player 1: Qc 6c

Player 2: 2c 9h

Both players have full houses. But player 1 only has a full house with 4,
while player 2 has a full house with 9, which is stronger.

The expected result is player 2 has a stronger hand than player 1, hence
the return value of the evaluation of player 2 is lower than player 1.

### C++ methods

To evaluate the hands in the above example, we can use the C++ method
`phevaluator::EvaluateCards` and pass the 7 cards as arguments.

```c++
#include "phevaluator/phevaluator.h"
#include <cassert>

int main() {
  int x = phevaluator::EvaluateCards("9c", "4c", "4s", "9d", "4h", "Qc", "6c");
  int y = phevaluator::EvaluateCards("9c", "4c", "4s", "9d", "4h", "2c", "9h");

  assert(x > y);
}
```

### C methods

In the C version, the evaluation would be tricker, since we have to convert
the card to an integer by ourselves.

The formula is `rank * 4 + suit`.

We use 0 for the clubs, 1 for the diamonds, 2 for the hearts, and 3 for the
spades.

And the rank values are:

deuce = 0, trey = 1, four = 2, five = 3, six = 4, seven = 5, eight = 6,
nine = 7, ten = 8, jack = 9, queen = 10, king = 11, ace = 12.

```c
#include "phevaluator/phevaluator.h"
#include <assert>

int main() {
  // Community cards
  int a = 7 * 4 + 0; // 9c
  int b = 2 * 4 + 0; // 4c
  int c = 2 * 4 + 3; // 4s
  int d = 7 * 4 + 1; // 9d
  int e = 2 * 4 + 2; // 4h

  // Player 1
  int f = 10 * 4 + 0; // Qc
  int g = 4 * 4 + 0; // 6c

  // Player 2
  int h = 0 * 4 + 0; // 2c
  int i = 7 * 4 + 2; // 9h

  int x = evaluate_7cards(a, b, c, d, e, f, g);
  int y = evaluate_7cards(a, b, c, d, e, h, i);

  assert(x > y);
}
```

<a name="cardid"></a>
## Card Id

We can use an integer to represent a card. The two least significant bits
represent the 4 suits, ranged from 0-3. The rest of it represent the 13
ranks, ranged from 0-12.

More specifically:
deuce = 0, trey = 1, four = 2, five = 3, six = 4, seven = 5, eight = 6,
nine = 7, ten = 8, jack = 9, queen = 10, king = 11, ace = 12.

So that you can use `rank * 4 + suit` to get the card ID.
 
The complete card Id mapping can be found below. The rows are the ranks
from 2 to Ace, and the columns are the suits: club, diamond, heart and spade.

|   | C | D | H | S |
|---|---|---|---|---|
| 2 | 0 | 1 | 2 | 3 |
| 3 | 4 | 5 | 6 | 7 |
| 4 | 8 | 9 | 10| 11|
| 5 | 12| 13| 14| 15|
| 6 | 16| 17| 18| 19|
| 7 | 20| 21| 22| 23|
| 8 | 24| 25| 26| 27|
| 9 | 28| 29| 30| 31|
| T | 32| 33| 34| 35|
| J | 36| 37| 38| 39|
| Q | 40| 41| 42| 43|
| K | 44| 45| 46| 47|
| A | 48| 49| 50| 51|
