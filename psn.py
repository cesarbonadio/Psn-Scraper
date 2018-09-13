import requests,json,re,time
from clases import *
from bs4 import BeautifulSoup


try:
	psnid = raw_input('Give me a psn id: ')
except NameError:
	psnid = input('Give me a psn id: ')


print('Scraping.....')
scrap = Scraper(psnid)
print('\nData scraped from: {0} \n Played Games {1}'.format(scrap.getPageName(),psnid))
print('Json generated:\n\n')

#juegos =  scrap.getGameTable()

#print(juegos['Minecraft']['trophies']['earned'])
#print(type(juegos))
#print(juegos.keys())
#print('\n\n\n')

#print(json.dumps(juegos,indent=4))

#print(json.dumps(scrap.getPlayerBasics(),indent=4))

#print(json.dumps(scrap.getPlayerStats(),indent=4))

#print(json.dumps(scrap.getRecentTrophies(), indent=4))

#print(json.dumps(scrap.getRarestTrophies(), indent = 4))

print(json.dumps(scrap.getCountTrophiesRarity(),indent = 4))


#print(re.compile('abc'))





