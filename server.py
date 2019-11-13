#!/usr/bin/env python

import os
from flask import Flask, render_template, request
app = Flask(__name__)

from imdb import IMDb
ia = IMDb()

@app.route("/test")
def imdb():
    search = request.args.get('search')

    results = ia.search_movie(search)
    
    return render_template('results.html', results=results)

@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='localhost', port=os.environ.get('PORT', 3000), debug=True)
