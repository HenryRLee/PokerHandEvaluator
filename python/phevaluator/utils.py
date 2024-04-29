"""Utilities."""

from __future__ import annotations

import random
from typing import List


def sample_cards(size: int) -> List[int]:
    """Sample random cards with size.

    Args:
        size (int): The size of the sample.

    Returns:
        List[int]: The list of the sampled cards.
    """
    return random.sample(range(52), k=size)
