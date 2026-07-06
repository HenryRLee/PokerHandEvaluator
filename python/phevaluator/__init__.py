"""Package for evaluating a poker hand."""

from typing import Any

# import mapping to objects in other modules
all_by_module = {
    "phevaluator": ["card", "evaluator_omaha", "evaluator", "utils"],
    "phevaluator.card": ["Card"],
    "phevaluator.evaluator": [
        "evaluate_cards",
        "evaluate_5cards",
        "evaluate_6cards",
        "evaluate_7cards",
    ],
    "phevaluator.evaluator_omaha": [
        "evaluate_omaha_cards",
        "evaluate_plo4_cards",
        "evaluate_plo5_cards",
        "evaluate_plo6_cards",
    ],
    "phevaluator.utils": ["sample_cards"],
}

# Based on werkzeug library
object_origins = {}
for module, items in all_by_module.items():
    for item in items:
        object_origins[item] = module

__docformat__ = "google"


# Based on https://peps.python.org/pep-0562/ and werkzeug library
def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy submodule imports."""
    if name in object_origins:
        module = __import__(object_origins[name], None, None, [name])
        return getattr(module, name)

    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
