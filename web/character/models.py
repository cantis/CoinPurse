from sqlalchemy.orm import relationship
from web import db


class Character(db.Model):
    """ Represents a character """
    __tablename__ = 'Characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    is_dead = db.Column(db.Boolean, default=False)
    entries = relationship('Entry', backref='character')
