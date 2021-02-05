from flask import render_template
from web import Blueprint

error = Blueprint('error', __name__)


@error.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@error.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
