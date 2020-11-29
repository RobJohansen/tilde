from flask import render_template, request
from app import app, db
from app.models import User, Node

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
    node = Node.query.filter_by(name=search).first()

    if node is None:
        item = ImdbItem(search, index)

        node = Node(
            name=search,
            timestamp=item.result_release_date
        )

        db.session.add(node)
        db.session.commit()

    return render_template(
        'node.html',
        node=node
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
