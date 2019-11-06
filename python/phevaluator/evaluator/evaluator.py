from evaluator.card import Card
from evaluator.evaluator5 import evaluate_5cards
from evaluator.evaluator6 import evaluate_6cards
from evaluator.evaluator7 import evaluate_7cards
from evaluator.evaluator8 import evaluate_8cards
from evaluator.evaluator9 import evaluate_9cards

def evaluate_cards(*args):
  if len(args) == 5:
    return evaluate_5cards(
      Card(args[0]), Card(args[1]), Card(args[2]), Card(args[3]), Card(args[4])
    )
  elif len(args) == 6:
    return evaluate_6cards(
      Card(args[0]), Card(args[1]), Card(args[2]),
      Card(args[3]), Card(args[4]), Card(args[5])
    )
  elif len(args) == 7:
    return evaluate_7cards(
      Card(args[0]), Card(args[1]), Card(args[2]), Card(args[3]),
      Card(args[4]), Card(args[5]), Card(args[6])
    )
  elif len(args) == 8:
    return evaluate_8cards(
      Card(args[0]), Card(args[1]), Card(args[2]), Card(args[3]),
      Card(args[4]), Card(args[5]), Card(args[6]), Card(args[7])
    )
  elif len(args) == 9:
    return evaluate_9cards(
      Card(args[0]), Card(args[1]), Card(args[2]), Card(args[3]), Card(args[4]),
      Card(args[5]), Card(args[6]), Card(args[7]), Card(args[8])
    )
