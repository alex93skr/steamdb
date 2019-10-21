#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################
import pickle

from bs4 import BeautifulSoup
import json
import random
import threading
from pprint import pprint

import requests
from fake_headers import Headers

from bs4 import BeautifulSoup
import bs4

import re


#############################################################

def fake_head():
    # return Headers(headers=True).generate()
    return {'Accept': '*/*', 'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0.2) Gecko/20100101 Firefox/67.0.2',
            'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'Referer': 'https://google.com'}


class MyThread(threading.Thread):

    def __init__(self, id):
        self.id = id
        threading.Thread.__init__(self)

    def run(self):

        self.url = f'https://steamdb.info/app/{str(self.id)}/'
        # proxy1 = {'https': f'https://{random.choice(proxy_data)}'}

        while True:
            try:
                r = requests.get(self.url, headers=fake_head(), timeout=3)
                if r.ok:
                    self.html = r.text
                    self.parser()
                    print('ok:', self.id)
                    return
            except Exception as err:
                print('err:', self.id, err)
                return

    def parser(self):
        dPrint = False

        if dPrint: print(self.id)
        if dPrint: print(self.url)

        soup = BeautifulSoup(self.html, 'html.parser')

        try:
            applicationCategory = soup.find('td', {"itemprop": "applicationCategory"}).text
            if dPrint: print(applicationCategory)
            steamdb[self.id].update({'applicationCategory': applicationCategory})
        except Exception as err:
            print('err:', self.id, err)

        try:
            author = soup.find('span', {"itemprop": "author"}).text
            if dPrint: print(author)
            steamdb[self.id].update({'author': author})
        except Exception as err:
            print('err:', self.id, err)

        try:
            publisher = soup.find('span', {"itemprop": "publisher"}).text
            if dPrint: print(publisher)
            steamdb[self.id].update({'publisher': publisher})
        except Exception as err:
            print('err:', self.id, err)

        try:
            operatingSystem = soup.find('meta', {"itemprop": "operatingSystem"}).attrs['content']
            if dPrint: print(operatingSystem)
            steamdb[self.id].update({'operatingSystem': operatingSystem})
        except Exception as err:
            print('err:', self.id, err)

        try:
            dateModified = soup.find('span', {"itemprop": "dateModified"}).attrs['content']
            if dPrint: print(dateModified)
            steamdb[self.id].update({'dateModified': dateModified})
        except Exception as err:
            print('err:', self.id, err)

        try:
            datePublished = soup.find('span', {"itemprop": "datePublished"}).attrs['content']
            if dPrint: print(datePublished)
            steamdb[self.id].update({'datePublished': datePublished})
        except Exception as err:
            print('err:', self.id, err)

        try:
            categories_ = soup.find('div', {"class": "header-thing header-thing-full"})
            categories = []
            for i in categories_.children:
                if type(i) is bs4.element.Tag:
                    categories.append(i.attrs['aria-label'])
            if dPrint: print(categories)
            steamdb[self.id].update({'categories': categories})
        except Exception as err:
            print('err:', self.id, err)

        try:
            userTags_ = soup.find_all('a', {"class": "btn btn-sm btn-outline btn-tag"})
            userTags = []
            for i in userTags_:
                userTags.append(i.text)
            if dPrint: print(userTags)
            steamdb[self.id].update({'userTags': userTags})
        except Exception as err:
            print('err:', self.id, err)

        try:
            # metacritic_score = ''
            metacritic_score_ = soup.find('td', text=re.compile('metacritic_score'))
            if not metacritic_score_ is None:
                for i in metacritic_score_.next_elements:
                    if type(i) is bs4.element.Tag:
                        metacritic_score = i.text
                        break
                if dPrint: print(metacritic_score)
                steamdb[self.id].update({'metacritic_score': metacritic_score})
        except Exception as err:
            print('err:', self.id, err)


if __name__ == '__main__':

    with open('steamdb.pickle', 'rb') as f:
        steamdb = pickle.load(f)

    print(type(steamdb))
    print(len(steamdb))

    MAX_THREAD_COUNT = 30

    id_list = list(steamdb.keys())
    # id_list = list(steamdb.keys())[100:114]
    # id_list = [random.randint(100, 15000) for i in range(50)]
    # id_list = [10182]

    start = 0

    while start < len(id_list):
        print('START', start)
        threads = []
        for id in id_list[start:start + MAX_THREAD_COUNT]:
            # for id in id_list:
            # print(id)
            t = MyThread(id)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        start += MAX_THREAD_COUNT

    # for id in id_list:
    #     print(id)
    #     pprint(steamdb[id])
    #     print()

    with open('steamdb_full.pickle', 'wb') as f:
        pickle.dump(steamdb, f)




#############################################################
