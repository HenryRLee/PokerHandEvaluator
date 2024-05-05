# Test Data

Each directory has two sets of test data, both in csv format. The last column of
each line represents the rank of the test case, and the other columns are the
card input.

In the `string_input_tests.csv` files, the card inputs are using string format,
while in the `id_input_tests.csv` files, the inputs are [Card Id](../cpp/#cardid)
format.

For example, if we look at the file `five/string_input_tests.csv`, it has six columns.
The first five columns are the five different cards, and the last column is the
rank of the given five cards.

```bash
card_1,card_2,card_3,card_4,card_5,rank
2C,2D,2H,2S,3C,166
2C,2D,2H,2S,3D,166
2C,2D,2H,2S,3H,166
2C,2D,2H,2S,3S,166
2C,2D,2H,2S,4C,165
2C,2D,2H,2S,4D,165
2C,2D,2H,2S,4H,165
2C,2D,2H,2S,4S,165
2C,2D,2H,2S,5C,164
```

The cards in the first test case are: 2C, 2D, 2H, 2S, and 3C, which ranks at 166.
