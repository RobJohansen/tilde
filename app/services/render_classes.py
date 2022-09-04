#!/usr/bin/env python

class RenderResult:
    '''
    Representing render result.
    '''

    url = None

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '<{}>'.format(
            self.url
        )
