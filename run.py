from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import datetime 
import os 
import time


url = "http://w2.kkkk99.net/"
login_url = "?r=1"
main_url = "main.php"

username = "x660s1573"
password = "aa123456"

browser = webdriver.Firefox()#PhantomJS()


def login():

	browser.get(url + login_url)
	
	#button = browser.find_element_by_xpath('//button[@id="signin-submit"]') 

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
	
	browser.get('http://49297922.w2.kkkk99.net/index.php/content/hdp/2')

	table_container = WebDriverWait(browser, 1000).until(
		EC.presence_of_element_located((By.XPATH, "//div[@id='mTableContainer']"))
	)

def parse_table():

	html = browser.page_source
	soup = BeautifulSoup(html, "html.parser")

	for tbody in soup.find(id='mTableContainer').findAll('tbody')[2:]:
		if tbody.find('th'):
			#print('SPORT: ' + str(tbody.find('th').get_text()))
			print(tbody.find('th').get_text())
		print(' | '.join([td.get_text() for td in tbody.findAll('td')]))
		#for td in tbody.findAll('td'):
		#	print('TD IS: ' + str(td.get_text()))





def main():
	
	login()

	close_popup()
	
	wait_table()

	while True:
		print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		parse_table()
		time.sleep(20)
	
	browser.quit()



if __name__ == '__main__':
	main()


