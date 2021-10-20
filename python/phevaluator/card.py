from __future__ import annotations

from typing import Union

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
    __slots__ = ["id_"]

    def __init__(self, other: Union[int, str, Card]):
        self.id_ = self.to_int(other)

    @staticmethod
    def to_int(other: Union[int, str, Card]) -> int:
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
            f"Type of paramete must be int, str or Card. passed: {type(other)}"
        )

    def describe_rank(self) -> str:
        return rank_reverse_map[self.id_ // 4]

    def describe_suit(self) -> str:
        return suit_reverse_map[self.id_ % 4]

    def describe_card(self) -> str:
        return self.describe_rank() + self.describe_suit()

    def __eq__(self, other) -> bool:
        if isinstance(other, int):
            return int(self) == other
        if isinstance(other, str):
            return str(self) == other
        if isinstance(other, Card):
            return self.id_ == other.id_
        return self.id_ == other

    def __str__(self) -> str:
        return self.describe_card()

    def __repr__(self) -> str:
        return f'Card("{self.describe_card()}")'

    def __int__(self) -> int:
        return self.id_

    def __hash__(self) -> int:
        return hash(self.id_)
