PokerHandEvaluator
==================

`PokerHandEvaluator <https://github.com/HenryRLee/PokerHandEvaluator>`_ (PH
Evaluator) is an efficient poker hand evaluator based on a perfect hash
algorithm. Instead of traversing all the combinations, it looks up the hand
strength from a pre-computed hash table, which only costs very few CPU cycles
and a considerably small amount of memory (~100kb for the 7-card evaluation).
With slight modifications the same algorithm is also applied to evaluating
Omaha and Pot Limit Omaha hands.

This site is organised into three sections:

* :doc:`algorithm/index` - the description of the underlying perfect-hash
  algorithm.
* :doc:`cpp/index` - usage and examples of the C/C++ library.
* :doc:`python/index` - usage and API reference of the ``phevaluator`` Python
  package.
* :doc:`changelog` - the history of notable changes across releases.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   algorithm/index
   cpp/index
   python/index
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
