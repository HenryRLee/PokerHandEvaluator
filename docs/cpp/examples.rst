Examples
========

In this example we use a scenario from the game Texas Hold'em:

Community cards: ``9c 4c 4s 9d 4h`` (both players share these cards)

* Player 1: ``Qc 6c``
* Player 2: ``2c 9h``

Both players have full houses. Player 1 only has fours full over nines, while
player 2 has nines full over fours, which is stronger than player 1.

All the code and compiling instructions can be found in the
`examples <https://github.com/HenryRLee/PokerHandEvaluator/tree/master/cpp/examples>`_
directory.

Example code in C++
-------------------

We can construct a ``Card`` by providing a two-character string:

.. code-block:: cpp

   phevaluator::Card a = phevaluator::Card("Qc");

The method ``EvaluateCards`` takes 5 to 7 ``Card`` parameters and returns a
``Rank``. You can also provide the strings directly and let the ``Card`` values
be constructed implicitly, to make your code cleaner:

.. code-block:: cpp

   phevaluator::Rank rank1 =
     phevaluator::EvaluateCards("9c", "4c", "4s", "9d", "4h", "Qc", "6c");

   phevaluator::Rank rank2 =
     phevaluator::EvaluateCards("9c", "4c", "4s", "9d", "4h", "2c", "9h");

A stronger hand compares as less than a weaker hand:

.. code-block:: cpp

   assert(rank1 > rank2); // rank2 is stronger

We can get the rank value among all 7462 possible hands. This ranking is
identical to the return value of Cactus Kev's evaluator: the best rank has
value 1 (a Royal Straight Flush), while the worst rank is 7462.

.. code-block:: cpp

   int value1 = rank1.value(); // 292
   int value2 = rank2.value(); // 236

We can tell the ranking category of the rank, either using the method
``category`` (which returns an enumerator) or ``describeCategory`` (which
returns a string). In this example both players hold full houses:

.. code-block:: cpp

   assert(rank1.category() == FULL_HOUSE);
   assert(rank1.describeCategory() == "Full House");

   assert(rank2.category() == FULL_HOUSE);
   assert(rank2.describeCategory() == "Full House");

We can get more detail from the rank using ``describeRank`` or
``describeSampleHand``. The best 5-card hand from player 2 is 9-9-9-4-4:

.. code-block:: cpp

   assert(rank2.describeSampleHand() == "99944");

Suit information is missing from that method because it usually doesn't matter,
unless all five cards share the same suit. The ``isFlush`` method tells us
whether the sample hand is a flush. In this example it is not:

.. code-block:: cpp

   assert(!rank2.isFlush());

Finally, ``describeRank`` gives a short description of the sample hand:

.. code-block:: cpp

   assert(rank2.describeRank() == "Nines Full over Fours");

Example code in C
-----------------

In the C version the evaluation is trickier, since we have to convert each card
to an integer ourselves. The formula is ``rank * 4 + suit``. See :doc:`card_id`
for the full mapping.

.. code-block:: c

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

After constructing all the cards, use ``evaluate_7cards`` to get a rank value.
The best rank is 1 (a Royal Straight Flush) and the worst is 7462:

.. code-block:: c

   int rank1 = evaluate_7cards(a, b, c, d, e, f, g); // 292
   int rank2 = evaluate_7cards(a, b, c, d, e, h, i); // 236

When comparing two rank values, the smaller one is stronger:

.. code-block:: c

   assert(rank1 > rank2); // rank2 is stronger

Similar to the C++ interface, we can get the rank category:

.. code-block:: c

   enum rank_category category = get_rank_category(rank1);
   assert(category == FULL_HOUSE);

   const char *categoryDesc = describe_rank_category(category); // "Full House"

Or get the sample hand from the rank:

.. code-block:: c

   describe_sample_hand(rank2); // 9 9 9 4 4

Although suit information is missing here, we only care about whether all five
cards are the same suit. Check it using ``is_flush``:

.. code-block:: c

   is_flush(rank2); // false

Finally, ``describe_rank`` gives a short description of the rank:

.. code-block:: c

   describe_rank(rank2); // Nines Full over Fours
