'''Tilde Routes'''

from datetime import datetime
from flask import request, jsonify, render_template
from app import app, db
from app.models import User, Node, NodeTerm

from app.services.wiki import get_wiki_rev_url
from app.services.imdb import get_imdb_result

# RENDER CONFIG
RENDER_SERVICE = "WIKIPEDIA"
SEARCH_SERVICE = "IMDB"


# PAGE ENDPOINTS
@app.route("/")
def index():
    return render_template_with_context(
        'index.html'
    )


# SEARCH ENDPOINTS
@app.route('/find', methods=['GET'])
def find():
    search_terms = request.args.get('terms')
    search_index = request.args.get('index')

    term = get_term(search_terms, search_index)

    return jsonify({
        'results': [
            {
                'name': term.name
            }
        ]
    })


@app.route("/search/<search_terms>/", defaults={'search_index': 0})
@app.route("/search/<search_terms>/<int:search_index>")
def search(search_terms, search_index):
    term = get_term(search_terms, search_index)

    return render_template_with_context(
        'search.html',
        term=term
    )


# RENDER ENDPOINTS
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

    return render_template_with_context(
        'render.html',
        url=url,
        node=node,
        date_time=date_time
    )


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


# RENDER HELPERS
def render_template_with_context(template, **kwargs):
    # TODO: user
    user = User.query.first()

    return render_template(
        template,
        user=user.email,
        **kwargs
    )


# DB ENDPOINTS
@app.route('/purge', methods=['POST'])
def purge():
    NodeTerm.query.delete()
    Node.query.delete()

    db.session.commit()

    return '', 200


# DB HELPERS
def get_term(search_terms, search_index):
    term = NodeTerm.query.filter_by(name=search_terms).first()

    if term is None:
        if SEARCH_SERVICE == "IMDB":
            result = get_imdb_result(search_terms, search_index)
        else:
            NotImplementedError()

        term = upsert_result(result)

    return term


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
        name=result.search_terms,
        node=node
    )
    db.session.add(term)

    # commit upserts
    db.session.commit()

    return term
