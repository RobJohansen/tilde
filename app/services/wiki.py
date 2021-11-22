#!/usr/bin/env python

import requests

WIKI_URL_ROOT = 'http://en.wikipedia.org'

WIKI_URL_QRY = WIKI_URL_ROOT + \
    '/w/api.php' + \
    '?action=query' + \
    '&prop=revisions' + \
    '&format=json' + \
    '&rvprop=ids' + \
    '&rvlimit=1' + \
    '&rvstart={timestamp}' + \
    '&titles={page_title}'

WIKI_URL_REV = WIKI_URL_ROOT + \
    '/w/index.php' + \
    '?oldid={rev_id}'

def get_json(url):
    try:
        return requests.get(url).json()

    except Exception:
        return None

def get_wiki_rev(page_title, timestamp):
    url = WIKI_URL_QRY.format(**{
        'page_title': page_title,
        'timestamp': timestamp
    })

    json = get_json(url)

    if json:
        pages = json['query']['pages']
        page_id = list(pages.keys())[0]

        page = pages[page_id]
        revisions = page.get('revisions')

        if revisions:
            if timestamp:
                return revisions[0]['revid']

            else:
                return revisions[0]['parentid']

    return None

def get_wiki_url(page_title, timestamp):
    rev_id = get_wiki_rev(page_title, timestamp)

    if rev_id:
        return WIKI_URL_REV.format(**{
            'rev_id': rev_id
        })

    return None
