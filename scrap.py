import os
from bs4 import BeautifulSoup as bs                              
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.firefox.options import Options
import requests

kissanime_login_url="https://kissanime.ru/Login"
kissanime_base_url="https://kissanime.ru"
kissanime_main_url=kissanime_base_url+"/"
kissanime_search_url=kissanime_main_url+"Search/Anime"
user_name="testkgp"
user_password="qwertyuiop"

def browser_init():
	_browser_profile = webdriver.FirefoxProfile()
	_browser_profile.set_preference("dom.webnotifications.enabled", False)
	_browser_profile.set_preference("browser.download.folderList", 2)
	_browser_profile.set_preference('browser.download.dir', '/Downloads')
	_browser_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'video/mp4')
	options = Options()
	options.add_argument("--headless")

	driver=webdriver.Firefox(firefox_profile=_browser_profile)
	#driver=webdriver.Firefox(firefox_profile=_browser_profile,options=options)

	return driver

def site_login(browser):
	browser.get(kissanime_login_url)
	WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID,"username")))
	
	user=browser.find_element_by_id("username")
	user.send_keys(user_name)
	
	password=browser.find_element_by_id("password")
	password.send_keys(user_password)
	
	login_button=browser.find_element_by_id("btnSubmit")
	login_button.click()

def site_search(browser):
	browser.get(kissanime_main_url)
	main_window=browser.current_window_handle

	WebDriverWait(browser,30).until(EC.presence_of_element_located((By.ID,"keyword")))
	#WebDriverWait(browser,30).until(EC.visibility_of_element_located((By.ID,"keyword")))
	
	inputelement=browser.find_element_by_id("keyword")
	inputelement.send_keys("boruto")

	searchButton = browser.find_element_by_id("imgSearch")
	searchButton.click()
	list = browser.window_handles
	for ad in list:
		browser.switch_to_window(ad)
		if ad!=main_window:
			browser.close()

	browser.switch_to_window(main_window)

	return browser,main_window

def search_result(browser):
	soup= bs(browser.page_source, 'html.parser')

	table=soup.find('table')

	links = table.find_all("a")
	i=1
	for link in links:
		anime=kissanime_base_url+link.get('href')
		title=(link.get_text()).strip()
		print(str(i) +". "+title)
		i+=1
	print("Enter which you want to download?")
	x= input()

	url=kissanime_base_url+links[int(x)-1].get('href')

	browser.get(url)
	WebDriverWait(browser, 5)

	browser.switch_to_window(main_window)
	return browser

def episode_result(browser):
	anime_soup= bs(browser.page_source, 'html.parser')
	anime_table=anime_soup.find('table')

	episodes = anime_table.find_all("a")
	i=1
	for episode in episodes:
		print(str(i)+"."+(episode.get_text()).strip())
		i+=1
	print("enter serial no to download")
	x= input()
	x=int(x)

	anime_url=kissanime_base_url + episodes[x-1].get('href')

	browser.get(anime_url)
	WebDriverWait(browser, 5)
	browser.switch_to_window(main_window)
	return browser

def skip(browser):
	skip_button=browser.find_element_by_class_name('specialButton')

	skip_button.click()
	WebDriverWait(browser, 5)

	return browser

def anime_page(browser):
	download_soup=bs(browser.page_source, 'html.parser')

	download_l=download_soup.find("div",{"id":"divDownload"})

	download_link=download_l.find('a')
	download_final=download_link['href']

	return browser, download_final

def download_page(browser):
	browser.get(download_final)

	final_soup=bs(browser.page_source, 'html.parser')

	resolutions=final_soup.find_all(id="button-download")
	i=1
	for resolution in resolutions:
		print(str(i)+"."+(resolution.get_text()).strip())
		i+=1

	print("enter resolution to download")
	x=input()
	x=int(x)

	anime_link=resolutions[x-1].get('href')
	browser.get(anime_link)

driver=browser_init()

try:
	site_login(driver)

	driver,main_window=site_search(driver)

	driver=search_result(driver)

	driver=episode_result(driver)

	driver=skip(driver)

	driver,download_final=anime_page(driver)

	driver=download_page(driver)

except Exception as e:
	print("an error occurred")
	print(e)
finally:
	driver.quit()




