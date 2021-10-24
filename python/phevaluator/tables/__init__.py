"""Pre-calculated tables."""
from .dptables import BINARIES_BY_ID, CHOOSE, DP, SUITBIT_BY_ID, SUITS
from .hashtable import FLUSH
from .hashtable5 import NO_FLUSH_5
from .hashtable6 import NO_FLUSH_6
from .hashtable7 import NO_FLUSH_7
from .hashtable_omaha import FLUSH_OMAHA, NO_FLUSH_OMAHA

__all__ = [
    "BINARIES_BY_ID",
    "CHOOSE",
    "DP",
    "SUITBIT_BY_ID",
    "SUITS",
    "FLUSH",
    "NO_FLUSH_5",
    "NO_FLUSH_6",
    "NO_FLUSH_7",
    "FLUSH_OMAHA",
    "NO_FLUSH_OMAHA",
]
