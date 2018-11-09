import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, flash
)

from werkzeug.security import check_password_hash, generate_password_hash

from shortener.db import get_db

#Need to make sure the blueprint knows what to go by.
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Register a new user.

    Validates that the username is not already taken. Hashes the password
    for security.
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        db_cursor = db.cursor(buffered=True)
        error = None



        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            db_cursor.execute(
                'SELECT id from users WHERE username=%s', (username,)
            )
            if db_cursor.fetchone() is not None:
                error = 'User {0} is already registered.'.format(username)

        if error is None:
            #The name is available, store it in the database and go to
            #the login page
            db_cursor.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                (username, generate_password_hash(password),)
            )
            db.commit()
            return redirect(url_for('url_shorten.index'))

        flash(error)

    return render_template('auth/register.html')