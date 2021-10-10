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


class Card(int):
    def __new__(cls, value: Union[int, str, Card]) -> Card:
        if isinstance(value, str):
            rank, suit = value
            value = rank_map[rank] * 4 + suit_map[suit]
        return super(Card, cls).__new__(cls, value)

    def describe_rank(self) -> str:
        return rank_reverse_map[self // 4]

    def describe_suit(self) -> str:
        return suit_reverse_map[self % 4]

    def describe_card(self) -> str:
        return self.describe_rank() + self.describe_suit()

    def __str__(self) -> str:
        return self.describe_card()

    def __repr__(self) -> str:
        return f'Card("{self.describe_card()}")'
