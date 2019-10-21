#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle


data = {}

count = 0

with open('all.html', 'r', encoding='utf-8') as f:
    for line in f:

        if count == 1:
            n = line[4:-7]
        elif count == 2:
            id = line[line.find('/">') + 3:-10]
        elif count == 3:
            name = line[4:-6]
        elif count == 4:
            positive = int(line[23:-6].replace(',', ''))
        elif count == 5:
            negative = int(line[23:-6].replace(',', ''))
        elif count == 6:
            rating = float(line[23:-7])

        if count == 6:
            count = 0
            # print(n, '|', id, '|', name, '|',  positive, '|', negative, '|', rating)
            data.update({id: {'name': name, 'positive': positive, 'negative': negative, 'rating': rating}})
        else:
            count += 1

print(len(data))

with open('steamdb.pickle', 'wb') as f:
    pickle.dump(data, f)

            # n = soup.tbody('td')[i].text
            # id = soup.tbody('td')[i+1].text
            # name = soup.tbody('td')[i+2].text
            # positive = soup.tbody('td')[i+3].text
            # negative = soup.tbody('td')[i+4].text
            # rating = soup.tbody('td')[i+5].text

            # <tr class="app odd" data-appid="620" role="row">
            # <td>1.</td>
            # <td><a href="https://steamdb.info/app/620/">620</a></td>
            # <td>Portal 2</td>
            # <td class="text-right">154,556</td>
            # <td class="text-right">2,080</td>
            # <td class="text-right">97.34%</td>
            # </tr><tr class="app even" data-appid="427520" role="row">
            # <td>2.</td>
