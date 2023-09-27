from pprint import pprint
from urllib.parse import urlparse

import bs4
import requests
from fake_useragent import UserAgent


class Main():
    def __init__(self, sign):
        self.base_url = 'https://yandex.ru/search/?text='
        self.sign = sign
        ua = UserAgent()
        self.headers = {
            'user-agent': ua.random
        }

    def start_polling(self):

        data = requests.get(f"https://yandex.ru/search/?text={self.sign}", headers=self.headers)
        soup = bs4.BeautifulSoup(data.text, 'html.parser')

        li_tegs = soup.findAll('a', target='_blank')
        target_blank_links = []
        for link in li_tegs:
            if 'href' in link.attrs:
                target_blank_links.append(link['href'])
        pprint(target_blank_links)
        self.step_metateg(target_blank_links)

    def step_metateg(self, target_blank):
        lst = ['some.ru', 'some', 'market.yandex.ru', 'pokupki.market.yandex.ru']
        link_dct = {}
        black_list_url = []
        for link in target_blank:
            print(link)
            # это как и сверху наработки на проверку доменов лишних, таких как яндекс маркет
            # domain = link.split("//")[-1].split("/")[0]
            parsed_url = urlparse(link)

            new_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            if new_url in black_list_url:
                continue
            try:
                hreff = requests.get(link, headers=self.headers)
                soup = bs4.BeautifulSoup(hreff.text, 'html.parser')
                meta_tag = soup.find('meta', attrs={'name': 'description'})
                content_text = meta_tag.get('content')
                link_dct[content_text] = link
                pprint(link_dct)
            except:
                print('bad link')
            black_list_url.append(new_url)



if __name__ == '__main__':
    sign = 'автошины'
    IMain = Main(sign)
    IMain.start_polling()



