from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import datetime 
import os 
import time
import pytz
from pony.orm import *
from daemonize import Daemonize


db = Database()
db.bind(provider='mysql', host='127.0.0.1', port=3306, user='root', passwd='iddqd3133122', db='narnik')

class Bettingoffer(db.Entity):
	id = PrimaryKey(int, auto=True)
	eventID = Required(int)
	eventFK = Required(int)
	eventType = Required(str)
	eventName = Required(str)
	evevntTime = Required(str)
	homeResult = Optional(str)
	awayResult = Optional(str)
	home_odd = Optional(float)
	away_odd = Optional(float)
	over_odd = Optional(float)
	under_odd = Optional(float) 
	hdp = Optional(str)
	ou = Optional(str)
	active = Required(str)
	is_live = Required(str)
	is_del = Required(str) 
	n = Required(int)
	ut = Required(str)

db.generate_mapping(create_tables=True)


url = "http://w2.kkkk99.net/"

login_url = "?r=1"
main_url = "main.php"

username = "x660s1573"
password = "aa123456"

browser = webdriver.PhantomJS()


def login():

	browser.get(url + login_url)
	
	button = WebDriverWait(browser, 100).until(
		EC.presence_of_element_located((By.XPATH, "//button[@id='signin-submit']"))
	)

	browser.find_element_by_xpath('//input[@id="txtUsername"]').send_keys(username)
	browser.find_element_by_xpath('//input[@id="txtPassword"]').send_keys(password)

	button.click()


def get_security_code():

	frame = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.XPATH, "//iframe[@id='main']"))
	)

	browser.switch_to.frame('main')
	form = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.XPATH, "//form[@id='form1']"))
	)

	security_code_input = browser.find_element_by_xpath('//input[@id="txtNewPwd1"]')
	if security_code_input:
		print(security_code_input)
		security_code_input.send_keys(security_code)
	button = browser.find_element_by_xpath('//button[@id="btnSubmit"]') 

	button.click()


def close_popup():
	
	button = WebDriverWait(browser, 1000).until(
		EC.presence_of_element_located((By.XPATH, "//button[@id='btnAccept']"))
	)

	button.click()


def wait_table():

	frameset = WebDriverWait(browser, 1000).until(
		EC.presence_of_element_located((By.XPATH, "//frameset"))
	)
	
	change_language()

	browser.get('http://49297922.w2.kkkk99.net/index.php/content/hdp/2')

	table_container = WebDriverWait(browser, 1000).until(
		EC.presence_of_element_located((By.XPATH, "//div[@id='mTableContainer']"))
	)


def change_language():

	browser.get('http://49297922.w2.kkkk99.net/index.php/main/switch_lang/en')
		

def parse_table():

	html = browser.page_source
	soup = BeautifulSoup(html, "html.parser")

	for tbody in soup.find(id='mTableContainer_Live').findAll('tbody')[1:]:
		if tbody.find('th'):
			eventType = tbody.find('th').get_text().replace("'", "")
		for tr in tbody.findAll('tr'):
			
			live = 'no'

			if tr.get('id') is not None:
				eventID = int('{}{}'.format(
					tr.get('id').split('__')[-2], 
					tr.get('id').split('__')[-1]
					))

				text_match = tr.findAll('td', { 'class' : 'text_match' })
				if text_match:
					text_match = text_match[0]

					homeName = text_match.select('span[class=rong]')
					if homeName:
						homeName = homeName[0].get_text().strip()

					alwayName = text_match.select('span[class=tor]')
					if alwayName:
						alwayName = alwayName[0].get_text().strip()

					eventName = '{}-sv-{}'.format(homeName, alwayName)

				text_time = tr.select('td[class*=match__{}__{}]'.format(
					tr.get('id').split('__')[-3],
					tr.get('id').split('__')[-2])
				)
				if text_time:
					text_time = text_time[0]

					homeResult = text_time.select('span[class*=hscore__{}__{}]'.format(
						tr.get('id').split('__')[-3],
						tr.get('id').split('__')[-2])
					)
					if homeResult:
						homeResult = homeResult[0].get_text().strip()

					awayResult = text_time.select('span[class*=ascore__{}__{}]'.format(
						tr.get('id').split('__')[-3],
						tr.get('id').split('__')[-2])
					)
					if awayResult:
						awayResult = awayResult[0].get_text().strip()

					firstSecond = text_time.select('span[class*=first_second__{}__{}]'.format(
						tr.get('id').split('__')[-3],
						tr.get('id').split('__')[-2])
					)
					if firstSecond:
						firstSecond = firstSecond[0].get_text()

					runningTime = text_time.select('span[class*=running_time__{}__{}]'.format(
						tr.get('id').split('__')[-3],
						tr.get('id').split('__')[-2])
					)
					if runningTime:
						runningTime = runningTime[0].get_text()

					if firstSecond == 'Live!':
						eventTime = firstSecond.strip()
						eventTime = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
						live = 'yes'

					elif firstSecond and runningTime:
						eventTime = datetime.time(
							int(firstSecond[:-1].strip()),
							int(runningTime[:-1].strip())
							).strftime("%Y-%m-%d %H:%M:%S")
					else:
						eventTime = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

				text_balls = tr.findAll('td', { 'class' : 'text_ball' })
				if text_balls:

					hdp = text_balls[0]
					if hdp:
						hdp = hdp.select('span[id*=out_ball__{}__{}__0__1]'.format(
							tr.get('id').split('__')[-3],
							tr.get('id').split('__')[-2])
						)
						if hdp:
							hdp = hdp[0].get_text()
						if not hdp:
							hdp = ''
					else:
						hdp = ''

					ou = text_balls[1]
					if ou:
						ou = ou.select('span[id*=out_ball__{}__{}__0__3]'.format(
							tr.get('id').split('__')[-3],
							tr.get('id').split('__')[-2])
						)
						if ou:
							ou = ou[0].get_text()
						if not ou:
							ou = ''
					else: 
						ou = ''

				home_odd_td = tr.select('td[id*=out_my_h__{}__{}__0__1__td]'.format(
					tr.get('id').split('__')[-3],
					tr.get('id').split('__')[-2])
				)
				if home_odd_td:
					home_odd_td = home_odd_td[0]
					home_odd = home_odd_td.select('a[id*=out_my_h__{}__{}__0__1]'.format(
						tr.get('id').split('__')[-3],
						tr.get('id').split('__')[-2])
					)
					if home_odd:
						if isinstance(home_odd, list):
							home_odd = home_odd[0].get_text()
						else:
							home_odd = home_odd.get_text()
							
						if not home_odd:
							home_odd = 0
						else:
							home_odd = float(home_odd)
					else: 
						home_odd = 0 

				away_odd_td = tr.select('td[id*=out_my_a__{}__{}__0__1__td]'.format(
					tr.get('id').split('__')[-3],
					tr.get('id').split('__')[-2])
				)
				if away_odd_td:
					away_odd_td = away_odd_td[0]
					away_odd = away_odd_td.select('a[id*=out_my_a__{}__{}__0__1]'.format(
						tr.get('id').split('__')[-3],
						tr.get('id').split('__')[-2])
					)
					if away_odd:
						if isinstance(away_odd, list):
							away_odd = away_odd[0].get_text()
						else:
							away_odd = away_odd.get_text()
							
						if not away_odd:
							away_odd = 0
						else:
							away_odd = float(away_odd)
					else: 
						away_odd = 0

				over_odd_td = tr.select('td[id*=out_my_h__{}__{}__0__3__td]'.format(
					tr.get('id').split('__')[-3],
					tr.get('id').split('__')[-2])
				)
				if over_odd_td:
					over_odd_td = over_odd_td[0]
					over_odd = over_odd_td.select('a[id*=out_my_h__{}__{}__0__3]'.format(
						tr.get('id').split('__')[-3],
						tr.get('id').split('__')[-2])
					)
					if over_odd:
						if isinstance(over_odd, list):
							over_odd = over_odd[0].get_text()
						else:
							over_odd = over_odd.get_text()
							
						if not over_odd:
							over_odd = 0
						else:
							over_odd = float(over_odd)
					else: 
						over_odd = 0

				under_odd_td = tr.select('td[id*=out_my_a__{}__{}__0__3__td]'.format(
					tr.get('id').split('__')[-3],
					tr.get('id').split('__')[-2])
				)
				if under_odd_td:
					under_odd_td = under_odd_td[0]
					under_odd = under_odd_td.select('a[id*=out_my_a__{}__{}__0__3]'.format(
						tr.get('id').split('__')[-3],
						tr.get('id').split('__')[-2])
					)
					if under_odd:
						if isinstance(under_odd, list):
							under_odd = under_odd[0].get_text()
						else:
							under_odd = under_odd.get_text()

						if not under_odd:
							under_odd = 0
						else:
							under_odd = float(under_odd)
					else: 
						under_odd = 0

				params = (
					eventID, 1, eventType, eventName, eventTime, homeResult, awayResult, 
					home_odd, away_odd, over_odd, under_odd, hdp, ou, 'yes', live, 'no', 1, '2017-08-22 15:44:05'
					)
				print(params)

				with db_session:
					bettingoffer = Bettingoffer.get(eventID=eventID)
					if bettingoffer:
						bettingoffer.set(
							homeResult=homeResult,
							awayResult=awayResult,
							home_odd=home_odd,
							away_odd=away_odd,
							over_odd=over_odd,
							under_odd=under_odd,
							hdp=hdp,
							ou=ou,
							)
					else:
						bettingoffer = Bettingoffer(
							eventID=eventID,
							eventFK=1,
							eventType=eventType,
							eventName=eventName,
							evevntTime=eventTime,
							homeResult=homeResult,
							awayResult=awayResult,
							home_odd=home_odd,
							away_odd=away_odd,
							over_odd=over_odd,
							under_odd=under_odd,
							hdp=hdp,
							ou=ou,
							active='yes',
							is_live=live,
							is_del='no',
							n=1,
							ut=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
							)
					commit()


def main():
	
	login()

	close_popup()
	
	wait_table()

	while True:
		print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		parse_table()
		time.sleep(10)
	
	browser.quit()


if __name__ == '__main__':
	pidfile='/tmp/%s' % 'bet_parser'
	daemon = Daemonize(app='bet_parser', pid=pidfile, action=main)
	daemon.start()