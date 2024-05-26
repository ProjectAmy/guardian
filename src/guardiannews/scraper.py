import json
import requests
import os

from datetime import datetime
from typing import Any
from bs4 import BeautifulSoup
from rich import print


# url = "https://www.theguardian.com/ |artanddesign |/2024/apr/24/|
# claudette-johnson-art-cotton-capital-nominated-for-turner-prize"


class GuardianSpider(object):
    def __init__(self):
        self.base_url: str = "https://www.theguardian.com/"  # tambah / baru bisa
        # self.category: Optional[str] = category
        self.date: str = datetime.now().strftime("/%Y/%b/%d/")
        # self.subcategory: Optional[str] = subcategory
        self.header = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/123.0.0.0 Safari/537.36")

    def get_response(self, url: str) -> BeautifulSoup:
        headers: dict[str, Any] = {
            "User-Agent": self.header
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

    # membuat method baru agar lebih efisien
    def make_soup(self, link):
        soup = self.get_response(os.path.join(self.base_url, link))
        return soup

    # membuat file json
    def make_json(self, filename, jsonfile):
        filename += '.json'
        with open(filename, 'w') as json_file:
            json.dump(jsonfile, json_file)

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
        # print("Generate URL")
        # with open('categories.json', 'w') as json_file:
        #     json.dump(categories, json_file)

        return categories

    def get_news_by_category(self, soup: BeautifulSoup):
        news_by_category = []
        articles = soup.find('main', attrs={'data-layout': 'FrontLayout'}).find_all('li')

        # iterasi
        for article in articles:
            title = article.find("span", attrs={"class": "show-underline"})
            link = article.find("a")

            # dicek karena ada li yang kosong
            if title and link:
                news = {
                    'title': title.text.strip(),
                    'news link': link.get("href")
                }
                news_by_category.append(news)

        return news_by_category

    def get_news_by_subcategory(self):
        pass

    def get_spesific_news(self):
        pass
