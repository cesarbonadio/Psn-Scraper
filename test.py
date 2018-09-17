import unittest
from web import *
from bs4 import BeautifulSoup

class BeautifulSoupTest(unittest.TestCase):

    def setUp(self):
    	self.doc = '<html>test</html>'
    	self.parser = 'html.parser'
    	self.souper = Souper(self.parser)
    	self.souper2 = Souper()

    def test_null_parser(self):
    	self.assertEqual(BeautifulSoup(self.doc), BeautifulSoup(self.doc,self.parser),'They are not the same')
    	self.assertEqual(self.souper.soupByString(self.doc),self.souper2.soupByString(self.doc))
    		
    def tearDown(self):
        self.doc = None
        self.parser = None

if __name__ == '__main__':
	unittest.main()

