#!/usr/bin/env python

import requests

WIKI_URL = 'http://en.wikipedia.org'

WIKI_URL_QUERY = WIKI_URL + \
    '/w/api.php' + \
    '?action=query' + \
    '&prop=revisions' + \
    '&format=json' + \
    '&rvprop=ids' + \
    '&rvlimit=1' + \
    '&rvstart={timestamp}' + \
    '&titles={page_title}'

WIKI_URL_REVISION = WIKI_URL + \
    '/w/index.php' + \
    '?oldid={rev_id}'

WIKI_DATE_FORMAT = "%Y%m%d%H%M%S"


def get_json(url):
    try:
        return requests.get(url).json()

    except Exception:
        return None


def get_wiki_query(page_title, page_timestamp):
    url = WIKI_URL_QUERY.format(**{
        'page_title': page_title,
        'timestamp':  page_timestamp.strftime(WIKI_DATE_FORMAT)
    })

    print(url)

    return get_json(url)


def get_wiki_rev(page_title, page_timestamp):
    json = get_wiki_query(page_title, page_timestamp)

    if json:
        pages = json['query']['pages']
        page_id = list(pages.keys())[0]

        page = pages[page_id]
        revisions = page.get('revisions')

        if revisions:
            if page_timestamp:
                return revisions[0]['revid']

            else:
                return revisions[0]['parentid']

    return None


def get_wiki_rev_url(page_title, timestamp):
    rev_id = get_wiki_rev(page_title, timestamp)

    if rev_id:
        return WIKI_URL_REVISION.format(**{
            'rev_id': rev_id
        })

    return None
