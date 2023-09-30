import random
from time import sleep as pause
from pprint import pprint
from urllib.parse import urlparse
import bs4
from fake_useragent import UserAgent
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from multiprocessing import Pool


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

        self.chrome_options = chrome_options

    def process_link(self, link):
        with open('output.txt', 'a', encoding='utf-8') as output_file:
            try:
                # Создаем новый драйвер для каждого процесса
                driver = webdriver.Chrome(options=self.chrome_options)
                driver.set_page_load_timeout(10)
                driver.maximize_window()

                driver.get(link)
            except TimeoutException:
                print(f'Timeout for {link}')
                return

            page_source = driver.page_source
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

            output_file.write(f"Link: {link}\n")
            output_file.write(f"Description: {context_text[0]}\n")
            output_file.write(f"Keywords: {context_text[1]}\n")
            output_file.write(f"Title: {context_text[2]}\n")
            output_file.write(f"OG Title: {context_text[3]}\n\n")
            print(link, context_text)

            # Закрываем драйвер после завершения обработки страницы
            driver.quit()

    def step_metateg(self):
        with Pool(processes=4) as pool:  # Указать желаемое количество процессов
            pool.map(self.process_link, self.file)


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
