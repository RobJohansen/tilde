#!/usr/bin/env python

from datetime import datetime
from imdb import IMDb

ia = IMDb()

DEFAULT_KEYS = ia.get_movie_infoset()

def search_items(search):
    return ia.search_movie(search)

def get_item(id, keys=DEFAULT_KEYS):
    return ia.get_movie(id, keys)

def update_item(result, key):
    ia.update(result, info=[key])

class ImdbItem:

    REGION = 'UK'
    RELEASE_DATE_KEY = 'release dates'
    KEYS = [RELEASE_DATE_KEY]

    results = None
    result_raw = None
    result_annotated = None
    result_attributes = None
    result_release_date = None

    def __get_attributes(self, result):
        for key in self.KEYS:
            try:
                update_item(result, key)

            except (Exception):
                print("key error: " + str(key))

        return { k: result.get(k) for k in result.current_info }

    def __parse_keys(self, results):
        return dict(map(lambda x: x.split("::"), results))

    def __parse_key(self, results, key):
        return self.__parse_keys(results)[key]

    def __to_date_time(self, date_string):
        return datetime.strptime(' '.join(date_string.split(' ')[:3]), '%d %B %Y')

    def __init__(self, search_term, search_index):
        self.results = search_items(search_term)

        self.result_raw = self.results[search_index]

        self.result_annotated = get_item(self.result_raw.getID(), self.KEYS)

        self.result_attributes = self.__get_attributes(self.result_raw)

        self.result_release_date = self.__to_date_time(
            self.__parse_key(
                self.result_attributes[self.RELEASE_DATE_KEY],
                self.REGION
            )
        )

    def __repr__(self):
        return '<Imdb {}>'.format(self.result_raw)
