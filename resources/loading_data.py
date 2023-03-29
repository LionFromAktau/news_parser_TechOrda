from datetime import datetime
from typing import List
import unicodedata
from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse

class LoadingData:

    def exclude_tag(self,my_dict: dict) -> dict:
        return {k: v for k, v in my_dict.items() if k != 'tag'}

    def loadData(self,top_tag: dict, bottom_tag: dict, title_cut: dict, date_cut: dict, url: str, res_id: int) -> \
    List[dict]:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        infoes = soup.findAll(top_tag['tag'], self.exclude_tag(top_tag))
        document = []
        for info in infoes[0:5]:
            link = info.find('a')['href']
            if url not in link:
                link = url + link
            date_text = info.find(date_cut['tag'], {self.exclude_tag(date_cut)})
            news_date = parse(date_text)
            news_unix_date = int(news_date.timestamp())
            title = info.find(title_cut['tag'], {self.exclude_tag(title_cut)}).text.strip()
            article = BeautifulSoup(requests.get(link).text, 'lxml').find(bottom_tag['tag'], self.exclude_tag(bottom_tag))
            content = unicodedata.normalize('NFKD', article.text).replace('\n', '')

            document.append({
                'res_id': res_id,
                'link': link,
                'news_date': news_date.date(),
                'news_unix_date': news_unix_date,
                'title': title,
                'content': content
            })
        return document

