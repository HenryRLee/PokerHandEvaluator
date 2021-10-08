# phevaluator: PokerHandEvaluator (Python Implementation)
## Installation
The library requires Python 3.
- with `pip`
    ```shell
    pip install .
    ```
- with `Poetry`
    ```shell
    poetry install
    ```

(advanced)
- `pip`
    - install dependencies only
        ```shell
        pip install -r requirements.txt
        ```
- `Poetry`
    - check validity of `pyproject.toml`
        ```shell
        poetry check
        ```
    - install dependencies only
        ```shell
        poetry install --no-root
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
    python3 -m unittest discover
    ```
- with isolated environment of `Poetry`
    ```shell
    poetry run python -m unittest discover
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

