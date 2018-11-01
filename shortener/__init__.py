import os
from flask import Flask
from dotenv import load_dotenv
from flaskext.mysql import MySQL
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
#from config import app_config

# Loading environment variables
load_dotenv()
load_dotenv(dotenv_path='../.env')

#db = MySQL()
db = SQLAlchemy()

def create_app(config_name):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    db_user = os.getenv('shortener_db_user')
    db_password = os.getenv('shortener_db_password')
    db_name = os.getenv('shortener_db_name')
    db_host = 'localhost'
    db_port = '3306'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}:{}/{}'.format(db_user, db_password, db_host, db_port, db_name)

    #app.config.from_object(app_config[config_name])
    #app.confg.from_pyfile('config.py')

    db.init_app(app)

    migrate = Migrate(app, db)

    from shortener import models

    @app.route('/hello')
    def hello():
        return 'Hello World'

    return app



