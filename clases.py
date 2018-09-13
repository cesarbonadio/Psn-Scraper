import requests,json,re,time
from bs4 import BeautifulSoup
from bs4 import Comment
import itertools 

class Scraper:

	link = 'https://psnprofiles.com/'
	psn_id = ''

	def __init__(self,psn_id):
		self.soup = self.__doSoup(self.link + psn_id)



	def __doSoup(self,link):
		r = requests.get(link)
		soup = BeautifulSoup(r.content, 'html.parser')
		return soup	


	def __replacerList(self,text,re):
		for r in re:
			text = text.replace(r[0],r[1])
		return text

	
	def getPageName(self):
		return self.soup.title.string.encode('utf-8')


	def getPlayerBasics(self):
		#find the profile tag first
		profile = self.soup.find('ul',{'class':'profile-bar'})

		level = profile.find_all('li',{'class':'icon-sprite level'})[0].string
		percentage = BeautifulSoup(str(profile.find_all(string = lambda text:isinstance(text,Comment))[0]), 'html.parser').span.string
		country = BeautifulSoup(str(profile.find(id = 'bar-country').get('title')), 'html.parser').center.string

		trophies_count = profile.find_all('li',{'class':['total','platinum','gold','silver','bronze']})
		trophies_count = [self.__replacerList(trophies_count[n].get_text(),[["\t",""],["\n",""],["\r",""]]) for n in range(len(trophies_count))]
		
		return { 
					'level' : level, 
					'percentage': percentage,
				   	'country' : country,
				   	'trophies' : {
				   	'platinum': trophies_count[1],
				   	'gold': trophies_count[2],
				   	'silver': trophies_count[3],
				   	'bronze': trophies_count[4],
				   	'total': trophies_count[0]
				   	}
				}



	def getPlayerStats(self):
		stats_generator = self.soup.find('div',{'class':'stats flex'}).find_all('span')
		stats_array = [stats_generator[n].stripped_strings.next() for n in range(len(stats_generator)) if n%2==0]
		
		return {
					'played': stats_array[0],
					'completed' : stats_array[1],
					'completion' : stats_array[2],
					'unearned_trophies': stats_array[3],
					'per_day':stats_array[4],
					'views': stats_array[5],
					'world_rank' : stats_array[6],
					'country_rank': stats_array[7]
		}

		

	def getRecentTrophies(self):
		recent = {}
		recent_trophies = self.soup.find('ul',{'class':'recent-trophies flex'}).find_all('li')

		for trophy in recent_trophies:

			generator = trophy.stripped_strings

			title = generator.next()
			description = generator.next()
			ago = generator.next().replace(" in","")
			game = generator.next()
			rarity_percentage = generator.next()
			rarity_type = generator.next()
			type = trophy.find('img').get('alt')

			recent.update({title: {
							'description': description,
							'ago': ago,
							'game' : game,
							'type': type,
							'rarity':{
							'percentage': rarity_percentage,
							'type' : rarity_type
					} 
				}
			})

		return recent




	def getRarestTrophies(self):
		rarest = {}
		rarest_trophies = self.soup.find_all('table',{'class':'zebra'})[2].find_all('tr')

		for trophy in rarest_trophies:

			generator = trophy.stripped_strings
			
			title = generator.next()
			game = generator.next()
			rarity_percentage = generator.next()
			rarity_type = generator.next()
			type = trophy.find_all('img')[1].get('alt')

			rarest.update({title:{
							'game':game,
							'type' : type,
							'rarity':{
								'percentage': rarity_percentage,
								'type' : rarity_type
					}
				}
			})

		return rarest




	def getCountTrophiesRarity(self):
		count_generator = self.soup.find('div',{'class':'row lg-hide'}).stripped_strings

		return {
					count_generator.next(): count_generator.next(),
					count_generator.next(): count_generator.next(),
					count_generator.next(): count_generator.next(),
					count_generator.next(): count_generator.next()
		}



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
				last = 	self.__replacerList(game.find_all('div',{'class':'small-info'})[1].get_text(),[["  ",""],["\n",""],["\t",""]])
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