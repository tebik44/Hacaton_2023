import random
from time import sleep as pause
from pprint import pprint
from urllib.parse import urlparse

import bs4
import pkg_resources
import requests
from fake_useragent import UserAgent
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException




class Main():
    def __init__(self, proxy, file):
        self.base_url = 'https://yandex.ru/search/?text='
        self.proxy = proxy
        self.file = file
        ua = UserAgent()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument(f'--user-agent={ua.random}')
        chrome_options.add_argument('--lang=ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7')

        # chrome_options.add_argument(f'--proxy-server=http://185.162.231.128:80')
        # chrome_options.add_argument(f'--utm_source=chrome.com')
        # with Chrome(service=Service(ChromeDriverManager(driver_version='117.0.5938.132').install()), options=chrome_options) as self.driver:
        #     self.driver.maximize_window()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(1)  # Здесь установлено время в 30 секунд, вы можете установить другое
        self.driver.maximize_window()

    def step_metateg(self):
        link_dct = {}
        test_lst = ['https://ru.wikipedia.org/wiki/Заглавная_страница']
        for link in self.file:
            print(link)
            try:
                self.driver.get(link)
                # pause(random.uniform(0.24, 3))
                pause(0.23)
            except:
                print('bad link')
            # trarajk = self.driver.page_source
            # description = self.driver.find_element(By.NAME, 'description').get_attribute('content')
            # title = self.driver.find_element_by_tag_name('title').text
            page_source = self.driver.page_source
            soup = bs4.BeautifulSoup(page_source, 'html.parser')
            meta_tag1 = soup.find('meta', attrs={'name': 'description'})
            meta_tag2 = soup.find('meta', attrs={'name': 'keywords'})
            meta_tag3 = soup.find('title')
            meta_tag4 = soup.find('meta', attrs={'property': 'og:title'})
            context_text = [
                meta_tag1.get('content') if meta_tag1 else None,
                meta_tag2.get('content') if meta_tag2 else None,
                meta_tag3.get_text() if meta_tag3 else None,
                meta_tag4.get('content') if meta_tag4 else None
            ]

            link_dct[link] = context_text
            pprint(link_dct[link])
            with open('output.txt', 'a', encoding='utf-8') as output_file:
                output_file.write(f"Link: {link}\n")
                output_file.write(f"Description: {context_text[0]}\n")
                output_file.write(f"Keywords: {context_text[1]}\n")
                output_file.write(f"Title: {context_text[2]}\n")
                output_file.write(f"OG Title: {context_text[3]}\n\n")


if __name__ == '__main__':
    lines_proxy = []
    lines_url = []
    with open('proxy.txt', 'r', encoding='utf-8') as proxy:
        for line in proxy:
            lines_proxy.append(line.strip())

    with open('link_list.csv', 'r', encoding='utf-8') as file:
        for line in file:
            lines_url.append(line.strip())

    IMain = Main(lines_proxy, lines_url)
    IMain.step_metateg()



