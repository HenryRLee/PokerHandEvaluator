# PH Evaluator Python package (phevaluator)

## Description

[PH Evaluator](https://github.com/HenryRLee/PokerHandEvaluator) is designed
for evaluating poker hands with more than 5 cards. Instead of traversing all
the combinations, it uses a perfect hash algorithm to get the hand strength
from a pre-computed hash table, which only costs very few CPU cycles and
considerably small memory (~100kb for the 7 card evaluation). With slight
modification, the same algorithm can be also applied to evaluating Omaha
poker hands.

## Installation
The library requires Python 3.
- with `pip`
    ```shell
    pip install .
    ```

## Using the library
The main function is the `evaluate_cards` function.
```python
from phevaluator import evaluate_cards

p1 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "Qc", "6c")
p2 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "2c", "9h")

# Player 2 has a stronger hand
print(f"The rank of the hand in player 1 is {p1}") # 292
print(f"The rank of the hand in player 2 is {p2}") # 236
```
The function can take both numbers and card strings (with format like: 'Ah' or '2C'). Usage examples can be seen in `examples.py`.

## Test
There are 1000 random examples tested for each type of hand (5 cards, 6 cards, and 7 cards). The examples are stored in json files the tests folder and were generated with the original C++ evaluator.

- with current environment
    ```shell
    python3 -m unittest discover -v
    ```

## Development
- recommended to format with [`black`](https://github.com/psf/black) before commit

    check where to correct (without formatting)
    ```shell
    black . --diff --color
    ```
    format all
    ```shell
    black .
    ```

