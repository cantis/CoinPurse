from flask import Flask, render_template, url_for, redirect
from flask.globals import request
from config import DevConfig
from flask_table import Table, Col
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

config = DevConfig()
app.config.from_object(config)

db = SQLAlchemy(app)
# To create the database at the command line execute:
#   python
#   >>>from app import db
#   >>>db.create_all()
#   >>>quit()


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    role = db.Column(db.String(25), nullable=False)
    salary = db.Column(db.String(10), nullable=False)


class TransactionsTable(Table):
    classes = ['table']
    table_id = 'tranTable'
    thead_classes = ['table__header']
    no_items = 'empty'

    def get_tr_attrs(self, item):
        return{'class': 'table__row'}
    name = Col('Name', th_html_attrs={'class': 'table__header'}, td_html_attrs={'class': 'table__cell'})
    role = Col('Role', th_html_attrs={'class': 'table__header'}, td_html_attrs={'class': 'table_cell'})
    salary = Col('Salary', th_html_attrs={'class': 'table__header'}, td_html_attrs={'class': 'table_cell'})


@app.route('/', methods=['get'])
def index():
    entries = Entry.query.all()
    table = TransactionsTable(entries)
    return render_template('index.html', table=table)


@app.route('/add', methods=['post'])
def add_transaction():
    name = request.form.get('name')
    role = request.form.get('role')
    salary = request.form.get('salary')
    new_entry = Entry(name=name, role=role, salary=salary)
    db.session.add(new_entry)
    db.session.commit()

    return redirect(url_for('index'))
