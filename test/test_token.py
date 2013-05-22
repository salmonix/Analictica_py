import os
import unittest
from Elements import Token


""" I have to admit the the thing I most hate in Python is the test system... Perl's Test::More is tooooo comfortable...."""
class CreationAndBasicTokenMethods(unittest.TestCase):

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        root = Token()
        root.S = 3
        self.input = ({'name':'Ghani', 'freq':3.0, 'parent':root},
                     {'name':'Irulan', 'freq':1.0, 'parent':root},
                     {'name':'Alia', 'freq':2.0, 'parent':root},
                     )
        self.root = Token()

    def test_instantiation(self):

        for i in self.input:
            self.root.add_token(i)

        self.assertEqual(len(self.root.tokens), 3)





if __name__ == '__main__':
    unittest.main()
