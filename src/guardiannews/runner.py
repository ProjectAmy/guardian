# use for run program
import os
import json

from .scraper import GuardianSpider


class Run(object):
    def __init__(self):
        self.spider: GuardianSpider = GuardianSpider()

    def scrape_category(self):
        soup = self.spider.get_response(os.path.join(self.spider.base_url, "international"))
        categories = self.spider.get_category(soup)
        print(categories)

    def scrape_by_category_opinion(self):
        soup = self.spider.get_response(os.path.join(self.spider.base_url, "uk/commentisfree"))
        by_category = self.spider.get_news_by_category(soup)

        # hasil
        with open('news_by_category_opinion.json', 'w') as json_file:
            json.dump(by_category, json_file)

        print(by_category)

