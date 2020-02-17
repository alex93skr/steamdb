#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################
import pickle
from tabulate import tabulate

import requests
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


def load_pickle(url):
    with open(url, "rb") as read_file:
        return pickle.load(read_file)


header = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

<title>steam sorter</title>

<style>
body {
 background-color: #0E202D;
 font-family: "Lucida Grande", Sans-Serif;
 font-size: 22px;
 color: white;
}

A:link,
A:visited,
A:active {
	color: white;
	text-decoration: none;
}

A:hover {
	color: white;
	text-decoration: underline;
}

.table_sort table {
  border-spacing: 0px;
  border-collapse: collapse;
  background: black;

}

.table_sort th {
    color: #ffebcd;
    background: #25567B;
    cursor: pointer;
}

.table_sort td,
.table_sort th {
	padding: 7px;
	padding-right: 20px;
	padding-left: 20px;
	font-family: "Lucida Grande", Sans-Serif;
	font-size: 13px;
}

.table_sort tbody tr:nth-child(odd) {
  background: #2A3A45
}

.table_sort tbody tr:nth-child(even) {
  background: #252D34
}


th.sorted[data-order="1"],
th.sorted[data-order="-1"] {
    position: relative;
}

th.sorted[data-order="1"]::after,
th.sorted[data-order="-1"]::after {
    right: 8px;
    position: absolute;
}

th.sorted[data-order="-1"]::after {
	content: "▼"
}

th.sorted[data-order="1"]::after {
	content: "▲"
}
</style>
	
<script type="text/javascript">
document.addEventListener('DOMContentLoaded', () => {

    const getSort = ({ target }) => {
        const order = (target.dataset.order = -(target.dataset.order || -1));
        const index = [...target.parentNode.cells].indexOf(target);
        const collator = new Intl.Collator(['en', 'ru'], { numeric: true });
        const comparator = (index, order) => (a, b) => order * collator.compare(
            a.children[index].innerHTML,
            b.children[index].innerHTML
        );
        
        for(const tBody of target.closest('table').tBodies)
            tBody.append(...[...tBody.rows].sort(comparator(index, order)));

        for(const cell of target.parentNode.cells)
            cell.classList.toggle('sorted', cell === target);
    };
    
    document.querySelectorAll('.table_sort thead').forEach(tableTH => tableTH.addEventListener('click', () => getSort(event)));
    
});
</script>

</head>

<center>
'''


# все категории
# все таги
#
# рейтинг по годам
# metacritic
# больше всего отзывов
# самые негативные ??
# статистика по годам
# средний рейтинг игр по годам

class Analyst:
    def __init__(self):
        file_html = open('steamdb_report.html', 'w', encoding='utf-8')

        file_html.write(header)

        file_html.write('<br>2019')
        out = self.print_sort_by_years()
        file_html.write(out.replace('<table>', '<table class="table_sort">'))

        file_html.close()

        import os
        myCmd = 'explorer D:\\code\\steamdb\\steamdb_report.html'
        os.system(myCmd)

    def print_sort_by_years(self):
        arr = []

        for id in steamdb:
            datePublished = steamdb[id].get('datePublished')
            if (not datePublished is None) and ('2019' in datePublished):
                metacritic_score = steamdb[id]['metacritic_score'] if not steamdb[id].get(
                    'metacritic_score') is None else ''

                # print(datePublished)

                url = f'<a href="https://store.steampowered.com/app/{id}' \
                      f'/" target="_blank">{steamdb[id]["name"][:40]}</a>'

                arr.append([
                    id,
                    f'<img src="https://steamcdn-a.akamaihd.net/steam/apps/{id}/capsule_sm_120.jpg">',
                    url,
                    steamdb[id]['rating'],
                    steamdb[id]['positive'] + steamdb[id]['negative'],
                    metacritic_score
                ])

        thead = ['id', '', 'name', 'rating', 'votes', 'metacritic']

        return tabulate(
            arr,
            thead,
            colalign=('left', 'left', 'left', 'right', 'right', 'right'),
            tablefmt="html"
        )

    def print_sort1(self):
        arr = []

        return tabulate(
            sorted(arr, key=lambda i: i[1], reverse=True)[:1000],
            # sorted(arr, key=lambda bids: bids[3], reverse=True)[:200],
            # arr,
            # header,
            # colalign=('left', 'left', 'center', 'right', 'right', 'right', 'right'),
            tablefmt="html"
            # tablefmt="simple"
        )


class Graphic:

    def __init__(self):
        # self.graphic_count_of_all_ah()
        self.by_years()
        # self.graphic_central_tendency()

    def by_years(self):
        import matplotlib.pyplot as plt

        for id in steamdb:
            datePublished = steamdb[id].get('datePublished')
            if (not datePublished is None) and ('2019' in datePublished):
                pass


def key_arr_stat(key):
    alltags = {}

    for id in steamdb:
        cat = steamdb[id].get(key)
        if not cat is None:
            for c_sub in cat:
                if not c_sub in alltags:
                    alltags.update({c_sub: 1})
                else:
                    alltags[c_sub] += 1

    print(len(alltags))

    print(tabulate(sorted(list(alltags.items()), key=lambda i: i[1], reverse=True)))


def key_stat(key):
    arr = {}

    for id in steamdb:
        key_v = steamdb[id].get(key)
        if not key_v is None:
            if key_v in arr:
                arr[key_v] += 1
            else:
                arr.update({key_v: 1})

    print('total in arr:', len(arr))

    print(tabulate(sorted(list(arr.items()), key=lambda i: i[1], reverse=True)[:100]))


def metacritic_score():
    for id in steamdb:
        metacritic = steamdb[id].get('metacritic_score')
        if (not metacritic is None) and (int(metacritic) > 91):
            print(metacritic, steamdb[id]['name'], f'https://steamdb.info/app/{id}/')


def sort_by_years():
    arr = []

    for id in steamdb:
        datePublished = steamdb[id].get('datePublished')
        if (not datePublished is None) and ('2019' in datePublished):
            # print(datePublished)
            arr.append([
                id,
                steamdb[id]['name'][:20],
                steamdb[id]['rating'],
                steamdb[id]['positive'] + steamdb[id]['negative'],
                f'https://steamdb.info/app/{id}/'
            ])
    # pprint(arr)
    print(tabulate(sorted(arr, key=lambda i: i[2], reverse=True)[:100]))


def stat_by_datePublished():
    arr = {}

    for id in steamdb:
        datePublished = steamdb[id].get('datePublished')
        if (not datePublished is None):
            datePublished = datePublished[0:4]

            if datePublished == '2020':
                continue

            rait = steamdb[id]['positive'] + steamdb[id]['negative']

            # print(datePublished)
            if datePublished in arr:
                arr[datePublished][0] += 1
                arr[datePublished][1] += steamdb[id]['positive']
                arr[datePublished][2] += steamdb[id]['negative']
                arr[datePublished][3] += rait

            else:
                arr.update({datePublished: [1, steamdb[id]['positive'], steamdb[id]['negative'], rait]})

    pprint(arr)


def finder():
    arr = []

    for id in steamdb:
        datePublished = steamdb[id].get('datePublished')
        if (datePublished is not None):
            datePublished = datePublished[0:4]

            # if datePublished == '2017' and 'Racing' in steamdb[id]['userTags']:
            if 'Old School' in steamdb[id]['userTags']:
                # print(id, steamdb[id]['name'], steamdb[id]['rating'], f'https://store.steampowered.com/app/{id}')

                arr.append([
                    # id,
                    steamdb[id]['name'],
                    steamdb[id]['rating'],
                    f'https://store.steampowered.com/app/{id}'
                ])

    # pprint(arr)
    print(tabulate(sorted(arr, key=lambda i: i[1], reverse=True)))
    # print(tabulate(arr))


def range_of_ratings():
    def rounding(n):
        if 0 <= n < 10: return 0
        if 10 <= n < 20: return 1
        if 20 <= n < 30: return 2
        if 30 <= n < 40: return 3
        if 40 <= n < 50: return 4
        if 50 <= n < 60: return 5
        if 60 <= n < 70: return 6
        if 70 <= n < 80: return 7
        if 80 <= n < 90: return 8
        if 90 <= n < 100: return 9

    arr = {}
    for id in steamdb:

        datePublished = steamdb[id].get('datePublished')
        rating = steamdb[id].get('rating')
        negative = steamdb[id].get('negative', 0)
        positive = steamdb[id].get('positive', 0)
        if (rating is not None) and (negative + positive > 100) and ('Multiplayer' in steamdb[id]['userTags']):
            # if (rating is not None) and (negative + positive > 100):
            # if (rating is not None) and (datePublished is not None) \
            #             and (datePublished[0:4] == '2019') and (negative + positive < 10):
            # if (rating is not None):
            # rounding_rating = rounding(rating)
            rounding_rating = round(rating)
            if rounding_rating not in arr:
                arr.update({rounding_rating: 1})
            else:
                arr[rounding_rating] += 1
    # pprint(arr)
    print(arr)
    print('total:', sum(arr.values()))

    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker

    # fig, axs = plt.subplots(2, 1)
    # gr = axs[0].bar(arr.keys(), arr.values())
    # gr2 = axs[1].bar(arr2.keys(), arr2.values())

    fig, ax = plt.subplots()

    gr = plt.bar(arr.keys(), arr.values())

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            # print(rect, height)
            plt.annotate('{}'.format(height),
                         xy=(rect.get_x() + rect.get_width() / 2, height),
                         xytext=(0, 0),  # 3 points vertical offset
                         textcoords="offset points",
                         ha='center', va='bottom')

    # plt.xlabel('value')
    # plt.ylabel('date')

    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

    autolabel(gr)

    plt.grid(True, linestyle='--', which='major',
             color='grey', alpha=.25)

    # plt.suptitle('Categorical Plotting')
    plt.show()


def avr_tags_ratings():

    arr = {}
    for id in steamdb:

        # datePublished = steamdb[id].get('datePublished')
        rating = steamdb[id].get('rating')
        negative = steamdb[id].get('negative', 0)
        positive = steamdb[id].get('positive', 0)
        if (rating is not None) and (negative + positive > 10):
            rounding_rating = round(rating)

def main():
    # pprint(steamdb)

    # print(len(steamdb))

    # key_arr_stat('categories')
    # key_arr_stat('userTags')
    # key_stat('operatingSystem')
    # metacritic_score()
    # stat_by_datePublished()

    # sort_by_years()

    # finder()

    range_of_ratings()

    # avr_tags_ratings()

    # запуск
    # Analyst()


#############################################################

if __name__ == '__main__':
    steamdb = load_pickle('steamdb_full.pickle')

    main()

#############################################################
