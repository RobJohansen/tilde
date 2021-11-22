'''Tilde Routes'''

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

@app.route("/imdb/<search_terms>/", defaults={'search_index': 0})
@app.route("/imdb/<search_terms>/<int:search_index>")
def search_imdb(search_terms, search_index):
    force = request.args.get('force') is not None

    item = None
    term = NodeTerm.query.filter_by(term=search_terms).first()

    if force or term is None:
        # TODO: prune based on search
        if force:
            Node.query.delete()
            NodeTerm.query.delete()
            db.session.commit()

        item = ImdbItem(search_terms, search_index)

        node = Node.query.filter_by(name=item.node.name).first()

        # create node structure
        if node is None:
            node = Node(
                name=item.node.name,
                timestamp=item.node.timestamp
            )
            db.session.add(node)

            for (key, sub_nodes) in item.sub_nodes.items():
                parent_node = Node(
                    name="Season {}".format(key),
                    timestamp=min(map(lambda n: n.timestamp, sub_nodes.values())),
                    parent=node
                )
                db.session.add(parent_node)

                for (_, sub_node) in sub_nodes.items():
                    child_node = Node(
                        name=sub_node.name,
                        timestamp=sub_node.timestamp,
                        parent=parent_node
                    )
                    db.session.add(child_node)

        term = NodeTerm(
            term=search_terms,
            node=node
        )
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
    page = get_wiki_url(wiki_page, item.node.timestamp)

    return render_template(
        'wiki.html',
        item=item,
        url=page
    )
