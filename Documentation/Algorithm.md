# Algorithm

## Table of Contents

- [Chapter 1: A Basic Evaluation Algorithm](#chapter1)
- [Chapter 2: Evaluate the Flushes First](#chapter2)
- [Chapter 3: Hash For a Restricted Quinary](#chapter3)
- [Chapter 4: The Ultimate Dynamic Programming](#chapter4)

<a name="chapter1"></a>

## Chapter 1: A Basic Evaluation Algorithm

The algorithm we are describing here, is suitable for hands with 5 to 9 cards.
We are choosing 7-card stud poker as examples, since the 7-card hand is the
most common and typical scenario.

We know that a deck has 52 different cards, and a 7-card poker hand consists of
7 different cards from a deck. We can easily represent a 7-card poker hand with
a 52-bit binary uniquely, with exactly 7 bits set to 1 and 45 bits set to 0.

For example, if a hand has

```text
 5 of Spades,
 4 of Clubs,
 7 of Spades,
 Jack of Diamonds,
 Ace of Clubs,
 10 of Spades,
 and 5 of Hearts,
```

we can have such a 52-bit binary as a represenation:

```text
 |   Spades   |   Hearts   |  Diamonds  |   Clubs   |
 23456789TJQKA23456789TJQKA23456789TJQKA23456789TJQKA
 0001010010000000100000000000000000010000010000000001
```

We can see that there are totally 52 choose 7 = 133,784,560 combinations of such
representations. If we could map each hand representation to a number range from
[1, 133784560], we can then create a hash table of size 133784560, and assign a
unique value in the hash table for each hand. In other words, we need a perfect
hash function of a 52-bit binary with exactly 7 bits set to 1.

First we sort all these 133784560 binaries in lexicographical order. If we have
a function that receives a binary as an input, and outputs its position in this
lexicographical ordering, this functions is exactly the perfect hash function.

Let's formalize this to a more general problem, and name it HashNBinaryKSum.

```text
 Problem: HashNBinaryKSum

 Input: integer n, integer k, an n-bit binary with exactly k bits set to 1

 Output: the position of the binary in the lexicographical ordering of all n-bit
 binaries with exactly k bits of ones
```

Consider an example with n = 4 and k = 2, the binary 0011 should return 1, and
1010 should return 5.

```text
  0011 0101 0110 1001 1010 1100
```

The problem can be solved in recursions. In order to get the position in the
ordering, we can instead count how many numbers are ahead of that position.

Take 1010 for example, we can count the number of valid numbers in the range
`[0, 1010)`. As for counting the numbers in range `[0, 1010)`, we can first
count the numbers in `[0, 1000)`, then count `[1000, 1010)`. To solve the
former case `[0, 1000)`, we can use 3 choose 2, which is the number of
combinations of filling 2 ones in the last 3 bits. The latter case
`[1000, 1010)` is equivalent to `[000, 010)`, with both the parameter n
and k decrement by 1, so it becomes a smaller problem and can be solved
in another recursion.

We can optimize the recursion to a loop, and the sample C code is shown below.

```c
int hash_binary(unsigned char q[], int len, int k)
{
  int sum = 0;
  int i;

  for (i=0; i<len; i++)
  {
    if (q[i])
    {
      if (len-i-1 >= k)
        sum += choose[len-i-1][k];

      k--;

      if (k == 0)
        break;
    }
  }

  return ++sum;
}
```

In practice, we don't need the final increment at the end, by treating the
position as a number starting from 0, which also fits perfectly in a hash table.

We can precompute all possible n choose k and store the results. For a problem
with a n-bit binary, the function runs in at most n cycles.

If we apply this function to a poker hand, it'll take 52 cycles to compute the
hash value. Meanwhile we need a hash table of size 133784560 entries in the
7-card poker hand case. Both the time and memory performance are not what we
expected.

Proceed to chapter 2, you will find out how a more advanced algorithm can solve
the problem.

<a name="chapter2"></a>

## Chapter 2: Evaluate the Flushes First

What makes a poker evaluator complicated, is the Flush category (including the
Straight Flush). If we don't care about the Flush, we can ignore the suits, and
simplify the 52-bit binary to a 13-bit quinary (base 5 number). The reason we
need base 5, is that for each rank, there can be 0, 1, 2, 3, 4 numbers of cards,
hence 5 possibilities.

So we can split the problem into two branches, the hands with a flush and the
hands without a flush. The first one can be represented by a 13-bit binary,
and the latter one can be represented by a 13-bit quinary.

In 7-card poker, if there are at least five cards in the same suit, this hand
is guaranteed to be either Flush or Straight Flush. Because if we have at
least 5 cards in the same suit, these cards must have different ranks, and then
combining 2 more cards from the other suit cannot form a Four of a Kind or a
Full House. We also know that, there cannot be two flushes in different suits
in a 7-card hand.

Therefore, we can first evaluate whether the hand is a flush or not. Once we
find a flush in a 7-card hand, we can stop evaluating the rest of the cards.
However, if the hand has more than 7 cards, we need to keep evaluating the
other branch.

It's not hard to determine whether a hand has a flush or not, we only need a
counter for each suit. In the meantime, we need to maintain a binary for each
suit, so that when we see a flush, we can pass the corresponding binary to the
function that evaluates flush hands.

For example, given the input:

```text
 5 of Spades,
 4 of Spades,
 7 of Spades,
 Jack of Diamonds,
 Ace of Clubs,
 10 of Spades,
 8 of Spades,
```

our 4 counters and binaries are:

```text
 Spades:     counter 5, binary 0000101101100
 Hearts:     counter 0, binary 0000000000000
 Clubs:      counter 1, binary 1000000000000
 Diamonds:   counter 1, binary 0001000000000
```

As soon as we see the counter of Spades is greater than 4, we can pass the
binary 0000101101100 to the next function to evaluate the flush. We don't need
to worry about the other cards in other suits, because none of those cards can
form another flush.

We can of course use the HashNBinaryKSum function and three hash table (k can be
5, 6 and 7) to evaluate the flush binary. However, considering the number
2^13 = 8192 is not very large, we can directly look up a table of size 8192,
that saves us a loop of 13 cycles to compute the perfect hash.

If the hand contains no more than 7 cards, we can now immediately return the
value of the flush as a final result. Otherwise, we still need to go through the
non-flush branch, and compare both results.

We will discuss how to evaluate the quinary in the next chapter.

<a name="chapter3"></a>

## Chapter 3: Hash For a Restricted Quinary

Recall that for a hand that suits no longer matters, we can represent a 7-card
hand with a 13-bit quinary (base 5) number. Again, there is a restriction of
such a quinary, which is the sum of all bits is equal to 7.

To encode the quinary, we need 13 counters. When a new card comes in, increment
the counter of the corresponding rank. For example, if a hand has 2 Aces, 3
Fives, 1 Seven and 1 Jack, the quinary is 2001000103000.

Let's try to find a perfect hash function for such a quinary. Same as what we
did in the binary hash, if we sort all the quinary in lexicographical order,
where the sum of all bits of each quinary is equal to 7, the position in this
ordering is a perfect hash of this quinary.

```text
 Problem: HashNQuinaryKSum

 Input: integer n, integer k, an (n+1)-bit quinary with the sum of all bits
  equal to k

 Output: the position of the quinary in the lexicographical ordering of all
  (n+1)-bit quinaries with sum of all bits equal to k
```

Similar to what we did in the binary hash, in order to get the position of the
quinary, we can count how many valid numbers are smaller than this quinary. For
example, given a 4-bit quinary 4300, we can first count the valid numbers in
range `[0000, 4300)`, then increment the result in the end. The range
`[0000, 4300)` can be splitted into `[0000, 4000)` and `[4000, 4300)`. The
latter range is equivalent to `[000, 300)` with parameter n-1 and k-4, and
becomes a problem of a smaller size.

Unlike the binary hash, the range `[0000, 4000)`is not easy to compute. We
can keep splitting the range into `[0000, 1000)`, `[1000, 2000)`, `[2000, 3000)`
and `[3000, 4000)`. The range `[1000, 2000)` is equivalent to `[000, 1000)`
with k-1, and the range `[2000, 3000)` is equivalent to `[000, 1000)` with k-2,
and so on.

Now the remaining problem is solving the range `[0000, 1000)` with parameter k.
This range can be splitted into `[000, 400)` and `[400, 1000)`, and eventually
it can be partitioned into 5 small ranges. The result of the problem is the
sum of the result of the 5 subproblems with range of exactly a power of 5.

We can use dynamic programming to solve all these subproblems, and store the
result in an array. Let's use a 3-d array `dp[l][n][k]` of size `5*14*8`,
where n is the number of trailing zero bits, k is the remaining number of k, and
l is the most significant bit of the excluding endpoint. For
example, the result of `[0000, 1000)` is stored in `dp[1][3][k]`, as the
excluding endpoint is 1000, resulting l to be 1 and n to be 3. Another
example is `[000, 200)`, whose result is stored in `dp[2][2][k]`.

The base cases for the array dp:

```pseudocode
  if 0 <= i <= 4:
    dp[1][1][i] = 1;
  if i > 4:
    dp[1][1][i] = 0;
```

For example, for `[00, 10)` with `k=4` there's only one legal quinary (04)
However there is no instance for a quinary in the same range with `k=5` or any
`k` larger than 4.

Then we iterate the edges:

```pseudocode
  for each i in [2, 13]:
    dp[1][i][1] = i;
    dp[1][i][0] = 1;
```

For example, a 4-bit quinary with k=1 (`dp[1][3][1]`) has three quinaries: 001,
010, 100.
If `k=0`, the only legal quinary 000.

Now we can iterate all `dp[1][i][j]`. We do this by iterating the next digit
from 0 to 4 and evaluating the shorter expression for smaller `k`. :

```pseudocode
  for each i in [2, 13] and j in [2, 7]:
    dp[1][i][j] = SUM{k:[0,4]}dp[1][i-1][j-k];
```

For example, to evaluate `dp[1][2][7]` (range `[000,100)` with `k=7`), we need to
enumerate the second bit from 0 to 4. This means summing for 07, 16, 25, 34, 43.
Notice that 07, 16, 25 are invalid and `dp[1][1][k] = 0 (for k > 4)` will ignore
them.

Now the iteration for the rest of the entries:

```pseudocode
  for each l in [2, 4] and i in [1, 13] and j in [0, 7]:
    dp[l][i][j] = dp[l-1][i][j] + dp[1][i][j-l+1]
```

For example `dp[4][4][5]`, which is equivalent to the number of valid
quinaries in the range `[00000, 40000)` with k=5. It can be splitted into
`[00000, 30000)` with k=5, and `[30000, 40000)`. The former one is `dp[3][4][5]`,
the latter one is equivalent to `[00000, 10000)` with k=k-3, which is
`dp[1][4][2]`.

Finally we can compute the hash of the quinary base on the dp arrays. The
example C code is shown below.

```c
int hash_quinary(unsigned char q[], int len, int k)
{
  int sum = 0;
  int i;

  for (i=0; i<len; i++) {
    sum += dp[q[i]][len-i-1][k];

    k -= q[i];

    if (k <= 0)
      break;
  }

  return ++sum;
}
```

In practice, the final increment can be ignored.

The final lookup hash table will contain 49205 entries, and the hash function
takes at most 13 cycles to compute. This algorithm is much better than any
others that do 7-card poker evaluation by checking all 21 combinations.

<a name="chapter4"></a>

## Chapter 4: The Ultimate Dynamic Programming Algorithm

Recall that in chapter one, we managed to find a mapping from a 52-bit
restricted binary to a hash key ranged from 0 to 133784559. Although the number
of entries in this hash table is considerably large, it's still feasible on
modern computers. If we could manage to improve the time efficiency in the hash
function, it's still a useful approach.

Let's go back to that problem HashNBinaryKSum:

```text
 Problem: HashNBinaryKSum

 Input: integer n, integer k, an n-bit binary with exactly k bits set to 1

 Output: the position of the binary in the lexicographical ordering of all n-bit
 binaries with exactly k bits of ones
```

More specificly, we are trying to solve a problem with n = 52 and k = 7. If we
split the 52-bit binary into 4 blocks, where each block has 13 bits, we can
precompute the results in a table in size 2^13 \* 4 \* 8, and do only 4 summations
in the actual hash function. In practice, it would be easier if we use a 16-bit
block instead of 13, making the table in size 2^16 \* 4 \* 8.

Precomputing this table is similar to the methods we used in the previous
chapters. I'll just put the sample C code here and omit the explanations.

```c
{
  int dp[65536][4][8];

  for (i=0; i<65536; i++) {
    for (j=0; j<4; j++) {
      for (k=0; k<8; k++) {
        int ck = k;
        int s;
        int sum = 0;

        for (s=15; s>=0; s--) {
          if (i & (1 << s)) {
            int n = j*16 + s;

            sum += choose[n][ck];

            ck--;
          }
        }

        dp[i][j][k] = sum;
      }
    }
  }
}
```

And the hash function only need to sum up the result from the dp table. The C
code is shown below.

```c
int fast_hash(unsigned long long handid, int k)
{
  int hash = 0;

  unsigned short * a = (unsigned short *)&handid;

  hash += dp_fast[a[3]][3][k];
  k -= bitcount[a[3]];

  hash += dp_fast[a[2]][2][k];
  k -= bitcount[a[2]];

  hash += dp_fast[a[1]][1][k];
  k -= bitcount[a[1]];

  hash += dp_fast[a[0]][0][k];

  return hash;
}
```

Although this algorithm takes very few CPU cycles to compute the hash value (4
summations and 3 decrements), the overall performance is worse than what we used
in the previous chapter. Part of the reason might be the dp table is greater
than a normal page size (64Kbytes). If we cut the block into 8 bits and use a
table of size 2^8 \* 8 \* 8, which will double the number of operations in the
hash function (8 summations and 7 decrements), the performance seems to improve,
but still doesn't beat the algorithm used in the previous chapter under my
environment.

In summary, although it's an algorithm that uses very few CPU cycles, the true
performance is bounded by the time access to the memory, which doesn't make it
significantly faster than the algorithm we used in chapter 2 to chapter 3.
