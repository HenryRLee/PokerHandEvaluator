Building and testing
====================

The following instructions assume you are in the
`cpp <https://github.com/HenryRLee/PokerHandEvaluator/tree/master/cpp>`_
directory. If you are in the repository root, change into it first:

.. code-block:: sh

   cd cpp

Build with CMake
----------------

The library can be built using CMake. A recommended way of building it is:

.. code-block:: sh

   cmake -B build      # create a folder named build and configure the Makefile
   cmake --build build # start the build in the new folder

This generates a static-linked library ``libpheval.a`` in the new folder, as
well as a unit test binary ``unit_tests``.

Run ``unit_tests`` to perform the unit tests:

.. code-block:: sh

   cd build/
   ./unit_tests

Another option is to build the library only, skipping the unit test binary.
Build with the target ``pheval`` to build just the static-linked library:

.. code-block:: sh

   cmake -B build
   cmake --build build/ --target pheval

The CMake command generates a Makefile in the new folder, so if you prefer GNU
Make you can still use it. For example:

.. code-block:: sh

   cmake -B build
   cd build
   make pheval

Build on Windows
----------------

The unit tests depend on the Google Test suite, which isn't available on
Windows. This option lets you build the libraries and examples without it:

.. code-block:: sh

   cmake -B build -DBUILD_TESTS=OFF

After successfully running the ``cmake`` command, each build target generates a
``.vcxproj`` file, which is a project file that can be imported into Visual
Studio.

Build with GNU Make
-------------------

The ``cpp`` directory also includes a Makefile for users that want to use
native GNU Make to compile the library.

Simply run ``make`` to build the static-linked library ``libpheval.a``.

In the ``examples`` directory there is another Makefile to compile the examples
with the library linked:

.. code-block:: sh

   cd examples
   make

Disabling PLO variants
----------------------

Building the PLO6 library costs a significant amount of memory. If you don't
want to build this feature, you may disable PLO6 using a CMake config:

.. code-block:: sh

   cmake -DBUILD_PLO6=OFF .. ; make

Similarly, you can turn off PLO4 and PLO5.
