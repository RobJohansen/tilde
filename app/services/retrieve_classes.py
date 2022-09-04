#!/usr/bin/env python

class RetrieveResult:
    '''
    Collection of retrieve result items and sub items.
    '''

    # terms
    search_terms = None

    # results
    search_results = None
    search_result = None

    # result items
    result_item = None
    sub_result_items = {}

    def __init__(self, search_terms):
        self.search_terms = search_terms

    def __repr__(self):
        return '<{} (sub: {})>'.format(
            self.result_item,
            len(self.sub_result_items)
        )

class RetrieveResultItem:
    '''
    Representing item of retrieve result.
    '''

    item_id = None
    kind = None
    name = None
    timestamp = None

    def __repr__(self):
        return '<[{} {}] {}>'.format(
            self.kind,
            self.item_id,
            self.name,
        )
