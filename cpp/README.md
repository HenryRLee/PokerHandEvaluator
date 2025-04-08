# C/C++ Library

## Build and test

The following intructions assumes you are in the [cpp](/cpp/) directory. If
you are in the root directory, please change to [cpp](/cpp/) first.

```sh
cd cpp
```

### Build with CMake

This library can be built using CMake. A recommended way of building it is:

```sh
mkdir -p build
cd build
cmake ..
make
```

This will generate a static-linked library `libpheval.a`, as well as
a unit test binary `unit_tests`.

Run `unit_tests` to perform the unit tests:

```sh
./unit_tests
```

Another build option is to build the library only, after generating the CMake files,
run `make pheval` to build the static-linked library.

```sh
mkdir -p build
cd build
cmake ..
make pheval
```

### Build in Windows

The unit tests depends on Google Test suite, which isn't available in Windows.
This way allows us to build the libraries and examples.

```sh
mkdir -p build
cd build
cmake -DBUILD_TESTS=OFF ..
```

After successfully running the `cmake` command, each build target will generate a
`.vcxproj` file, which is a project file that can be imported to Visual Studio.

### Build with GNU Make

This [cpp](/cpp/) directory also includes a Makefile, for users that want to use
native GNU Make to compile the library.

Simply run `make` to build the static-linked library `libpheval.a`.

In the [examples](/cpp/examples), there is another Makefile to compile the examples
with the library linked.

```sh
cd examples
make
```

## Using the libraries

After running `make`, you can see the following library files generated:

```text
libpheval.a      # library pheval
libpheval5.a     # library pheval5
libpheval6.a     # library pheval6
libpheval7.a     # library pheval7
libphevalplo4.a  # library phevalplo4
libphevalplo5.a  # library phevalplo5
libphevalplo6.a  # library phevalplo6
```

### pheval

The corresponding library file is `libpheval.a`.

This library includes 5-card, 6-card, and 7-card evaluators.

It also includes all the methods of describing a rank. However, the additional
memory usage of these rank describing methods is significantly high (356k), due
to the rank description table declared in `src/7462.c`.

The example usage of this library can be found in `examples/c_example.c` and
`examples/cpp_example.cc`.

### pheval5, pheval6, and pheval7

The corresponding library files are `libpheval5.a`, `libpheval6.a`, and
`libpheval7.a`.

These libraries are memory optimized for evaluating 5-card hands, 6-card hands,
and 7-card hands respectively.

These libraries don't include the rank describing methods, in order to save the
memory usage.

The example usage of these libraries can be found in
`examples/evaluator5_standalone_example.cc`,
`examples/evaluator6_standalone_example.cc` and
`examples/evaluator7_standalone_example.cc`.

### phevalplo4, phevalplo5, and phevalplo6

The corresponding library files are `libphevalplo4.a`, `libphevalplo5.a`, and
`libphevalplo6.a`.

These libraries are made for evaluator Pot Limit Omaha 4 (standard Omaha) hands,
Pot Limit Omaha 5 hands, and Pot Limit Omaha 6 hands respectively.

These libraries also include all the methods of describing a rank. The additional
memory usage of these rank describing methods is insignificant compared to the
memory usage of the basic omaha evaluators.

The example usage of these libraries can be found in `examples/plo4_example.cc`,
`examples/plo5_example.cc` and `examples/plo6_example.cc`.

Building the PLO6 library costs significant amount of memory. If you don't want
to build this feature, you may disable PLO6 using a CMake config.

```bash
cmake -DBUILD_PLO6=OFF .. ; make
```

Similarly, you can turn off PLO4 and PLO5.

### Linking the library

After building the libraries, you can add the `./include`
directory to your includes path, and link the library to your source
code. In addition, at least C++11 standard is required for compiling.

For example:

```bash
g++ -I include/ -std=c++11 your_source_code.cc libpheval.a -o your_binary
```

## Examples

In this example we use a scenario in the game Texas Holdem:

Community cards: 9c 4c 4s 9d 4h (both players share these cards)

Player 1: Qc 6c

Player 2: 2c 9h

Both players have full houses. But player 1 only has a four full house over
nine, while player 2 has nine full house over four, which is stronger than
player 1.

The following two sections will show us how this example hands are evaluated
using PHEvaluator. All the code and compiling can be found in the
[examples](examples) directory.

### Example Code in C++

We can construct a Card by providing a two character string, like this:

```C++
phevaluator::Card a = phevaluator::Card("Qc");
```

Then the method `EvaluateCards` will take parameters from 5 to 7 Cards and
return a Rank type. Sometimes, you can provide the strings directly to the
method and let the Cards be constructed implicitly, to make your code
cleaner.

```C++
phevaluator::Rank rank1 =
  phevaluator::EvaluateCards("9c", "4c", "4s", "9d", "4h", "Qc", "6c");

phevaluator::Rank rank2 =
  phevaluator::EvaluateCards("9c", "4c", "4s", "9d", "4h", "2c", "9c");
```

Now that we have the Ranks from both players' hands. What information can
we get from them?

First, we can do comparison on these Ranks. A stronger hand is greater than
a weaker hand.

```C++
assert(rank1 < rank2); // rank2 is stronger
```

We can also get its rank in all 7562 possible hands. This ranking is
identical to the return value of the Cactus Kev's evaluator:
the best rank has value 1, which is a Royal Straight Flush, while the
worst rank is 7462.

```C++
int value1 = rank1.value(); // 292
int value2 = rank2.value(); // 236
```

We can also tell the ranking category of the rank: either using the method
`category` which returns an enumerator, or the method `describeCategory`
which returns a string. In this example, both players are holding full houses.

```C++
assert(rank1.category() == FULL_HOUSE);
assert(rank1.describeCategory() == "Full House");

assert(rank2.category() == FULL_HOUSE);
assert(rank2.describeCategory() == "Full House");
```

Apart from the ranking category, we can get more detail from the rank, using
the `describeRank` or the `describeSampleHand` method.

Let's see a sample hand from the `rank2`:

```C++
assert(rank2.describeSampleHand() == "99944");
```

As we can see, the best 5-card hand from player 2 is 9-9-9-4-4. Suit
information is missing from this method, because usually they don't matter,
unless all the five cards have the same suit. So we have another method that
tells us whether the sample hand is a flush. In this example, it is not.

```C++
assert(!rank2.isFlush());
```

Finally, we have another method to give us a short description of the sample
hand:

```C++
assert(rank2.describeRank() == "Nines Full over Fours");
```

### Example Code in C

In the C version, the evaluation would be tricker, since we have to convert
the card to an integer by ourselves.

The formula is `rank * 4 + suit`.

We use 0 for the clubs, 1 for the diamonds, 2 for the hearts, and 3 for the
spades.

And the rank values are:
deuce = 0, trey = 1, four = 2, five = 3, six = 4, seven = 5, eight = 6,
nine = 7, ten = 8, jack = 9, queen = 10, king = 11, ace = 12.

And the suits are:
club = 0, diamond = 1, heart = 2, spade = 3

The mapping of a Card and its integer value can be found in [Card Id](#cardid).

```C
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
```

After constructing all the Cards, we will use `evaluate_7cards` to get a
rank value. A rank value indicates its rank in the 7462 ranking table. The
best rank is 1, which is a Royal Straight Flush, and the worst rank is 7462.

```C
int rank1 = evaluate_7cards(a, b, c, d, e, f, g); // 292
int rank2 = evaluate_7cards(a, b, c, d, e, h, i); // 236
```

If we compare these two rank value, the rank with a smaller value is
stronger.

```C
assert(rank1 > rank2); // rank2 is stronger
```

Similar to the C++ interfaces, we can see the rank category:

```C
enum rank_category category = get_rank_category(rank1);
assert(category == FULL_HOUSE);

const char * categoryDesc = describe_rank_category(category); // "Full House"
```

Or get the sample hand from the rank:

```C
describe_sample_hand(rank2); // 9 9 9 4 4
```

We can see the 5 best cards from player 2 are 9 9 9 4 4.

Although suit information is missing here, indeed we only care about whether
all five cards are in the same suit or not. We can check it using the
`is_flush` method:

```C
is_flush(rank2); // false
```

Finally, we can use `rank_description` to get a short description of the rank:

```C
describe_rank(rank2); // Nines Full over Fours
```

<a name="cardid"></a>

## Card Id

We can use an integer to represent a card. The two least significant bits
represent the 4 suits, ranged from 0-3. The rest of it represent the 13
ranks, ranged from 0-12.

More specifically, the ranks are:

deuce = 0, trey = 1, four = 2, five = 3, six = 4, seven = 5, eight = 6,
nine = 7, ten = 8, jack = 9, queen = 10, king = 11, ace = 12.

And the suits are:
club = 0, diamond = 1, heart = 2, spade = 3

So that you can use `rank * 4 + suit` to get the card ID.

The complete card Id mapping can be found below. The rows are the ranks
from 2 to Ace, and the columns are the suits: club, diamond, heart and spade.

|      |    C |    D |    H |    S |
| ---: | ---: | ---: | ---: | ---: |
|    2 |    0 |    1 |    2 |    3 |
|    3 |    4 |    5 |    6 |    7 |
|    4 |    8 |    9 |   10 |   11 |
|    5 |   12 |   13 |   14 |   15 |
|    6 |   16 |   17 |   18 |   19 |
|    7 |   20 |   21 |   22 |   23 |
|    8 |   24 |   25 |   26 |   27 |
|    9 |   28 |   29 |   30 |   31 |
|    T |   32 |   33 |   34 |   35 |
|    J |   36 |   37 |   38 |   39 |
|    Q |   40 |   41 |   42 |   43 |
|    K |   44 |   45 |   46 |   47 |
|    A |   48 |   49 |   50 |   51 |
