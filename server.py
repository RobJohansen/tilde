#!/usr/bin/env python

import os
from interfaces.imdb import *
from interfaces.wiki import *
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/imdb/<search>/", defaults={'index': 0})
@app.route("/imdb/<search>/<int:index>")
def imdb(search, index):
    results = get_movie(search)
    result = results[index]

    annotate_result_safe(result, ['release dates'])
    attributes = { k: result.get(k) for k in result.current_info }

    limit = to_date_time(get_split_key(attributes['release dates'], 'UK'))

    return render_template(
        'imdb.html',
        results=results,
        info=default_infoset,
        limit=limit,
        attributes=attributes
    )

@app.route("/wiki/<imdb_page>/<wiki_page>")
def wiki(imdb_page, wiki_page):
    limit = get_imdb_limit(imdb_page)
    page = get_wiki_url(wiki_page, limit)

    return render_template(
        'wiki.html',
        limit=limit,
        url=page
    )

@app.route("/")
def index():
    tilds = request.args.get('tilds')

    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == "__main__":
    app.run(
        host='localhost',
        port=os.environ.get('PORT', 3000),
        debug=True
    )
