# Python Library

## Install and Test
The library requires Python 3. It's recommended to use a virtualenv. 

To install the requirements run:
```
pip install -r requirements.txt
``` 


There are 1000 random examples tested for each type of hand (5 cards, 6 cards, 7 cards, 8 cards and 9 cards). The examples are stored in json files the tests folder and were generated with the original C++ evaluator.


To run the tests:
```
cd phevaluator
python -m unittest tests.test_evaluator
```

## Using the library
The main function is the `evaluate_cards` function in `phevaluator/evaluator/evaluator.py`.

The function can take both numbers and card strings (with format like: 'Ah' or '2C'). Usage examples can be seen in `examples.py`.

## Benchmark

The performance is of course not as good as the C++ version but the benchmark results on *MacBook Pro 2,2 GHz Quad-Core Intel Core i7, 16GB* are as follow:

CPython 3.7.4 (The standard python interpeter):


PyPy3 (The python python interpeter):


## The simple evaluator

The simple_evaluator is also possible to use and can take in from 5-9 arguments. But it has worse performance.
