import requests
import json
import re
import re
import urllib2
from bs4 import BeautifulSoup


psnid = raw_input('Insertar un psn id: ')
print('Scrapping.....')


r = requests.get('https://psnprofiles.com/'+str(psnid))

soup = BeautifulSoup(r.content, 'html.parser')
#print(soup.prettify())

tabla_de_juegos = soup.find('table',{'id':'gamesTable'}).find_all('tr')

print('\nDatos extraidos de la pagina: ' + str(soup.title.string.encode('utf-8')))
print('Juegos que ha jugado el usuario {0}\n\n'.format(psnid))


# output [<a class="title" href="/trophies/2340-minecraft/cesar_gamer12" rel="nofollow">Minecraft</a>]

for juego in tabla_de_juegos:
	print(juego.find_all('span')[0].find_all('a')[0].string+': '+ juego.find_all('b')[0].string +
		  ' trofeos de '+ juego.find_all('b')[1].string)

#print(soup.find('table' , {'id':'gamesTable'}).find_all('tr')[1].find_all('span')[0].find_all('a')[0].string)



