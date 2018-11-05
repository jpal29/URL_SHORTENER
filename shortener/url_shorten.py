import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request
)

#Need to make sure the blueprint knows what to go by.
bp = Blueprint('url_shorten', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    """Just show a basic html page for now"""
    if request.method == 'POST':
        url = request.form['url']
        #db = get_db()
        print(url)
        error = None

        if not url:
            error = 'URL is required'

        if error is None:
            return redirect(url_for('url_shorten.index'))
    return render_template('index.html')
