from bs4 import BeautifulSoup
import requests
import csv
import re
import datetime

def getDate(counter_days):
	"""
	date_div = (tr.find('div', class_='flleft').text).split(" ")
	date_day = date_div[0]
	m = re.search(r'(\d+)(\w+)', date_div[1])
	date_number, date_month = m.group(1), m.group(2)
	return f'{date_day} {date_number} {date_month}'
	"""
	today = datetime.date.today()
	tdelta = datetime.timedelta(days=counter_days)
	return today + tdelta

def getTime(td):
	time_text = td.find('td').text.split(':')
	time = datetime.time(int(time_text[0]), int(time_text[1]))
	date_and_time = datetime.datetime.combine(getDate(counter_days-1), time) 
	return date_and_time

def getTemperature(td):
	if (td.find('div', class_='normal tempcolorcell')):
		temp_humidity = td.find('div', class_='normal tempcolorcell').text
	if (td.find('div', class_='normal maxtemp tempcolorcell')):
		temp_humidity = td.find('div', class_='normal maxtemp tempcolorcell').text
	split = temp_humidity.strip().split('\n')
	if len(split) == 2:
		temperature = split[0].split("°")[0]
		humidity = split[1].split("%")[0]
		return temperature, "", humidity
	if len(split) == 3: 						#face temperature
		temperature = split[0].split("°")[0]
		temperature_face = split[1].split("°")[0]
		humidity = split[2].split("%")[0]
		return temperature, temperature_face, humidity


def getWind(td):
	td_wind = td.text
	beaufort_direction_speed = td_wind.strip().split('\n')
	beaufort_direction = beaufort_direction_speed[0].replace("Μπφ","").split(" ")
	beaufort = beaufort_direction[0]
	direction = beaufort_direction[2]
	speed = beaufort_direction_speed[1].split('Km/h')[0]
	return beaufort, direction, speed

def getDesciption(td):
	return td.text.strip().replace('\n','',1).split('\n')[0]

def perhourRowmargin(tr):
	"""
	print(getTime(tr.find('td', class_= 'innerTableCell fulltime')))
	print(getTemperature(tr.find('td', class_= 'innerTableCell temperature tempwidth')))
	print(getWind(tr.find('td', class_= 'innerTableCell anemosfull')))
	print(getDesciption(tr.find('td', class_= 'innerTableCell PhenomenaSpecialTableCell phenomenafull')))
	"""
	date_and_time = getTime(tr.find('td', class_= 'innerTableCell fulltime'))
	temperature, temperature_face, humidity = getTemperature(tr.find('td', class_= 'innerTableCell temperature tempwidth'))
	beaufort, direction, speed = getWind(tr.find('td', class_= 'innerTableCell anemosfull'))
	desciption = getDesciption(tr.find('td', class_= 'innerTableCell PhenomenaSpecialTableCell phenomenafull'))
	meteo_dict[getTime(tr.find('td', class_= 'innerTableCell fulltime'))] = {
												'temperature' : temperature, 
												'temperature_face' : temperature_face,
												'humidity' : humidity,
												'beaufort' : beaufort,
												'direction' : direction,
												'speed' : speed,
												'desciption' : desciption}

source = requests.get('https://meteo.gr/cf.cfm?city_id=37').text
soup = BeautifulSoup(source, 'lxml')
#with open ('meteoArgos.html') as source:
#	soup = BeautifulSoup(source, 'lxml')

meteo_dict = {}
content = soup.find('div', class_='content')
table = content.find('table')
children = table.findChildren("tr" , recursive=False)
counter_days = 0
for tr in children:
	if (tr.find('td', class_= 'innerTableCell fulltime')):
		perhourRowmargin(tr)
	else:
		counter_days += 1
print(meteo_dict)