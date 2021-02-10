from flask_login import UserMixin
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from web import db, login_manager


class Entry(db.Model):
    """ Represents an entry in the purse """
    __tablename__ = 'Entries'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    game_session = db.Column(db.Integer)
    description = db.Column(db.String(150), default='')
    amount = db.Column(db.Float)
    character_id = Column(Integer, ForeignKey('Characters.id'))


class Character(db.Model):
    """ Represents a character """
    __tablename__ = 'Characters'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    is_dead = db.Column(db.Boolean, default=False)
    entries = relationship('Entry', backref='character')


class Setting(db.Model):
    """ represents persistent settings for the application """
    __tablename__ = 'Settings'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(), nullable=False)
    value = db.Column(db.String(), nullable=False)


class User(db.Model, UserMixin):
    """ represents an application user """
    __tablename__ = 'Users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)


def init_db():
    db.create_all()
