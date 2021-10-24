"""Module for card."""
from __future__ import annotations

from typing import Any, Union

# fmt: off
rank_map = {
    "2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7,
    "T": 8, "J": 9, "Q": 10, "K": 11, "A": 12,
}
suit_map = {
    "C": 0, "D": 1, "H": 2, "S": 3,
    "c": 0, "d": 1, "h": 2, "s": 3
}
# fmt: on

rank_reverse_map = {value: key for key, value in rank_map.items()}
suit_reverse_map = {value: key for key, value in suit_map.items() if key.islower()}


class Card:
    """An immutable card object.

    Attributes:
        __id (int): The integer that identifies the card.
            We can use an integer to represent a card. The two least significant bits
            represent the 4 suits, ranged from 0-3. The rest of it represent the 13
            ranks, ranged from 0-12.

            More specifically, the ranks are:

            deuce = 0, trey = 1, four = 2, five = 3, six = 4, seven = 5, eight = 6,
            nine = 7, ten = 8, jack = 9, queen = 10, king = 11, ace = 12.

            And the suits are:
            club = 0, diamond = 1, heart = 2, spade = 3

            So that you can use `rank * 4 + suit` to get the card ID.

            The complete card Id mapping can be found below. The rows are the ranks from
            2 to Ace, and the columns are the suits: club, diamond, heart and spade.

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

        __slots__ (list[str]): Explicitly declare data members

    Raises:
        ValueError: Construction with invalid string
            The string parameter of the constructor should be exactly 2 characters.

            >>> Card("9h")  # OK
            >>> Card("9h ") # ERROR

        TypeError: Construction with unsupported type
            The parameter of the constructor should be one of the following types: [int,
            str, Card].
            >>> Card(0)       # OK. The 0 stands 2 of Clubs
            >>> Card("2c")    # OK
            >>> Card("2C")    # OK. Capital letter is also accepted.
            >>> Card(Card(0)) # OK
            >>> Card(0.0)     # ERROR. float is not allowed

        TypeError: Setting attribute
            >>> c = Card("2c")
            >>> c.__id = 1      # ERROR
            >>> c._Card__id = 1 # ERROR

        TypeError: Deliting attribute
            >>> c = Card("2c")
            >>> del c.__id      # ERROR
            >>> del c._Card__id # ERROR

    """

    __slots__ = ["__id"]
    __id: int

    def __init__(self, other: Union[int, str, Card]):
        """Construct card object.

        If the passed argument is integer, it's set to `self.__id`.
        If the passed argument is string, its id is calculated and set to `self.__id`.
        Thus, the original string is discarded. e.g. Card("2C").describe_card() == "2c"
        If the passed argument is Card, it's copied.

        Args:
            other (int): The integer that identifies the card.
            other (str): The description of the card. e.g. "2c", "Ah"
            other (Card): The other card to copy.

        Examples:
            Those four variable are same.

            >>> c1 = Card(0)
            >>> c2 = Card("2c")
            >>> c3 = Card("2C")
            >>> c4 = Card(c1)
            >>> print(c1, c2, c3, c4)
            Card("2c") Card("2c") Card("2c") Card("2c")
        """
        card_id = Card.to_id(other)
        # Note: use base class assignment because assignment to this class is protected
        # by `Card.__setattr__`
        # Note: use name mangling: `_Card__id` instead of `Card.__id`.
        object.__setattr__(self, "_Card__id", card_id)  # equiv to `self.__id = card_id`

    @property
    def id_(self) -> int:
        """Return `self.__id`.

        Returns:
            int:
        """
        return self.__id

    @staticmethod
    def to_id(other: Union[int, str, Card]) -> int:
        """Return the Card ID integer as API.

        If the passed argument is integer, it's returned with doing nothing.
        If the passed argument is string, its id is calculated.
        If the passed argument is Card, `other.id_` is returned.

        Args:
            other (int): The integer that identifies the card.
            other (str): The description of the card. e.g. "2c", "Ah"
            other (Card): The other card to copy.

        Raises:
            ValueError: Passed invalid string
            TypeError: Passed unsupported type

        Returns:
            int: Card ID
        """
        if isinstance(other, int):
            return other
        elif isinstance(other, str):
            if len(other) != 2:
                raise ValueError(f"The length of value must be 2. passed: {other}")
            rank, suit, *_ = tuple(other)
            return rank_map[rank] * 4 + suit_map[suit]
        elif isinstance(other, Card):
            return other.id_

        raise TypeError(
            f"Type of parameter must be int, str or Card. passed: {type(other)}"
        )

    def describe_rank(self) -> str:
        """Calculate card rank.

        Returns:
            str: The card rank

        Examples:
            >>> c1 = Card("2c")
            >>> c1.describe_rank()
            "2"

            >>> c2 = Card("Ah")
            >>> c2.describe_rank()
            "A"
        """
        return rank_reverse_map[self.id_ // 4]

    def describe_suit(self) -> str:
        """Calculate suit. It's lowercased.

        Returns:
            str: The suit of the card

        Examples:
            >>> c1 = Card("2c")
            >>> c1.describe_suit()
            "c"

            >>> c2 = Card("2H")
            >>> c2.describe_suit()
            "h"
        """
        return suit_reverse_map[self.id_ % 4]

    def describe_card(self) -> str:
        """Return card description.

        Returns:
            str: The card description.

        Examples:
            >>> c1 = Card("2c")
            >>> c1.describe_card()
            "2c"

            >>> c2 = Card("AH")
            >>> c2.describe_suit()
            "Ah"
        """
        return self.describe_rank() + self.describe_suit()

    def __eq__(self, other: Any) -> bool:
        """Return equality. This is special method.

        Args:
            other (int): This is compared to `int(self)`
            other (str): This is compared to `str(self)`. It's case-insensitive.
            other (Card): `other.id_` is compared to `self.id_`.
            other (Any): This is compared to `self.id_`

        Returns:
            bool: The result of `self == other`

        Examples:
            >>> Card(0) == Card("2c") == Card("2C")
            True

            >>> 3 == Card(3) == 3
            True

            >>> "Ah" == Card("Ah") == "Ah"
            True

            >>> "AH" == Card("Ah") == "AH"
            True
        """
        if isinstance(other, int):
            return int(self) == other
        if isinstance(other, str):
            # case-insensitive
            return str(self).lower() == other.lower()
        if isinstance(other, Card):
            return self.id_ == other.id_
        return self.id_ == other

    def __str__(self) -> str:
        """str: Special method for `str(self)`. e.g. '2c', 'Ah'."""
        return self.describe_card()

    def __repr__(self) -> str:
        """str: Special method for `repr(self)`. e.g. Card("2c"), Card("Ah")."""
        return f'Card("{self.describe_card()}")'

    def __int__(self) -> int:
        """int: Special method for `int(self)`."""
        return self.id_

    def __hash__(self) -> int:
        """int: Special method for `hash(self)`."""
        return hash(self.id_)

    def __setattr__(self, name: str, value: Any) -> None:
        """Set an attribute. This causes TypeError since assignment to attribute is prevented."""
        raise TypeError("Card object does not support assignment to attribute")

    def __delattr__(self, name: str) -> None:
        """Delete an attribute. This causes TypeError since deletion of attribute is prevented."""
        raise TypeError("Card object does not support deletion of attribute")
