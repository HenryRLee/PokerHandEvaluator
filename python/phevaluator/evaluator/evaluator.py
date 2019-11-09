from evaluator.evaluator5 import evaluate_5cards
from evaluator.evaluator6 import evaluate_6cards
from evaluator.evaluator7 import evaluate_7cards
from evaluator.evaluator8 import evaluate_8cards
from evaluator.evaluator9 import evaluate_9cards

rank_map = {
    '2': 0,
    '3': 1,
    '4': 2,
    '5': 3,
    '6': 4,
    '7': 5,
    '8': 6,
    '9': 7,
    'T': 8,
    'J': 9,
    'Q': 10,
    'K': 11,
    'A': 12
}

suit_map = {
    'C': 0,
    'D': 1,
    'H': 2,
    'S': 3,
    'c': 0,
    'd': 1,
    'h': 2,
    's': 3
}

def evaluate_cards(*args):
  if isinstance(args[0], str):
    cards = []
    for arg in args:
      cards.append(rank_map[arg[0]] * 4 + suit_map[arg[1]])
  else:
    cards = tuple(args) 
    
  if len(args) == 5:
    return evaluate_5cards(*cards)
  elif len(args) == 6:
    return evaluate_6cards(*cards)
  elif len(args) == 7:
    return evaluate_7cards(*cards)
  elif len(args) == 8:
    return evaluate_8cards(*cards)
  elif len(args) == 9:
    return evaluate_9cards(*cards)
