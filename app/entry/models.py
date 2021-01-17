from app import db
from sqlalchemy import Column, Integer, ForeignKey


class Entry(db.Model):
    """ Represents an entry in the purse """
    __tablename__ = 'Entries'
    id = db.Column(db.Integer, primary_key=True)
    game_session = db.Column(db.Integer)
    description = db.Column(db.String(150), default='')
    amount = db.Column(db.Float)
    character_id = Column(Integer, ForeignKey('Characters.id'))
