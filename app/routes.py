from flask import render_template, request
from app import app, db
from app.models import User, Node, NodeTerm

from app.services.wiki import get_wiki_url
from app.services.imdb import ImdbItem

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route("/")
def index():
    return render_template(
        'index.html',
        user=User.query.first()
    )

@app.route("/imdb/<search>/", defaults={'index': 0})
@app.route("/imdb/<search>/<int:index>")
def search_imdb(search, index):
    force = request.args.get('force') is not None

    item = None
    term = NodeTerm.query.filter_by(term=search).first()

    if force or term is None:
        # todo: prune based on search
        if force:
            Node.query.delete()
            NodeTerm.query.delete()
            db.session.commit()

        item = ImdbItem(search, index)

        node = Node(
            name=item.node.name,
            timestamp=item.node.timestamp
        )

        term = NodeTerm(
            term=search,
            node=node
        )

        db.session.add(node)
        db.session.add(term)

        db.session.commit()

    return render_template(
        'node.html',
        node=term.node,
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
