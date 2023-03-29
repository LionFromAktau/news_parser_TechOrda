from django.shortcuts import render
from typing import List
import unicodedata
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from dateutil.parser import parse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from . import models,serializers
# from loading_data import LoadingData

class ResourceViewSet(ModelViewSet):
    serializer_class = serializers.ResourceSerializer
    queryset = models.Resource.objects.prefetch_related().all()

class ItemViewSet(ModelViewSet):
    serializer_class = serializers.ItemSerializer
    queryset = models.Items.objects.select_related().all()

    def exclude_tag(self, my_dict: dict) -> dict:
        return {k: v for k, v in my_dict.items() if k != 'tag'}

    def loadData(self, top_tag: dict, bottom_tag: dict, title_cut: dict, date_cut: dict, url: str, name: str) -> \
            List[dict]:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        infoes = soup.findAll(top_tag['tag'], self.exclude_tag(top_tag))
        document = []
        for info in infoes[0:5]:
            link = info.find('a')['href']
            if name.lower() not in link:
                link = url + link
            date_text = info.find(date_cut['tag'])['datetime']
            news_date = str(parse(date_text).date())
            news_unix_date = int(parse(date_text).timestamp())
            # print(added_unix_date)
            title = info.find(title_cut['tag'], self.exclude_tag(title_cut)).text.strip()
            print(link)
            article = BeautifulSoup(requests.get(link).text, 'lxml').find(bottom_tag['tag'],
                                                                          self.exclude_tag(bottom_tag))
            content = unicodedata.normalize('NFKD', article.text).replace('\n', '')

            document.append({
                'link': link,
                'news_date': news_date,
                'news_unix_date': news_unix_date,
                'title': title,
                'content': content
            })
        return document

    def create(self, request, *args, **kwargs):
        serializer = serializers.ItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resource = models.Resource.objects.get(RESOURCE_NAME=serializer.validated_data['resource_name'])
        items = self.loadData(top_tag=resource.top_tag,bottom_tag=resource.bottom_tag,title_cut=resource.title_cut, date_cut=resource.date_cut, url=resource.RESOURCE_URL, name=resource.RESOURCE_NAME)
        models.Items.objects.bulk_create(
            [models.Items(res_id=resource, link=i['link'], title=i['title'], content=i['content'], news_unix_date=i['news_unix_date'], news_date=i['news_date']) for i in items]
        )
        return Response({'message': 'created'}, status=status.HTTP_201_CREATED)
