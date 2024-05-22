import json
import requests

from datetime import datetime
from typing import Any
from bs4 import BeautifulSoup
from rich import print


# url = "https://www.theguardian.com/ |artanddesign |/2024/apr/24/|  claudette-johnson-art-cotton-capital-nominated-for-turner-prize"


class GuardianSpider(object):
    def __init__(self):
        self.base_url: str = "https://www.theguardian.com/"  # tambah / baru bisa. Mengapa tidak langsung tambah internasional?
        # self.category: Optional[str] = category
        self.date: str = datetime.now().strftime("/%Y/%b/%d/")
        # self.subcategory: Optional[str] = subcategory

    def get_response(self, url: str) -> BeautifulSoup:
        headers: dict[str, Any] = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }

        res = requests.get(url=url, headers=headers)
        print("Site Status Code: ", res.status_code)

        #  response checking
        # f = open("response.html", 'w+')
        # f.write(res.text)
        # f.close()
        # Menambah encoding utf-8
        with open("response.html", "w", encoding="utf-8") as f:
            f.write(res.text)
            f.close()

        # scrape process
        soup: BeautifulSoup = BeautifulSoup(res.text, "html.parser")

        return soup

    def get_latest_news(self, soup: BeautifulSoup):
        # res = requests.get(os.path.join(self.base_url, "international"), headers=headers)

        contents = soup.find("div", attrs={"id": "container-headlines"}).find_all("li")
        for content in contents:
            title: str = content.find("span", attrs={"class": "show-underline"}).text.strip()
            print(title)

    def get_category(self, soup: BeautifulSoup):
        categories: list[dict[str, str]] = []
        navbar = soup.find('div', attrs={'data-component': 'nav2'})

        # get pillar list
        pillars = navbar.find('ul', attrs={'data-testid': 'pillar-list'}).find_all('a')
        for pillar in pillars:
            link = pillar.get('href')
            category = pillar.text

            data_pillar: dict[str, str] = {
                "link": link,
                "category": category
            }
            categories.append(data_pillar)

        menubar = navbar.find('ul', attrs={'role': 'menubar'}).find_all('a')
        for menu in menubar:
            data_menubar: dict[str, str] = {
                'link': menu.get('href'),
                'category': menu.text
            }
            categories.append(data_menubar)

        # return hasil
        print("Generate URL")
        with open('categories.json', 'w') as json_file:
            json.dump(categories, json_file)

        return categories

    def get_spesific_news(self):
        pass

    def get_news_by_category(self):
        pass

    def get_news_by_category_opinion(self, soup: BeautifulSoup):
        news_opinion = []
        opinions = soup.find('div', attrs={'id': 'container-opinion'}).find_all('li')

        # iterasi
        for opinion in opinions:
            news = {
                'title': opinion.find("span", attrs={"class": "show-underline"}).text.strip(),
                'news link': opinion.find("a").get("href")
            }
            news_opinion.append(news)

        # hasil
        with open('news_opinion.json', 'w') as json_file:
            json.dump(news_opinion, json_file)

    def get_news_by_subcategory(self):
        pass
