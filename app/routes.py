'''Tilde Routes'''

from datetime import datetime
from flask import request, jsonify, render_template
from app import app, db
from app.models import User, Node, NodeTerm

from app.services.wiki import get_wiki_rev_url
from app.services.imdb import get_imdb_result

# RENDER CONFIG
SEARCH_SERVICE = "IMDB"
RENDER_SERVICE = "WIKIPEDIA"


# PAGE ENDPOINTS
@app.route("/")
def index():
    return render_template_with_context(
        'index.html'
    )


# SEARCH ENDPOINTS
@app.route('/search', methods=['GET'])
def search():
    node_id = request.args.get('node_id')
    terms = request.args.get('terms')

    matches = Node.query.filter_by(
        parent_id=(None if node_id == '' else node_id)
    ).filter(
        Node.name.like("%{}%".format(terms))
    ).all()

    return jsonify({
        'results': [
            {
                'id': child.id,
                'name': child.name,
                'timestamp': child.timestamp
            } for child in matches
        ]
    })


@app.route("/retrieve/<terms>/", defaults={'results_index': 0})
@app.route("/retrieve/<terms>/<int:results_index>")
def retrieve(terms, results_index):
    term = NodeTerm.query.filter_by(name=terms).first()

    if term is None:
        if SEARCH_SERVICE == "IMDB":
            result = get_imdb_result(terms, results_index)
        else:
            NotImplementedError()

        term = upsert_result(result)

    return render_template_with_context(
        'debug_retrieve.html',
        term=term
    )


@app.route('/search/page', methods=['GET'])
def search_page():
    url = None
    node = None
    timestamp = None

    node_id = request.args.get('node_id')
    terms = request.args.get('terms')

    if node_id:
        node = Node.query.get(node_id)
        timestamp = node.timestamp
    else:
        timestamp = datetime.strptime(request.args.get('date_time'), '%Y%m%d')

    if SEARCH_SERVICE == "IMDB":
        url = get_wiki_rev_url(terms, timestamp)
    else:
        NotImplementedError()

    return jsonify({
        'url': url,
        'timestamp': timestamp
    })


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
