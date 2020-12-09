from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.email)

class Node(db.Model):
    # fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    timestamp = db.Column(db.DateTime, index=True)

    # relationships
    terms = db.relationship("NodeTerm", lazy="joined")
    children = db.relationship("Node", lazy="joined", join_depth=2,
        backref=db.backref('parent', remote_side=[id])
    )

    def __repr__(self):
        return '<Node {}>'.format(self.name)

class NodeTerm(db.Model):
    # fields
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(64), index=True, unique=True)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))

    # relationships
    node = db.relationship("Node", back_populates="terms")

    def __repr__(self):
        return '<NodeTerm {} {}>'.format(self.term, self.node_id)