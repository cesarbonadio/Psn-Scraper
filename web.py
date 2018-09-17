import requests,json,re,time
import util
from bs4 import BeautifulSoup
from bs4 import Comment
import itertools 




class Souper:

	__soup = None

	def __init__(self, parser = None):
		self.__parser = parser

	def soupByLink(self,link):
		r = requests.get(link)
		return BeautifulSoup(r.content,self.__parser) if self.__parser else BeautifulSoup(r.content)	

	def soupByString(self,doc):
		return BeautifulSoup(doc,self.__parser) if self.__parser else BeautifulSoup(doc)
	
	def setSoup(self,soup):
		self.__soup = soup

	def getSoup(self):
		return self.__soup	

	def setParser(self,parser):
		self.__parser = parser		



class Scraper:

	def __init__(self,base_link = 'https://psnprofiles.com/'):
		self.base_link = base_link
		self.souper = Souper('html.parser')

	def setSouperSoup(self, link = None):
		if link is None: link = self.base_link
		self.souper.setSoup(self.souper.soupByLink(link))

	def getPageName(self, utf_8 = True):
		return self.souper.getSoup().title.string.encode('utf-8') if utf_8 else self.souper.getSoup().title.string	













class PlayerScraper(Scraper):

	def __init__(self,psn_id,base_link = 'https://psnprofiles.com/'):
		Scraper.__init__(self, base_link + psn_id)
		

	def getPlayerBasics(self):
		profile = self.souper.getSoup().find('ul',{'class':'profile-bar'})

		level = profile.find_all('li',{'class':'icon-sprite level'})[0].string
		percentage = self.souper.soupByString(str(profile.find_all(string = lambda text:isinstance(text,Comment))[0])).span.string
		country = self.souper.soupByString(str(profile.find(id = 'bar-country').get('title'))).center.string

		trophies_count = profile.find_all('li',{'class':['total','platinum','gold','silver','bronze']})
		trophies_count = [util.replaceByList(trophies_count[n].get_text(),[["\t",""],["\n",""],["\r",""]]) for n in range(len(trophies_count))]
		
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
		stats_generator = self.souper.getSoup().find('div',{'class':'stats flex'}).find_all('span')
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

		

	def getRecentTrophies(self, number = 9):

		all = {}

		for i in range((number//50)+1):

			log_soup = self.souper.soupByLink(self.base_link + self.psn_id + '/log'+'?page='+str(i+1))
			recent_table = log_soup.find('table',{'class':'zebra'}).find_all('tr')
			recent = {}

			for recent_trophy in range(number-(50*i)):

				try:

					generator = recent_table[recent_trophy].stripped_strings

					title = generator.next()
					description = generator.next()
					trophy_number = generator.next().replace("#","")
					timestamp = generator.next()+generator.next()+' '+generator.next()+' at '+generator.next()
					achievers = generator.next()
					generator.next()
					game_owners = generator.next()
					generator.next()
					rarity_percentage = generator.next()
					rarity_type = generator.next()
					type = recent_table[recent_trophy].find_all('img')[2].get('title').lower()
					game = recent_table[recent_trophy].find_all('img')[0].get('title')


					recent.update({title: {
					'description': description,
					'trophy_number': trophy_number, 
					'timestamp': timestamp,
					'achievers': achievers,
					'game_owners': game_owners,
					'game' : game,
					'type': type,
					'rarity':{
					'percentage': rarity_percentage,
					'type' : rarity_type
						} 
					}
					})

				except IndexError:
					break

			all.update(recent)			

		return all




	def getRarestTrophies(self):
		rarest = {}
		rarest_trophies = self.souper.getSoup().find_all('table',{'class':'zebra'})[2].find_all('tr')

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
		count_generator = self.souper.getSoup().find('div',{'class':'row lg-hide'}).stripped_strings

		return {
		count_generator.next(): count_generator.next(),
		count_generator.next(): count_generator.next(),
		count_generator.next(): count_generator.next(),
		count_generator.next(): count_generator.next(),
		count_generator.next(): count_generator.next()
		}






	def getGameTable(self):
		games = {}
		table = self.souper.getSoup().find('table',{'id':'gamesTable'}).find_all('tr')

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
				last = 	util.replaceByList(game.find_all('div',{'class':'small-info'})[1].get_text(),[["  ",""],["\n",""],["\t",""]])
			except IndexError:
				last = 	'No trophies or missing timestamp'
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




	def getTrophiesMilestones(self):
		trophies = {}
		table = self.souper.getSoup().find('table',{'class':'box zebra'}).find_all('tr')

		for trophy in table:
			generator = trophy.stripped_strings
			trophy_title = generator.next()
			game = generator.next()
			description = generator.next()
			timestamp = generator.next()

			trophies.update({trophy_title:{
			'game' : game,
			'description' : description,
			'timestamp' : timestamp
			}
			})

		return trophies




	def getLevelsTimestamp(self):
		levels = {}
		level_soup = self.souper.soupByLink(self.base_link + self.psn_id + '/levels')
		table = level_soup.find('table',{'box zebra animate'}).find_all('tr')

		for trophy in reversed(table):
			level_reached = trophy.get('id').replace("level-","")
			generator = trophy.stripped_strings
			trophy_title = generator.next()
			trophy_description = generator.next()
			timestamp = util.replaceByList(trophy.find('span',{'class':'separator left'}).get_text(),[["\t",""],["\n"," "],["\r",""]])

			levels.update({level_reached:{
			'timestamp': timestamp,
			'trophy' :{ 
			'title':trophy_title,
			'description':trophy_description
					}
				}
			})

		return levels




				