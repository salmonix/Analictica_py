import unittest
import Configuration

class TestSourceCoinfiguration(unittest.TestCase):
    
    def setUp(self):
        self.config = Configuration('sources','full_example')
        
    def test_testentry(self):
        self.assertEqual(type( self.config), 'Configure', 'Got configuration object.')
        
        
        