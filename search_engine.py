import random
import time
import os
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
from pathlib import Path


# id_subregionslinks = 'subregionslinks',
# subreg_tag = 'a',
# stepback_id = 'back_region_link'
def lang_source(url, find_by_id, class_langs, tag_langs):
	driver = webdriver.Firefox()
	url_local = Scrapping(url).url_in_use()
	driver.get(url_local)
	prime_source = driver.page_source
	prime_url = driver.current_url
	soup = BeautifulSoup(prime_source, 'lxml')
	langs = soup.find('div', class_=class_langs).find_all(tag_langs)
	source_name = ''
	source2_name = ''
	for lang in langs:
		try:
			if lang.find('a'):
				element_secondary = driver.find_element(By.LINK_TEXT, lang.text.strip())
				source2_name = f'{url.split(".")[-2]}_{lang.text.strip()}'
			else:
				source_name = f'{url.split(".")[-2]}_{lang.text.strip()}'
		except Exception as e:
			raise e

	print(prime_source)
	try:
		element_lang = driver.find_element(By.ID, find_by_id)
		ActionChains(driver).click(element_lang).perform()
		time.sleep(3)
		secondary_source = driver.page_source
		secondary_url = driver.current_url

	except Exception as e:
		raise e
	path1 = Scrapping(url).file_tree(file_name=source_name, extension_key='html')
	path2 = Scrapping(url).file_tree(file_name=source2_name, extension_key='html')
	with open(path1, 'w') as f:
		f.write(prime_source)
	with open(path2, 'w') as f:
		f.write(secondary_source)
	print(secondary_source, '\n', secondary_url, prime_url, source_name, source2_name)
	driver.quit()


# lang_source('olx.ua', find_by_id='changeLang', class_langs='lang-selector small', tag_langs='li')
def category(
		main_tag=None,
		sub_main_tag=None,
		main_id=None,
		main_class=None,
		sub_main_class=None,
		sub_tag=None,
		sub_id=None,
		sub_class=None):
	paths = ['olx/olx_язык.html', 'olx/olx_мова.html']
	path_to_ru = 'olx/olx_язык.html'
	path_to_ua = 'olx/olx_мова.html'
	for path_ in paths:
		file_name = f"langs_ru_ua_choose{path_.split('.')[-2].split('/')[-1].strip()}"
		dir_key = 'category'
		print(file_name)
		with open(path_, 'r') as f:
			file = f.read()
			soup = BeautifulSoup(file, 'lxml')
			# find categories
			categories_lists = soup.find_all(main_tag, class_=main_class)
			category_dict = {}
			for set_categories in categories_lists:
				categories = set_categories.find_all(sub_main_tag, class_=sub_main_class)
				for category_ in categories:
					category_name = category_.find('a').text.strip()
					category_link = category_.find('a').get('href').strip()
					category_dict[category_name] = {'link': category_link, 'name': category_name, 'subcategories': []}
			keys_list = list(category_dict.keys())
			for key in keys_list:
				value_source = category_dict.get(key)
				link = value_source.get('link')
				subcategories = soup.find_all(sub_tag, class_=sub_class)
				iterations = []
				for subcategory in subcategories:
					if subcategory.find('a'):
						subcategory_link = subcategory.find('a').get('href').strip()
						subcategory_name = subcategory.find('a').text.strip()
						if link.split('/')[-2] in subcategory_link:
							iterations.append(
								{'subcategory_name': subcategory_name, 'subcategory_link': subcategory_link})
							print(subcategory_name)
							print(subcategory_link)
						else:
							pass
						# value_source['subcategories'] = [{'subcategory_name': key}, {'subcategory_link': link}]
						value_source['subcategories'] = iterations
			Scrapping(url='olx.ua').json_write(source=category_dict, file_name=file_name, dir_key=dir_key)
			print(category_dict)


category(
	main_tag='div',
	main_class='maincategories',
	sub_main_tag='div',
	sub_main_class='item',
	sub_tag='li',
	sub_class='fleft'
)


def find_geo(url, input_id, regions_links, tag_regions):
	driver = webdriver.Firefox()
	url_local = Scrapping(url).url_in_use()
	driver.get(url=url_local)
	start = driver.find_element(By.ID, input_id)
	ActionChains(driver).click(start).perform()
	src_regions = driver.page_source
	# find elements regions
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


def collect_category(src_path):
	# parent = Path.root(src_path).parent
	path = src_path
	with open(path, 'r') as f:
		src = f.read()
		soup = BeautifulSoup(src, 'lxml')
		categories_list = soup.find('div', class_='maincategories').find_all('a', class_='link parent')
		categories = []
		for item in categories_list:
			categories.append(item.text.strip())
			print(item.text)
		print(categories)

# collect_category(src_path='olx/main_page.html')
# find_geo(input_id='cityField', regions_links='regionslinks', tag_regions='li', url='olx.ua')

# driver = webdriver.Firefox()
# driver.get(url='https://www.olx.ua')
# start = driver.find_element(By.ID, 'cityField')
# ActionChains(driver).click(start).perform()
# src_regions = driver.page_source
# ActionChains(driver).scroll_to_element()
