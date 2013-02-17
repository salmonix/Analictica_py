# import unittest
from Engines import Yuret
from Data.Elements import Tokens
from pprint import pprint


# class Test.Yuret_linking(unittest.TestCase):


Tok = Tokens()
Yur = Yuret(Tok)
data = [0, 1, 2, 3, 4]
pprint (data)
Yur.process_sentence(data)
