#!/usr/bin/env python

from imdb import IMDb

from .retrieve_classes import RetrieveResult, RetrieveResultItem

REGION = 'USA'

MAIN_KEY = 'main'
KIND_KEY = 'kind'
DATE_KEY = 'release dates'
SUB_ITEMS_KEY = 'episodes'

INFO_SET = [MAIN_KEY, DATE_KEY, SUB_ITEMS_KEY]

ITEMS_LIMIT = 2
SUB_ITEMS_LIMIT = 2

# general imdb result helpers
IA = IMDb()

def __search_items(search_terms):
    return IA.search_movie(search_terms)

def __get_item(movie_id, keys=IA.get_movie_infoset()):
    return IA.get_movie(movie_id, keys)

def __update_item(result, key):
    IA.update(result, info=key)

class ImdbResult(RetrieveResult):
    def __init__(self, search_terms, search_index):
        RetrieveResult.__init__(self, search_terms)

        # results
        self.search_results = __search_items(search_terms)
        self.search_result = self.search_results[search_index]

        # item
        item = __get_item(self.search_result.getID(), INFO_SET)
        sub_items = item.get(SUB_ITEMS_KEY, [])

        self.result_item = ImdbResultItem(item)

        print("retrieved item: " + str(self.result_item))

        # sub items
        for (index, sub_item_set) in sub_items.items():
            if index > ITEMS_LIMIT:
                continue

            self.sub_result_items[index] = {}

            for (i, sub_item) in sub_item_set.items():
                if i > SUB_ITEMS_LIMIT:
                    continue

                __update_item(sub_item, DATE_KEY)

                self.sub_result_items[index][i] = ImdbResultItem(sub_item)

                print("retrieved sub-item: " + str(self.sub_result_items[index][i]))


# general imdb result item helpers
def __parse_key_map(results):
    return dict(map(lambda x: x.split("::"), results))

def __get_value(results, key):
    return __parse_key_map(results)[key]

def __from_timestamp(date_string):
    from datetime import datetime

    return datetime.strptime(' '.join(date_string.split(' ')[:3]), '%d %B %Y')

class ImdbResultItem(RetrieveResultItem):
    def __init__(self, item):
        self.item_id = item.getID()
        self.kind = item[KIND_KEY]
        self.name = str(item)
        self.timestamp = __from_timestamp(
            __get_value(
                item[DATE_KEY],
                REGION
            )
        )


def get_imdb_result(search_terms, search_index):
    return ImdbResult(search_terms, search_index)
