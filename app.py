from flask import Flask, render_template, url_for, redirect
from flask.globals import request
from wtforms.fields.simple import HiddenField
from config import DevConfig
from flask_table import Table, Col
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)

config = DevConfig()
app.config.from_object(config)

db = SQLAlchemy(app)
# To create the database at the command line execute:
#   python
#   >>>from app import db
#   >>>db.create_all()
#   >>>quit()

bs = Bootstrap()
bs.init_app(app)


class Entry(db.Model):
    """ db table for coin purse entries """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    role = db.Column(db.String(25), nullable=False)
    salary = db.Column(db.String(10), nullable=False)


class TransactionsTable(Table):
    """ Defines an flask_table for HTML Render """
    classes = ['table']
    table_id = 'tranTable'
    thead_classes = ['table__header']
    no_items = 'empty'

    def get_tr_attrs(self, item):
        return{'class': 'table__row'}
    name = Col('Name', th_html_attrs={'class': 'table__header'}, td_html_attrs={'class': 'table__cell'})
    role = Col('Role', th_html_attrs={'class': 'table__header'}, td_html_attrs={'class': 'table_cell'})
    salary = Col('Salary', th_html_attrs={'class': 'table__header'}, td_html_attrs={'class': 'table_cell'})


class AddEntryForm(FlaskForm):
    """ Add Entry Form """
    id = HiddenField()
    name = StringField(label='Name', validators=[InputRequired('Please provide a name')])
    role = StringField(label='Role', validators=[InputRequired('Please provide a role')])
    salary = StringField(label='Salary', validators=[InputRequired('Please provide a salary')])


@app.route('/', methods=['get'])
def index():
    entries = Entry.query.all()
    table = TransactionsTable(entries)
    add_form = AddEntryForm()
    return render_template('index.html', table=table, add_form=add_form)


@app.route('/add', methods=['post'])
def add_transaction():
    """ Handle adding a new transaction """
    form = AddEntryForm()
    if form.validate_on_submit():
        new_entry = Entry(
            name=request.form.get('name'),
            role=request.form.get('role'),
            salary=request.form.get('salary')
            )
        db.session.add(new_entry)
        db.session.commit()

    return redirect(url_for('index'))
