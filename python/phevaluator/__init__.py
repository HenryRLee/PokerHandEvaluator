"""Package for evaluating a poker hand."""
from . import hash as hash_  # FIXME: `hash` collides to built-in function


# import mapping to objects in other modules
all_by_module = {
    "phevaluator": ["card", "evaluator_omaha", "evaluator", "hash", "tables", "utils"],
    "phevaluator.card": ["Card"],
    "phevaluator.evaluator": ["_evaluate_cards", "evaluate_cards"],
    "phevaluator.evaluator_omaha": ["_evaluate_omaha_cards", "evaluate_omaha_cards"],
    "phevaluator.utils": ["sample_cards"]
}

# Based on werkzeug library
object_origins = {}
for module, items in all_by_module.items():
    for item in items:
        object_origins[item] = module

__docformat__ = "google"


# Based on https://peps.python.org/pep-0562/ and werkzeug library
def __getattr__(name):
    """lazy submodule imports"""
    if name in object_origins:
        module = __import__(object_origins[name], None, None, [name])
        return getattr(module, name)
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
