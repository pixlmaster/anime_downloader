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

#driver=webdriver.Firefox()
_browser_profile = webdriver.FirefoxProfile()
_browser_profile.set_preference("dom.webnotifications.enabled", False)
_browser_profile.set_preference("browser.download.folderList", 2)
_browser_profile.set_preference('browser.download.dir', '/Downloads')
_browser_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'video/mp4')
options = Options()
options.add_argument("--headless")
#driver=webdriver.Firefox(firefox_profile=_browser_profile)
driver=webdriver.Firefox(firefox_profile=_browser_profile,options=options)

driver.get("https://kissanime.ru/Login")
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID,"username")))
user=driver.find_element_by_id("username")
print(user)
user.send_keys("testkgp")
password=driver.find_element_by_id("password")
password.send_keys("qwertyuiop")
login_button=driver.find_element_by_id("btnSubmit")
login_button.click()


driver.get("https://kissanime.ru/")

WebDriverWait(driver, 30)

main_window=driver.current_window_handle

WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID,"keyword")))
WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.ID,"keyword")))
inputelement=driver.find_element_by_id("keyword")

inputelement.send_keys("boruto")

searchButton = driver.find_element_by_id("imgSearch")
searchButton.click()

while driver.current_url != "https://kissanime.ru/Search/Anime":
     ActionChains(driver).send_keys(Keys.CONTROL + 'w').perform()

driver.switch_to_window(main_window)

soup= bs(driver.page_source, 'html.parser')

table=soup.find('table')

links = table.find_all("a")
i=1
for link in links:
	anime="https://kissanime.ru"+link.get('href')
	title=(link.get_text()).strip()
	print(str(i) +". "+title)
	i+=1
print("Enter which you want to download?")
x= input()

url="https://kissanime.ru"+links[int(x)-1].get('href')

driver.get(url)

WebDriverWait(driver, 10)
driver.switch_to_window(main_window)

anime_soup= bs(driver.page_source, 'html.parser')
anime_table=anime_soup.find('table')

episodes = anime_table.find_all("a")
i=1
for episode in episodes:
	print(str(i)+"."+(episode.get_text()).strip())
	i+=1
print("enter serial no to download")
x= input()
x=int(x)

anime_url="https://kissanime.ru" + episodes[x-1].get('href')

driver.get(anime_url)
WebDriverWait(driver, 10)
driver.switch_to_window(main_window)

skip_button=driver.find_element_by_class_name('specialButton')

skip_button.click()
WebDriverWait(driver, 10)

download_soup=bs(driver.page_source, 'html.parser')

download_l=download_soup.find("div",{"id":"divDownload"})

download_link=download_l.find('a')
download_final=download_link['href']

driver.get(download_final)

final_soup=bs(driver.page_source, 'html.parser')

resolutions=final_soup.find_all(id="button-download")
i=1
for resolution in resolutions:
	print(str(i)+"."+(resolution.get_text()).strip())
	i+=1

print("enter resolution to download")
x=input()
x=int(x)

anime_link=resolutions[x-1].get('href')
driver.get(anime_link)
