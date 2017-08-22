from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import datetime 
import os 
import time
import pymysql
import pytz

url = "http://w2.kkkk99.net/"
login_url = "?r=1"
main_url = "main.php"

username = ""
password = ""

browser = webdriver.PhantomJS()
cnx = pymysql.connect(user='root', database='narnik', charset='utf8')
cursor = cnx.cursor()

query = ("INSERT INTO narnik.score108_bettingoffer (eventID, eventFK, eventType, eventName, eventTime"
		"homeResult, awayResult, home_odd, away_odd, under_odd, hdp, ou, active, is_live, n)"
		"VALUES %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" 
		"ON DUPLICATE KEY UPDATE active = 'yes';")

query2 = ("INSERT INTO narnik.bettingoffer (eventID, eventFK, eventType, eventName, eventTime" 
		  "homeResult, awayResult, home_odd, away_odd, under_odd, hdp, ou, active, is_live, n)"
		  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
		  #"ON DUPLICATE KEY UPDATE active = 'yes';"
		  )

query3 = ("INSERT INTO `bettingoffer` (`id`, `eventID`, `eventFK`, `eventType`, `eventName`, `evevntTime`, `homeResult`, `awayResult`, `home_odd`, `away_odd`, `over_odd`, `under_odd`, `hdp`, `ou`, `active`, `is_live`, `del`, `n`, `ut`)"
		  "VALUES (1,22039300,1,'SEA Games Malaysia 2017 - Basketball Womens','Myanmar (w)-sv-Philippines (w)','06:38','0','0',0.56,-0.8,NULL,0.6,'79.50','144.50','yes','yes','no',1,'2017-08-22 15:44:05');")

query5 = ("INSERT INTO `bettingoffer` (`id`, `eventID`, `eventFK`, `eventType`, `eventName`, `evevntTime`, `homeResult`, `awayResult`, `home_odd`, `away_odd`, `over_odd`, `under_odd`, `hdp`, `ou`, `active`, `is_live`, `del`, `n`, `ut`)"
		  "VALUES %s;")


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
						eventTime = datetime.datetime.utcnow().strftime("%H:%M")
						live = 'yes'

					elif firstSecond and runningTime:
						eventTime = datetime.time(
							int(firstSecond[:-1].strip()),
							int(runningTime[:-1].strip())
							).strftime("%H:%M")
					else:
						eventTime = datetime.datetime.utcnow().strftime("%H:%M")

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
							hdp = None
					else:
						hdp = None

					ou = text_balls[1]
					if ou:
						ou = ou.select('span[id*=out_ball__{}__{}__0__3]'.format(
							tr.get('id').split('__')[-3],
							tr.get('id').split('__')[-2])
						)
						if ou:
							ou = ou[0].get_text()
						if not ou:
							ou = None
					else: 
						ou = None 

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
							home_odd = None
						else:
							home_odd = float(home_odd)
					else: 
						home_odd = None 

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
							away_odd = None
						else:
							away_odd = float(away_odd)
					else: 
						away_odd = None 

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
							over_odd = None
						else:
							over_odd = float(over_odd)
					else: 
						over_odd = None 

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
							under_odd = None
						else:
							under_odd = float(under_odd)
					else: 
						under_odd = None 

				params = (
					eventID, 1, eventType, eventName, eventTime, homeResult, awayResult, 
					home_odd, away_odd, under_odd, hdp, ou, 'yes', live, 'no', 1, '2017-08-22 15:44:05'
					)
				print(params)
				query5 = ("INSERT INTO `bettingoffer` (`eventID`, `eventFK`, `eventType`, `eventName`, `evevntTime`, `homeResult`"
										"`awayResult`, `home_odd`, `away_odd`, `over_odd`, `under_odd`, `hdp`, `ou`, `active`" 
										"`is_live`, `del`, `n`, `ut`"
						  #"VALUES %s" % params)
						  "VALUES ({0}, {1}, '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}')".format(
						  	eventID, 1, eventType, eventName, eventTime, homeResult, awayResult, 
							home_odd, away_odd, under_odd, hdp, ou, 'yes', live, 'no', 1, '2017-08-22 15:44:05'
						  	))
				cursor.execute(query5)



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
	main()
