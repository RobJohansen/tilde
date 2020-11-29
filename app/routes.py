from flask import render_template, request
from app import app
from app.models import User

from app.services.wiki import get_wiki_url
from app.services.imdb import ImdbItem

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route("/")
def index():
    # tilds = request.args.get('tilds')

    return render_template(
        'index.html',
        user=User.query.first()
    )

@app.route("/imdb/<search>/", defaults={'index': 0})
@app.route("/imdb/<search>/<int:index>")
def search_imdb(search, index):
    item = ImdbItem(search, index)

    return render_template(
        'imdb.html',
        item=item
    )

@app.route("/wiki/<imdb_page>/<wiki_page>")
def search_wiki(imdb_page, wiki_page):
    item = ImdbItem(imdb_page, 0)
    page = get_wiki_url(wiki_page, item.result_release_date)

    return render_template(
        'wiki.html',
        item=item,
        url=page
    )
