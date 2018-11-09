import os
from flask import current_app, g
from flask.cli import with_appcontext
import mysql.connector

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

def get_db():
    """
    Connect to the application's configured database. The connection is unique
    for each request and will be reused if this is called again.
    """

    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=os.getenv('shortener_db_host'),
            user=os.getenv('shortener_db_user'),
            passwd=os.getenv('shortener_db_password'),
            database=os.getenv('shortener_db_name')
        )

        return g.db

def close_db(e=None):
    """
    If this request connected to the database, close the connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)




