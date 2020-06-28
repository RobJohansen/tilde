#!/usr/bin/env python

from datetime import datetime
from imdb import IMDb

ia = IMDb()
default_infoset = ia.get_movie_infoset()

def get_movie(search):
    return ia.search_movie(search)

def get_split(results):
    return dict(map(lambda x: x.split("::"), results))

def get_split_key(results, key):
    return get_split(results)[key]

def to_date_time(date_string):
    return datetime.strptime(' '.join(date_string.split(' ')[:3]), '%d %B %Y')

def get_first_result_key(search, key):
    return ia.search_movie(search)[0][key]

def annotate_result_safe(result, infoset=default_infoset):
    for info in infoset:
        try:
            ia.update(result, info=[info])
        except:
            print("error: " + str(info))
            pass

def get_imdb_results(search):
    return ia.search_movie(search)

def get_imdb_result(search, index=0):
    return get_imdb_results(search)[index]

def get_imdb_limit(search, region='UK'):
    key = 'release dates'

    results = ia.search_movie(search)
    result = ia.get_movie(results[0].getID(), info=[key])

    return to_date_time(get_split_key(result[key], region))