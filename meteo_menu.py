"""
On this file we are extracting the menu of meteo.gr
We exctract the state of towns, towns names add their id
"""

from bs4 import BeautifulSoup
import requests
import re

def get_menu(url):
	source = requests.get(url).text
	soup = BeautifulSoup(source, 'lxml')
	areas = soup.find_all('h2', class_='m')
	towns = soup.find_all('div', class_='divided')
	menu_dict = {}
	for area, towm in zip(areas, towns):
		m = re.findall(r'href="\/cf\.cfm\?city_id=(\d+)">( *\w+.*)<\/a>', str(towm))
		if len(m) > 0:
			menu_dict[area.text.strip()] = {city.strip():ids for ids,city in m}
	return menu_dict


url = 'https://meteo.gr/cf.cfm?city_id=171' # URL of nauplion, a random city in order to get the available menu
print(get_menu(url))
