#!/usr/bin/env python

from datetime import datetime
from imdb import IMDb

ia = IMDb()

# constants

REGION = 'USA'

MAIN_KEY = 'main'
KIND_KEY = 'kind'
DATE_KEY = 'release dates'
SUB_ITEMS_KEY = 'episodes'

info_set = [MAIN_KEY, DATE_KEY, SUB_ITEMS_KEY]


# general helpers

def search_items(search):
    return ia.search_movie(search)

def get_item(id, keys=ia.get_movie_infoset()):
    return ia.get_movie(id, keys)

def update_item(result, key):
    ia.update(result, info=[key])


# imdb / node classes

'''
Node representing IMDB item.
'''
class ImdbNode:

    id = None
    kind = None
    name = None
    timestamp = None

    def __parse_keys(self, results):
        return dict(map(lambda x: x.split("::"), results))

    def __parse_key(self, results, key):
        return self.__parse_keys(results)[key]

    def __to_date_time(self, date_string):
        return datetime.strptime(' '.join(date_string.split(' ')[:3]), '%d %B %Y')

    def __get_id(self, item):
        return item.getID()

    def __get_kind(self, item):
        return item[KIND_KEY]

    def __get_name(self, item):
        return str(item)

    def __get_date(self, item):
        return self.__to_date_time(
            self.__parse_key(
                item[DATE_KEY],
                REGION
            )
        )

    def __init__(self, item):
        self.id = self.__get_id(item)
        self.kind = self.__get_kind(item)
        self.name = self.__get_name(item)
        self.timestamp = self.__get_date(item)

    def __repr__(self):
        return '<[{} {}] {}>'.format(
            self.kind,
            self.id,
            self.name,
        )

'''
Collection of nodes and subnodes.
'''
class ImdbItem:
    # results
    results = None
    result = None

    # items
    node = None
    sub_nodes = {}

    def __init__(self, search_term, search_index):
        # search
        self.results = search_items(search_term)
        self.result = self.results[search_index]

        # item
        item = get_item(self.result.getID(), info_set)
        sub_items = item[SUB_ITEMS_KEY]

        self.node = ImdbNode(item)

        print("retrieved item: " + str(self.node))

        # sub items
        for (s, sub_item_set) in sub_items.items():
            if (s > 1):
                continue

            self.sub_nodes[s] = {}

            for (i, sub_item) in sub_item_set.items():
                if (i > 5):
                    continue

                ia.update(sub_item, DATE_KEY)

                self.sub_nodes[s][i] = ImdbNode(sub_item)

                print("retrieved sub-item: " + str(self.sub_nodes[s][i]))

    def __repr__(self):
        return '<{} (sub: {})>'.format(
            self.node,
            len(self.sub_nodes)
        )
