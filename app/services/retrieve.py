#!/usr/bin/env python

from app import app, db
from app.models import Node, NodeTerm
from app.services.retrieve_imdb import get_imdb_result

RETRIEVE_SERVICE = "IMDB"

def get_retrieve_result(terms, results_index):
    if RETRIEVE_SERVICE == "IMDB":
        return get_imdb_result(terms, results_index)
    else:
        NotImplementedError()

def upsert_retrieve_result(result):
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
