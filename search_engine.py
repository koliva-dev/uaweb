import random
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager import chrome, firefox, microsoft
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from main_scrapper import Scrapping
import lxml

# id_subregionslinks = 'subregionslinks',
# subreg_tag = 'a',
# stepback_id = 'back_region_link'


def find_geo(url, input_id, regions_links, tag_regions):
	driver = webdriver.Firefox()
	url_local = Scrapping(url).url_in_use()
	driver.get(url=url_local)
	start = driver.find_element(By.ID, input_id)
	ActionChains(driver).click(start).perform()
	src_regions = driver.page_source
	# find elements regions
	regions_clicks = driver.find_element(By.ID, regions_links).find_elements(By.TAG_NAME, tag_regions)
	index = -1
	driver.quit()
	soup = BeautifulSoup(src_regions, 'lxml')
	regions = soup.find('noindex').find_all('a', class_='regionlink region_link')
	regions_list = []
	for i in regions:
		regions_list.append(i.text)
	print(len(regions_list), regions_list)
	regs_subregs = {}
	for i in range(len(regions_list)):
		driver = webdriver.Firefox()
		driver.get(url='https://www.olx.ua')
		start = driver.find_element(By.ID, input_id)
		ActionChains(driver).click(start).perform()
		regions_clicks = driver.find_element(By.ID, regions_links).find_elements(By.TAG_NAME, tag_regions)
		element = regions_clicks[i]
		ActionChains(driver).scroll_by_amount(delta_x=0, delta_y=120).perform()
		time.sleep(random.randrange(2, 3))
		ActionChains(driver).click(element).perform()
		subsource = driver.page_source
		soup = BeautifulSoup(subsource, 'lxml')
		try:
			subregions = soup.find('div', class_='table full subregionslinks').find_all('a')
			subregions_list = []
			for item in subregions:
				print(item.text)
				subregions_list.append(item.text)
				regs_subregs[regions_list[i]] = subregions_list
		except AttributeError:
			pass


		driver.quit()
		time.sleep(2)

	save = Scrapping(url)
	save.json_write(source=regs_subregs, file_name='olx_regions', dir_key='regions')


find_geo(input_id='cityField', regions_links='regionslinks', tag_regions='li', url='olx.ua')

# driver = webdriver.Firefox()
# driver.get(url='https://www.olx.ua')
# start = driver.find_element(By.ID, 'cityField')
# ActionChains(driver).click(start).perform()
# src_regions = driver.page_source
# ActionChains(driver).scroll_to_element()