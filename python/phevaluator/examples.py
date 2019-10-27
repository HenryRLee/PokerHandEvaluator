from evaluator.evaluator import evaluate_cards


def example1():
  a = 7 * 4 + 0 # 9c
  b = 2 * 4 + 0 # 4c
  c = 2 * 4 + 3 # 4s
  d = 7 * 4 + 1 # 9d
  e = 2 * 4 + 2 # 4h


  # Player 1
  f = 10 * 4 + 0 # Qc
  g = 4 * 4 + 0 # 6c

  # Player 2
  h = 0 * 4 + 0 # 2c
  i = 7 * 4 + 2 # 9h

  p1 = evaluate_cards(a, b, c, d, e, f, g)  # expected 292
  p2 = evaluate_cards(a, b, c, d, e, h, i)  # expected 236

  print(f'The rank of the hand in player 1 is {p1}')
  print(f'The rank of the hand in player 2 is {p2}')
  print('Player 2 has a stronger hand')

def example2():
  p1 = evaluate_cards('9c', '4c', '4s', '9d', '4h', 'Qc', '6c')  # expected 292
  p2 = evaluate_cards('9c', '4c', '4s', '9d', '4h', '2c', '9h')  # expected 236

  print(f'The rank of the hand in player 1 is {p1}')
  print(f'The rank of the hand in player 2 is {p2}')
  print('Player 2 has a stronger hand')

if __name__ == '__main__':
  example1()
  example2()
