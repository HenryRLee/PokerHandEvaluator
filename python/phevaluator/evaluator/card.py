class Card(int):
  def __new__(cls, value):
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
    if isinstance(value, str):
      value = rank_map[value[0]] * 4 + suit_map[value[1]]
    return super(Card, cls).__new__(cls, value)
