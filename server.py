#!/usr/bin/env python

import os
from flask import Flask, render_template, request
from datetime import datetime
app = Flask(__name__)

from imdb import IMDb
ia = IMDb()
default_infoset = ia.get_movie_infoset()

def get_split(results):
    return dict(map(lambda x: x.split("::"), results))

def get_split_key(results, key):
    return get_split(results)[key]

def to_date(date_string):
    return datetime.strptime(date_string, '%d %B %Y').date()

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

def get_imdb_result(search, index=0):
    return get_imdb_results(search)[index]

def get_imdb_limit(search, region='UK'):
    key = 'release dates'

    results = ia.search_movie(search)
    result = ia.get_movie(results[0].getID(), info=[key])

    return to_date(get_split_key(result[key], region))

@app.route("/imdb/<search>/", defaults={'index': 0})
@app.route("/imdb/<search>/<int:index>")
def imdb(search, index):
    results = ia.search_movie(search)
    result = results[index]

    annotate_result_safe(result, ['release dates'])
    attributes = { k: result.get(k) for k in result.current_info }

    limit = to_date(get_split_key(attributes['release dates'], 'UK'))

    return render_template(
        'imdb.html',
        results=results,
        info=default_infoset,
        limit=limit,
        attributes=attributes
    )

@app.route("/limit")
def limit():
    search = request.args.get('search')
    tilds = request.args.get('tilds')

    limit = get_imdb_limit(search)

    return render_template(
        'limit.html',
        limit=limit
    )

@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='localhost', port=os.environ.get('PORT', 3000), debug=True)
