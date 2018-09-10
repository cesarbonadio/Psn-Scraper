import requests,json,re,time
from bs4 import BeautifulSoup
from bs4 import Comment

class Scraper:

	link = 'https://psnprofiles.com/'
	psn_id = ''

	def __init__(self,psn_id):
		self.soup = self.__doSoup(self.link + psn_id)



	def __doSoup(self,link):
		r = requests.get(link)
		soup = BeautifulSoup(r.content, 'html.parser')
		return soup	


	
	def getPageName(self):
		return self.soup.title.string.encode('utf-8')


	def getPlayerStats(self):
		stats = {}

		#find the profile tag first
		profile = self.soup.find_all('ul',{'class':'profile-bar'})[0]


		level = profile.find_all('li',{'class':'icon-sprite level'})[0].string
		percentage = BeautifulSoup(str(profile.find_all(string = lambda text:isinstance(text,Comment))[0]), 'html.parser').span.string
		country = BeautifulSoup(str(profile.find(id = 'bar-country').get('title')), 'html.parser').center.string


		stats.update({ 
					   'level' : level, 
					   'percentage': percentage,
					   'country' : country,
					 })

		return stats	



	def getGameTable(self):
		games = {}

		table = self.soup.find('table',{'id':'gamesTable'}).find_all('tr')



		for game in table:

			name = game.find_all('span')[0].find_all('a')[0].string

			earned = game.find_all('b')[0].string
			unearned = game.find_all('b')[1].string

			platforms = game.find_all('div',{'class':'platforms'})[0].find_all('span')
			platforms = [platforms[n].string for n in range(len(platforms))]

			rank = game.find_all('span',{'class':['game-rank '+l for l in ('A','B','C','D','E','F','S')]})[0].string

			trophie_progress = game.find_all('div',{'class':'trophy-count'})[0].find_all('span')
			general_progress = trophie_progress[6].string
			trophie_progress = [trophie_progress[n].string for n in range(len(trophie_progress)) if n%2!=0]





						
			try:
				last = game.find_all('div',{'class':'small-info'})[1].get_text().replace("  ","").replace("\n","").replace("\t","")
			except IndexError:
				last = 	'No trophies or missing timestamp for the last earn'
				pass


			games.update({name:{
									'trophies': {
									'earned': earned , 
									'unearned': unearned, 
									'last': last,
									'progress' : general_progress,
										'count':{
										'gold': trophie_progress[0],
										'silver': trophie_progress[1],
										'bronze' : trophie_progress[2]
										}
									 },

									'platforms' : platforms,
									'rank': rank 
								}
						})

		return games




