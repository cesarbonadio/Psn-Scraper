import requests,json,re,time,unittest
from web import *
from bs4 import BeautifulSoup

#Test case class to see how works the scraper. To run: "python psn.py"

class ScraperTest(unittest.TestCase):

	def setUp(self):	
		try:
			#python 2
			self.psnid = raw_input('Give me a psn id: ')
		except NameError:
			#python 3
			self.psnid = input('Give me a psn id: ')

		self.player = PlayerScraper(self.psnid)
		self.site = SiteScraper()
		

	def testDicScraper(self):
		self.player.setSouperSoup() #Default link
		self.site.setSouperSoup() #Default link
		print('\nData scraped from: {0}'.format(self.player.getPageName()))
		print(json.dumps(self.site.getSiteStats(),indent = 3))
		#print(json.dumps(self.player.getGameTable(),indent=4))
		#print(json.dumps(self.player.getPlayerBasics(),indent=4))
		print(json.dumps(self.player.getPlayerStats(),indent=4))
		#print(json.dumps(self.player.getRecentTrophies(number=3), indent=4))
		#print(len(self.player.getRecentTrophies(number=2).keys()))
		#print(json.dumps(self.player.getRarestTrophies(), indent = 4))
		#print(json.dumps(self.player.getCountTrophiesRarity(),indent = 4))
		#print(json.dumps(self.player.getTrophiesMilestones(),indent = 4))
		#print(json.dumps(self.player.getLevelsTimestamp(), indent=3))

	def tearDown(self):
		self.psnid = None
		self.player = None
		self.site = None

if __name__ == '__main__':
	unittest.main()			





