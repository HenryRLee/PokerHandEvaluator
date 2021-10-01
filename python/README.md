# Python Library

## Install and Test
The library requires Python 3. It's recommended to use a virtualenv. 

To install the requirements run:
```
pip install -r requirements.txt
``` 


There are 1000 random examples tested for each type of hand (5 cards, 6 cards, and 7 cards). The examples are stored in json files the tests folder and were generated with the original C++ evaluator.


To run the unit test:

```
cd phevaluator
python3 -m unittest discover tests
```

There are also test code for testing the hash tables
```
cd phevaluator
python3 -m table_tests.test_dptables
python3 -m table_tests.test_hashtable
python3 -m table_tests.test_hashtable5
python3 -m table_tests.test_hashtable6
python3 -m table_tests.test_hashtable7
```

## Using the library
The main function is the `evaluate_cards` function in `phevaluator/evaluator/evaluator.py`.

The function can take both numbers and card strings (with format like: 'Ah' or '2C'). Usage examples can be seen in `examples.py`.

