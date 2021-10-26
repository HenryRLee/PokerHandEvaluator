"""Package for evaluating a poker hand."""
from . import hash as hash_  # FIXME: `hash` collides to built-in function
from . import tables
from .card import Card
from .evaluator import _evaluate_cards, evaluate_cards
from .evaluator_omaha import _evaluate_omaha_cards, evaluate_omaha_cards
from .utils import sample_cards

__all__ = ["tables", "Card", "evaluate_cards", "evaluate_omaha_cards", "sample_cards"]

__docformat__ = "google"
