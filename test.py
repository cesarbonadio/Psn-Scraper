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

	def test_pythonic_method(self):
		#at Souper class
		self.assertEqual(self.souper.soupByString(self.doc),self.souper2.soupByString(self.doc))		
			
	def tearDown(self):
		self.doc = None
		self.parser = None
		self.souper = None
		self.souper2 = None


class FakeScraperTest(unittest.TestCase):

	def setUp(self):
		self.scraper = Scraper('http://google.com')

	@unittest.expectedFailure
	def test_utf_encode(self):
		self.scraper.setSouperSoup()
		self.assertEqual(self.scraper.getPageName(),self.scraper.getPageName(False))
		
	def tearDown(self):
		self.scraper = None		


if __name__ == '__main__':
	unittest.main()
