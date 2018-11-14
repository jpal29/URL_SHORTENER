import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, flash, session, g
)

from werkzeug.security import check_password_hash, generate_password_hash

from shortener.db import get_db

#Need to make sure the blueprint knows what to go by.
bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """
    If a user id is stored in the session, load the user object from the database into ``g.user``.
    """
    print(session.get('user_id'))
    user_id = session.get('user_id')



    if user_id is None:
        g.user = None
    else:
        db = get_db()
        db_cursor = db.cursor(buffered=True)
        db_cursor.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,)
        )
        g.user = db_cursor.fetchone()


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

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        db_cursor = db.cursor(buffered=True)
        error = None
        db_cursor.execute(
            'SELECT * FROM users WHERE username = %s', (username,)
        )
        user = db_cursor.fetchone()
        print(user)
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('url_shorten.index'))

        # TODO create login template
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """
    Clear the current session, including the stored user id.
    """
    session.clear()
    return redirect(url_for('url_shorten.index'))