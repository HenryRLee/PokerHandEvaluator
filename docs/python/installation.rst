Installation
============

The library requires Python 3.10 or newer.

The evaluator is implemented as a C extension (``phevaluator._pheval``) that
wraps the C sources in the repository's
`cpp <https://github.com/HenryRLee/PokerHandEvaluator/tree/master/cpp>`_
directory, so a C compiler and **pip 21.3 or newer** are required to build from
source.

From PyPI
---------

.. code-block:: shell

   pip install phevaluator

From source
-----------

Build from within the repository (the sibling ``cpp`` directory is used to
compile the extension):

.. code-block:: shell

   pip install .

Optional Pot Limit Omaha support
---------------------------------

``evaluate_plo5_cards`` and ``evaluate_plo6_cards`` require the package to be
built with PLO5/PLO6 support. Their lookup tables are very large (hundreds of MB
of generated C source each), so they are **opt-in**: set the
``PHEVALUATOR_BUILD_PLO`` environment variable when installing from the
repository.

.. code-block:: shell

   # Build with PLO5 and PLO6 support (also accepts "5", "6", or "all")
   PHEVALUATOR_BUILD_PLO=5,6 pip install .

Calling ``evaluate_plo5_cards`` / ``evaluate_plo6_cards`` on a package built
without the corresponding support raises :class:`NotImplementedError`.
``evaluate_plo4_cards`` (and ``evaluate_omaha_cards``) are always available.
