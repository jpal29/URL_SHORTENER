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
            encoded_id = toBase64(db_cursor.lastrowid)
            #TODO need to change host to https instead of http
            return redirect(url_for('url_shorten.shorten',
                                    short_url='http://127.0.0.1:5000/{}'.format(encoded_id)))
            #return render_template('shorten.html', short_url='http://127.0.0.1:5000/{}'.format(encoded_id))
    elif request.method == 'GET':
        if g.user:
            db = get_db()
            db_cursor = db.cursor(buffered=True)
            db_cursor.execute('SELECT id, url FROM urls WHERE user_id=%s', (g.user[0],))
            urls = db_cursor.fetchall()
            # need to change url to base64
            formatted_urls = []
            for url in urls:
                formatted_urls.append('http://127.0.0.1:5000/{}'.format(toBase64(url[0])))
            return render_template('index.html', formatted_urls=formatted_urls)
        else:
            return render_template('index.html')

@bp.route('/shorten', methods=['GET'])
def shorten():
    return render_template('shorten.html', short_url=request.args.get('short_url'))

@bp.route('/<short_url>')
def redirect_short_url(short_url):
    decoded = toBase10(short_url)
    print('Decoded: {}'.format(decoded))
    #TODO need to change host to https instead of http
    url = 'http://127.0.0.1:5000'  # fallback if no URL is found
    db = get_db()
    db_cursor = db.cursor(buffered=True)
    db_cursor.execute('SELECT url FROM urls WHERE id=%s', (decoded,))
    try:
        short = db_cursor.fetchone()
        if short is not None:
            url = base64.urlsafe_b64decode(short[0])
    except Exception as e:
        print(e)
    return redirect(url)
