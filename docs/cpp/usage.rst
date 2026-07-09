Using the libraries
===================

After running ``make``, the following library files are generated:

.. code-block:: text

   libpheval.a      # library pheval
   libpheval5.a     # library pheval5
   libpheval6.a     # library pheval6
   libpheval7.a     # library pheval7
   libphevalplo4.a  # library phevalplo4
   libphevalplo5.a  # library phevalplo5
   libphevalplo6.a  # library phevalplo6

pheval
------

The corresponding library file is ``libpheval.a``.

This library includes the 5-card, 6-card, and 7-card evaluators. It also
includes all the methods of describing a rank. However, the additional memory
usage of these rank-describing methods is significantly high (356k), due to the
rank description table declared in ``src/7462.c``.

The example usage of this library can be found in ``examples/c_example.c`` and
``examples/cpp_example.cc`` (see :doc:`examples`).

pheval5, pheval6, and pheval7
-----------------------------

The corresponding library files are ``libpheval5.a``, ``libpheval6.a``, and
``libpheval7.a``.

These libraries are memory-optimized for evaluating 5-card hands, 6-card hands,
and 7-card hands respectively. They don't include the rank-describing methods,
in order to save memory usage.

The example usage of these libraries can be found in
``examples/evaluator5_standalone_example.cc``,
``examples/evaluator6_standalone_example.cc``, and
``examples/evaluator7_standalone_example.cc``.

phevalplo4, phevalplo5, and phevalplo6
--------------------------------------

The corresponding library files are ``libphevalplo4.a``, ``libphevalplo5.a``,
and ``libphevalplo6.a``.

These libraries evaluate Pot Limit Omaha 4 (standard Omaha) hands, Pot Limit
Omaha 5 hands, and Pot Limit Omaha 6 hands respectively. They also include all
the methods of describing a rank; the additional memory usage is insignificant
compared to the memory usage of the basic Omaha evaluators.

The example usage of these libraries can be found in ``examples/plo4_example.cc``,
``examples/plo5_example.cc``, and ``examples/plo6_example.cc``.

Linking the library
-------------------

After building the libraries, add the ``./include`` directory to your includes
path, and link the library to your source code. At least the C++11 standard is
required for compiling. For example:

.. code-block:: sh

   g++ -I include/ -std=c++11 your_source_code.cc libpheval.a -o your_binary
