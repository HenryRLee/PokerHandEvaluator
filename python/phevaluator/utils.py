"""Utilities."""

from __future__ import annotations

import random


def sample_cards(size: int) -> list[int]:
    """Sample random cards with size.

    Args:
        size (int): The size of the sample.

    Returns:
        list[int]: The list of the sampled cards.
    """
    return random.sample(range(52), k=size)
