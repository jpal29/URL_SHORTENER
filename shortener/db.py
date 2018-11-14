import os
from flask import current_app, g
from flask.cli import with_appcontext
import mysql.connector

import configparser

basedir = os.path.abspath(os.path.dirname(__file__))


config = configparser.ConfigParser()
config.read(os.path.join(basedir, 'config.ini'))

def get_db():
    """
    Connect to the application's configured database. The connection is unique
    for each request and will be reused if this is called again.
    """

    if 'db' not in g:
        if current_app.config['TESTING']:
            g.db = mysql.connector.connect(
                host=config['TESTING']['shortener_db_host'],
                user=config['TESTING']['shortener_db_user'],
                passwd=config['TESTING']['shortener_db_password'],
                database=config['TESTING']['shortener_db_name']
            )
        else:
            g.db = mysql.connector.connect(
                host=config['DEVELOPMENT']['shortener_db_host'],
                user=config['DEVELOPMENT']['shortener_db_user'],
                passwd=config['DEVELOPMENT']['shortener_db_password'],
                database=config['DEVELOPMENT']['shortener_db_name']
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




