'''Tilde Routes'''

from datetime import datetime
from flask import request, jsonify, render_template
from app import app, db
from app.models import User, Node, NodeTerm

from app.services.render import get_render_result
from app.services.retrieve import get_retrieve_result, upsert_retrieve_result

# JSON ENDPOINTS
@app.route('/search/nodes', methods=['GET'])
def search_nodes():
    # Get Nodes
    parent_id = request.args.get('parent_id')
    query = request.args.get('query')
    nodes = search_nodes(parent_id, query)

    return jsonify({
        'results': [
            {
                'id': node.id,
                'name': node.name,
                'timestamp': node.timestamp
            } for node in nodes
        ]
    })


@app.route('/search/page', methods=['GET'])
def search_page():
    # Get Timestamp
    node_id = request.args.get('node_id')
    date_time = request.args.get('date_time')
    (_, timestamp) = get_node_timestamp(node_id, date_time)

    # Get Render Result
    query = request.args.get('query')
    render_result = get_render_result(query, timestamp)

    return jsonify({
        'page_url': render_result.url
    })


# RENDER ENDPOINTS
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route("/")
def index():
    return render_template_with_context(
        'index.html'
    )


def render_template_with_context(template, **kwargs):
    # TODO: user
    user = User.query.first()

    return render_template(
        template,
        user=user.email,
        **kwargs
    )


# DEBUG HELPERS
@app.route("/debug/retrieve/<terms>/", defaults={'results_index': 0})
@app.route("/debug/retrieve/<terms>/<int:results_index>")
def debug_retrieve(terms, results_index):
    term = get_node_term(terms)

    if term is None:
        retrieve_result = get_retrieve_result(terms, results_index)

        term = upsert_retrieve_result(retrieve_result)

    return render_template_with_context(
        'debug_retrieve.html',
        term=term
    )


@app.route("/debug/render/<terms>/")
def debug_render(terms):
    # Get Timestamp
    node_id = request.args.get('node_id')
    date_time = request.args.get('date_time')
    (node, timestamp) = get_node_timestamp(node_id, date_time)

    # Get Render Result
    terms = request.args.get('terms')
    render_result = get_render_result(terms, timestamp)

    return render_template_with_context(
        'debug_render.html',
        url=render_result.url,
        node=node,
        date_time=date_time
    )


# DB ENDPOINTS
@app.route('/purge', methods=['POST'])
def purge():
    NodeTerm.query.delete()
    Node.query.delete()

    db.session.commit()

    return '', 200


# HELPERS
def search_nodes(parent_id, query):
    return Node.query.filter_by(
        parent_id=(None if parent_id == '' else parent_id)
    ).filter(
        Node.name.like("%{}%".format(query))
    ).all()


def get_node_term(terms):
    return NodeTerm.query.filter_by(
        name=terms
    ).first()

def get_node_timestamp(node_id, date_time):
    node = None
    timestamp = None

    if node_id:
        node = Node.query.get(node_id)
        timestamp = node.timestamp
    elif date_time:
        timestamp = datetime.strptime(date_time, '%Y%m%d')
    else:
        timestamp = datetime.now()

    return (node, timestamp)