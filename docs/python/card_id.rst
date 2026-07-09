Card Id
=======================================

We can use an integer to represent a card. The two least significant bits
represent the 4 suits, ranging from 0-3. The rest of it represents the 13
ranks, ranging from 0-12.

More specifically, the ranks are:

deuce = 0, trey = 1, four = 2, five = 3, six = 4, seven = 5, eight = 6,
nine = 7, ten = 8, jack = 9, queen = 10, king = 11, ace = 12.

And the suits are:
club = 0, diamond = 1, heart = 2, spade = 3

So that you can use ``rank * 4 + suit`` to get the card ID.

Technically, it is fine to swap the suit values, as long as the suits are
uniquely mapped to the values 0, 1, 2, and 3. If you do swap the suit values,
make sure to update the mapping in the source code as well (``suit_map`` in
``phevaluator/card.py``).

The complete card Id mapping can be found below. The rows are the ranks from 2
to Ace, and the columns are the suits: club, diamond, heart and spade.

===  ===  ===  ===  ===
\      C    D    H    S
===  ===  ===  ===  ===
2      0    1    2    3
3      4    5    6    7
4      8    9   10   11
5     12   13   14   15
6     16   17   18   19
7     20   21   22   23
8     24   25   26   27
9     28   29   30   31
T     32   33   34   35
J     36   37   38   39
Q     40   41   42   43
K     44   45   46   47
A     48   49   50   51
===  ===  ===  ===  ===
