# import mapping to pre-calculated tables in other modules
all_by_module = {
    "phevaluator.tables.dptables": ["CHOOSE", "DP", "SUITS"],
    "phevaluator.tables.hashtable": ["FLUSH"],
    "phevaluator.tables.hashtable5": ["NO_FLUSH_5"],
    "phevaluator.tables.hashtable6": ["NO_FLUSH_6"],
    "phevaluator.tables.hashtable7": ["NO_FLUSH_7"],
    "phevaluator.tables.hashtable_omaha": ["FLUSH_OMAHA", "NO_FLUSH_OMAHA"]
}

# Based on werkzeug library
object_origins = {}
for module, items in all_by_module.items():
    for item in items:
        object_origins[item] = module

# fmt: off
BINARIES_BY_ID = [
    0x1, 0x1, 0x1, 0x1,
    0x2, 0x2, 0x2, 0x2,
    0x4, 0x4, 0x4, 0x4,
    0x8, 0x8, 0x8, 0x8,
    0x10, 0x10, 0x10, 0x10,
    0x20, 0x20, 0x20, 0x20,
    0x40, 0x40, 0x40, 0x40,
    0x80, 0x80, 0x80, 0x80,
    0x100, 0x100, 0x100, 0x100,
    0x200, 0x200, 0x200, 0x200,
    0x400, 0x400, 0x400, 0x400,
    0x800, 0x800, 0x800, 0x800,
    0x1000, 0x1000, 0x1000, 0x1000,
]

SUITBIT_BY_ID = [0x1, 0x8, 0x40, 0x200] * 13
# fmt: on


# Based on https://peps.python.org/pep-0562/ and werkzeug library
def __getattr__(name):
    """lazy submodule imports"""
    if name in object_origins:
        module = __import__(object_origins[name], None, None, [name])
        return getattr(module, name)
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
