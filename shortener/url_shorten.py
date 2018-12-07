import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, make_response, g, flash
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
    if request.method == 'POST' and g.user:
        url = request.form['url']
        error = None
        if not url:
            error = 'URL is required.'

        # check that user has generated less than 10 queries
        db = get_db()
        db_cursor = db.cursor(buffered=True)
        db_cursor.execute('SELECT id, url FROM urls WHERE user_id=%s', (g.user[0],))
        urls = db_cursor.fetchall()
        if len(urls) >= 10:
            error = 'Max number of 10 urls shortened. Remove some to make some.'
        if error is not None:
            flash(error)
            return redirect(url_for('url_shorten.index'))
        else:
            encoded_url = str.encode(url)
            b64_url = base64.urlsafe_b64encode(encoded_url)
            decoded_b64_url = b64_url.decode()
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

    elif request.method == 'GET' and g.user:
        db = get_db()
        db_cursor = db.cursor(buffered=True)
        db_cursor.execute('SELECT id, url FROM urls WHERE user_id=%s', (g.user[0],))
        urls = db_cursor.fetchall()
        # need to change url to base64
        formatted_urls = []
        for url in urls:
            formatted_url = {}
            formatted_url['url_id'] = url[0]
            formatted_url['url'] = 'http://127.0.0.1:5000/{}'.format(toBase64(url[0]))
            formatted_urls.append(formatted_url)
        return render_template('index.html', formatted_urls=formatted_urls)
    else:
        return render_template('index.html')

@bp.route('/shorten', methods=['GET'])
@login_required
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

@bp.route('/delete', methods=['POST'])
@login_required
def delete():
    url_id = request.form.get("url_id")
    error = None
    if not url_id:
        error = 'Provide url id.'
    if error is not None:
        flash(error)
    db = get_db()
    db_cursor = db.cursor(buffered=True)
    db_cursor.execute('DELETE FROM urls where id=%s', (url_id,))
    db.commit()
    return redirect(url_for('url_shorten.index'))
