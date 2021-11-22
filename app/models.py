'''Tilde ORM Models'''

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref

from app import db

class User(db.Model):
    '''An actor using the system'''

    id = Column(Integer, primary_key=True)
    email = Column(String(120), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.email)

class Node(db.Model):
    '''The Node representing a root entity'''

    # fields
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    parent_id = Column(Integer, ForeignKey('node.id'))
    timestamp = Column(DateTime, index=True)

    # relationships
    terms = relationship("NodeTerm", lazy="joined")
    children = relationship("Node", lazy="joined", join_depth=2,
                            backref=backref('parent', remote_side=[id]))

    def __repr__(self):
        return '<Node {}>'.format(self.name)

class NodeTerm(db.Model):
    '''The matching terms referencing a Node'''

    # fields
    id = Column(Integer, primary_key=True)
    term = Column(String(64), index=True, unique=True)
    node_id = Column(Integer, ForeignKey('node.id'))
    node = db.relationship("Node", back_populates="terms")

    # relationships
    node = relationship("Node", back_populates="terms")

    def __repr__(self):
        return '<NodeTerm {} {}>'.format(self.term, self.node_id)
