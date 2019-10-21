#!/usr/bin/python
# -*- coding: utf-8 -*-
#############################################################
#
# - STEAMDB
# - by skr
#
#############################################################
import os
import pickle
import time
from pprint import pprint

from flask import Flask, render_template, request

app = Flask(__name__, template_folder='', static_folder='')


#############################################################

def load_pickle(url):
    with open(url, "rb") as read_file:
        return pickle.load(read_file)


def key_arr_stat(inkey, outkey):
    alltags = {}

    for id in steamdb:
        cat = steamdb[id].get(inkey)
        if not cat is None:
            for c_sub in cat:
                if not c_sub in alltags:
                    alltags.update({c_sub: 1})
                else:
                    alltags[c_sub] += 1

    appdata[outkey] = alltags


def key_stat(key):
    arr = {}

    for id in steamdb:
        key_v = steamdb[id].get(key)
        if not key_v is None:
            if key_v in arr:
                arr[key_v] += 1
            else:
                arr.update({key_v: 1})

    appdata.update({key: arr})


def years_stat():
    arr = []

    for id in steamdb:
        datePublished = steamdb[id].get('datePublished')
        if (datePublished is not None):
            datePublished = datePublished[0:4]
            if datePublished in arr:
                pass
            else:
                arr.append(datePublished)

    appdata['arg']['years'] = sorted(arr, reverse=True)


def data_preparation():
    years_stat()
    key_arr_stat('userTags', 'tag_dict')

    for n in sorted(list(appdata['tag_dict'].items()), key=lambda i: i[1], reverse=True):
        appdata['arg']['tag'].append([n[0], n[1]])

    # key_arr_stat('categories')
    # key_arr_stat('userTags')

    # key_stat('applicationCategory')
    # key_stat('author')
    # key_stat('operatingSystem')
    # key_stat('publisher')


def searcher():
    def check(key):
        if key == 'logo':
            return True
        elif key == 'years':
            datePublished = steamdb[id].get('datePublished')
            if (datePublished is not None) and (appdata['request'][key] in datePublished):
                return True
        elif key == 'rating':
            rating = steamdb[id].get('rating')
            if (rating is not None) and (rating >= int(appdata['request']['rating'])):
                return True
        elif key == 'votes':
            positive = steamdb[id].get('positive')
            negative = steamdb[id].get('negative')
            if (positive is not None) and (negative is not None) and (
                    positive + negative >= int(appdata['request']['votes'])):
                return True
        elif key == 'tag':
            userTags = steamdb[id].get('userTags')
            if all(tag in userTags for tag in appdata['request']['tag']):
                return True

        return False

    # need_to_check = []
    #
    # for key in appdata['request']:
    #     if (appdata['request'][key] is not None):
    #         need_to_check.append(key)

    if appdata['request'] == {}: return

    # print(need_to_check)

    for id in steamdb:
        if all(check(key) for key in appdata['request']):
            appdata['result'].append(id)

    # print('searcher')
    # pprint(appdata['request'])
    # print(len(appdata['result']))
    # pprint(appdata['result'])


#############################################################


@app.route('/', methods=['GET'])
def index():
    appdata['request'] = {}
    appdata['result'] = []

    for key, val in request.args.lists():
        if key in appdata['arg'] and val[0] in appdata['arg'][key]:
            appdata['request'][key] = val[0]
        if key == 'tag':
            for i in val:
                if i in appdata['tag_dict']:
                    if appdata['request'].get('tag') == None:
                        appdata['request'].update({'tag': []})
                    appdata['request']['tag'].append(i)

    pprint(appdata['request'])

    # print(request.args)
    # print(request.args.keys())
    # print(request.args.lists())
    # print(request.args.listvalues())

    searcher()

    return render_template('steamdb_skr.html', steamdb=steamdb, appdata=appdata, len=len(appdata['result']))


#############################################################

if __name__ == "__main__":
    steamdb = load_pickle('steamdb_full.pickle')

    appdata = {
        'arg': {
            'years': [],
            'rating': ['90', '80', '70', '50', '30'],
            'votes': ['50000', '20000', '5000', '1000', '100'],
            'tag': [],
            'logo': ['on']
        },
        'tag_dict': {},
        'request': {},
        'result': []
    }

    data_preparation()

    # pprint(appdata)

    if "HEROKU" in list(os.environ.keys()):
        app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
    else:
        # app.run()
        app.run(debug=True)

#############################################################
