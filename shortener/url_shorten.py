import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, make_response, g
)
import base64

from shortener.auth import login_required
from shortener.db import get_db
from shortener.encode import toBase10
from shortener.encode import toBase64

#Need to make sure the blueprint knows what to go by.
bp = Blueprint('url_shorten', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    """Just show a basic html page for now"""
    if request.method == 'POST':
        url = request.form['url']
        db = get_db()



        print(url)
        error = None

        if not url:
            error = 'URL is required'

        if error is None:
            return redirect(url_for('url_shorten.index'))
    return render_template('index.html')

@bp.route('/shorten', methods=('GET', 'POST'))
@login_required
def shorten():
    """Create a new shortened url."""
    if request.method == 'POST':
        url = request.form['url']
        error = None
        if not url:
            error = 'URL is required.'

        if error is not None:
            flash(error)
        else:
            encoded_url = str.encode(url)
            b64_url = base64.urlsafe_b64encode(encoded_url)
            decoded_b64_url = b64_url.decode()
            db = get_db()
            db_cursor = db.cursor(buffered=True)
            db_cursor.execute(
                'INSERT INTO urls (user_id, url) '
                'VALUES (%s, %s)',
                (g.user[0], decoded_b64_url, )
            )
            db.commit()
            print('URL ID: {}'.format(db_cursor.lastrowid))
            encoded_string_1 = toBase64(db_cursor.lastrowid)
            encoded_string_2 = toBase64(22111)
            print('Encoded String 1: {}'.format(encoded_string_1))
            print('Encoded String 2: {}'.format(encoded_string_2))
            return render_template('index.html', short_url=encoded_string_2)
    return render_template('shorten.html')

@bp.route('/<short_url>')
def redirect_short_url(short_url):
    decoded = toBase10(short_url)
    url = 'http://127.0.0.1:5000'  # fallback if no URL is found
    db = get_db()
    db_cursor = db.cursor(buffered=True)
    res = db_cursor.execute('SELECT url FROM urls WHERE id=%s', (decoded))
    try:
        short = res.fetchone()
        if short is not None:
            url = base64.urlsafe_b64decode(short[0])
    except Exception as e:
        print(e)
    return redirect(url)
