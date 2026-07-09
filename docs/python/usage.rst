Usage
=====

Evaluating a hand
-----------------

The main function is :func:`phevaluator.evaluate_cards`.

.. code-block:: python

   from phevaluator import evaluate_cards

   p1 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "Qc", "6c")
   p2 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "2c", "9h")

   # The rank is an integer from 1 (strongest) to 7462 (weakest), so a
   # smaller value means a stronger hand. Player 2 has a stronger hand here.
   print(f"The rank of the hand in player 1 is {p1}")  # 292
   print(f"The rank of the hand in player 2 is {p2}")  # 236

The returned value is the rank of the hand among all 7462 distinct five-card
hands. It is identical to the return value of Cactus Kev's evaluator: ``1`` is
the best possible hand (a Royal Straight Flush) and ``7462`` is the worst. A
smaller value is always a stronger hand, so you can compare two hands directly
(e.g. ``p2 < p1`` means player 2 wins).

The function accepts both integer card ids and card strings (with a format like
``"Ah"`` or ``"2C"``). The number of cards must be between 5 and 7.

Omaha and Pot Limit Omaha
-------------------------

Omaha-style hands (five community cards followed by the hole cards) can be
evaluated with the dedicated functions:

.. code-block:: python

   from phevaluator import evaluate_omaha_cards  # 4 hole cards
   from phevaluator import evaluate_plo4_cards   # 4 hole cards (alias of Omaha)
   from phevaluator import evaluate_plo5_cards   # 5 hole cards
   from phevaluator import evaluate_plo6_cards   # 6 hole cards

   # 5 community cards + 4 hole cards. The return value is a rank in the same
   # 1 (strongest) to 7462 (weakest) scale as evaluate_cards, computed from the
   # best five-card hand allowed by the Omaha rules.
   evaluate_omaha_cards("4c", "5c", "6c", "7s", "8s", "2c", "9c", "As", "Kd")

See :doc:`installation` for how to enable the opt-in PLO5/PLO6 evaluators.
