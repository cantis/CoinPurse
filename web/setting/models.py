from web import db


class Setting(db.Model):
    """ represents persistent settings for the application """
    __tablename__ = 'Settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(), nullable=False)
    value = db.Column(db.String(), nullable=False)
