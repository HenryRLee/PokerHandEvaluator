import unittest
import json
import os

from evaluator.evaluator import evaluate_cards

CARDS_FILE_5 = os.path.join(os.path.dirname(__file__), 'cardfiles/5cards.json')
CARDS_FILE_6 = os.path.join(os.path.dirname(__file__), 'cardfiles/6cards.json')
CARDS_FILE_7 = os.path.join(os.path.dirname(__file__), 'cardfiles/7cards.json')
CARDS_FILE_8 = os.path.join(os.path.dirname(__file__), 'cardfiles/8cards.json')
CARDS_FILE_9 = os.path.join(os.path.dirname(__file__), 'cardfiles/9cards.json')


class TestEvaluator(unittest.TestCase):

  def test_example(self):
    p1 = evaluate_cards('9c', '4c', '4s', '9d', '4h', 'Qc', '6c')
    p2 = evaluate_cards('9c', '4c', '4s', '9d', '4h', '2c', '9h')
    
    self.assertEqual(p1, 292)
    self.assertEqual(p2, 236)
    self.assertLess(p2, p1)

  def test_5cards(self):
    with open(CARDS_FILE_5, 'r') as read_file:
      hand_dict = json.load(read_file)
      for key, value in hand_dict.items():
        self.assertEqual(evaluate_cards(*key.split()), value)

  def test_6cards(self):
    with open(CARDS_FILE_6, 'r') as read_file:
      hand_dict = json.load(read_file)
      for key, value in hand_dict.items():
        self.assertEqual(evaluate_cards(*key.split()), value)

  def test_7cards(self):
    with open(CARDS_FILE_7, 'r') as read_file:
      hand_dict = json.load(read_file)
      for key, value in hand_dict.items():
        self.assertEqual(evaluate_cards(*key.split()), value)
 
  def test_8cards(self):
    with open(CARDS_FILE_8, 'r') as read_file:
      hand_dict = json.load(read_file)
      for key, value in hand_dict.items():
        self.assertEqual(evaluate_cards(*key.split()), value)

  def test_9cards(self):
      with open(CARDS_FILE_9, 'r') as read_file:
        hand_dict = json.load(read_file)
        for key, value in hand_dict.items():
          self.assertEqual(evaluate_cards(*key.split()), value)
