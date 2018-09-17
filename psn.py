import requests,json,re,time
from web import *
from bs4 import BeautifulSoup


try:
	psnid = raw_input('Give me a psn id: ')
except NameError:
	psnid = input('Give me a psn id: ')


print('Scraping.....')
scrap = Scraper(psnid,'https://psnprofiles.com/')
scrap.setSouperSoup()
print('\nData scraped from: {0} \n Played Games {1}'.format(scrap.getPageName(),psnid))
print('Json generated:\n\n')

#juegos =  scrap.getGameTable()

#print(juegos['Minecraft']['trophies']['earned'])
#print(type(juegos))
#print(juegos.keys())
#print('\n\n\n')

#print(json.dumps(scrap.getGameTable(),indent=4))

#print(json.dumps(scrap.getPlayerBasics(),indent=4))

#print(json.dumps(scrap.getPlayerStats(),indent=4))

#print(json.dumps(scrap.getRecentTrophies(number=1), indent=4))

#print(len(scrap.getRecentTrophies(number=2).keys()))


#print(json.dumps(scrap.getRarestTrophies(), indent = 4))

#print(json.dumps(scrap.getCountTrophiesRarity(),indent = 4))

#print(json.dumps(scrap.getTrophiesMilestones(),indent = 4))


#print(json.dumps(scrap.getLevelsTimestamp(), indent=3))

#print(re.compile('abc'))





