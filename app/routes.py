'''Tilde Routes'''

from datetime import datetime
from flask import render_template, request
from app import app, db
from app.models import User, Node, NodeTerm

from app.services.wiki import get_wiki_rev_url
from app.services.imdb import get_imdb_result

RENDER_SERVICE = "WIKIPEDIA"
SEARCH_SERVICE = "IMDB"

def upsert_result(result):
    node = Node.query.filter_by(name=result.result_item.name).first()

    # create node structure
    if node is None:
        node = Node(
            name=result.result_item.name,
            timestamp=result.result_item.timestamp
        )
        db.session.add(node)

        for (key, sub_result_items) in result.sub_result_items.items():
            parent_node = Node(
                name="Season {}".format(key),
                timestamp=min(map(lambda n: n.timestamp, sub_result_items.values())),
                parent=node
            )
            db.session.add(parent_node)

            for (_, sub_result_item) in sub_result_items.items():
                child_node = Node(
                    name=sub_result_item.name,
                    timestamp=sub_result_item.timestamp,
                    parent=parent_node
                )
                db.session.add(child_node)

    # register term
    term = NodeTerm(
        term=result.search_terms,
        node=node
    )
    db.session.add(term)

    db.session.commit()

    return term


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route("/")
def index():
    return render_template(
        'index.html',
        user=User.query.first()
    )


@app.route("/purge")
def purge():
    Node.query.delete()
    NodeTerm.query.delete()
    db.session.commit()

    return "success"


@app.route("/search/<search_terms>/", defaults={'search_index': 0})
@app.route("/search/<search_terms>/<int:search_index>")
def search(search_terms, search_index):
    result = None

    term = NodeTerm.query.filter_by(term=search_terms).first()

    if term is None:
        if SEARCH_SERVICE == "IMDB":
            result = get_imdb_result(search_terms, search_index)
        else:
            NotImplementedError()

        term = upsert_result(result)

    return render_template(
        'search.html',
        term=term,
        result=result
    )


@app.route("/render/<page_terms>/")
def render(page_terms):
    url = None
    node = None
    date_time = None

    node_id = request.args.get('node_id')

    if node_id:
        node = Node.query.get(node_id)
        date_time = node.timestamp
    else:
        date_time = datetime.strptime(request.args.get('date_time'), '%Y%m%d')

    if SEARCH_SERVICE == "IMDB":
        url = get_wiki_rev_url(page_terms, date_time)
    else:
        NotImplementedError()

    return render_template(
        'render.html',
        url=url,
        node=node,
        date_time=date_time
    )
