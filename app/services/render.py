#!/usr/bin/env python

from app.services.render_wiki import get_wiki_result

RENDER_SERVICE = "WIKI"

def get_render_result(terms, timestamp):
    if RENDER_SERVICE == "WIKI":
        return get_wiki_result(terms, timestamp)
    else:
        NotImplementedError()