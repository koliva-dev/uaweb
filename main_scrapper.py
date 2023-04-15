import asyncio
import time
import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pathlib import Path
import random


def headers_useragent():
	ua = UserAgent()
	headers = {
		'User-Agent': ua.random
	}
	return headers


class Scrapping:
	"""scrapping data from websites lib"""

	def __init__(self, url: str ):
		self.url = url
		self.extension = {
			'json': '.json',
			'py': '.py',
			'js': '.js',
			'xml': '.xml',
			'html': '.html',
			'csv': '.csv'
		}
		self.dir_name = {
			'regions': 'list_regions',
			'category': 'list_categories',
			'results': 'collected_data',
		}

	def url_in_use(self):
		url = f'https://www.{self.url}'
		return url

	def file_tree(self, file_name, extension_key, dir_key=None):
		"""
		start_source_name defined in body script as dir to source folder to store files
		and dirs of dir-tree
		:param extension_key: file to save in extension akin
				'json':'.json',
				'py':'.py',
				'js':'.js',
				'xml':'.xml',
				'html':'.html',
				'csv':'.csv'
		:param dir_key: establishing dir_names in list {
				regions: 'list_regions',
				category: 'list_categories',
				results: 'collected_data',
			}
		if dir_name no need (defining source) --> set dir_name = None
		:param file_name: return filename with extension as needed
		:return: dirs - tree
		"""
		start_source_name = self.url.split('.')[-2]
		if dir_key is None:
			file_name = f"{file_name}{self.extension[extension_key]}"
			path = Path(f'{start_source_name}/{file_name}')
			path.parent.mkdir(parents=True, exist_ok=True)
			print(path)
			return path

		else:
			path = Path(f'{start_source_name}/{self.dir_name[dir_key]}/{file_name}{self.extension[extension_key]}')
			path.parent.mkdir(parents=True, exist_ok=True)
			print(path)
			return path

	def json_write(self, source: dict, file_name, dir_key, extension_key=None):
		"""

		:param source: source dict to write
		:param file_name: file to write
		:param dir_key: folder as {
				regions: 'list_regions',
				category: 'list_categories',
				results: 'collected_data',
			}, where keys == args
		:param extension_key:
		:return:
		"""
		if extension_key is None:
			extension_key = 'json'
		path = self.file_tree(
			file_name=file_name,
			extension_key=extension_key,
			dir_key=dir_key)

		with open(path, 'w+') as f:
			json.dump(source, f, indent=4, ensure_ascii=False)

	def main_p_source(self):
		response = requests.get(self.url_in_use()).text
		path = self.file_tree(file_name='main_page', extension_key='html')
		with open(path, 'w+') as f:
			f.write(response)

		return path
