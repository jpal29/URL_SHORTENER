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

#Create short ID for URL

from shortid import ShortId

sid = ShortId()
print(sid.generate())


app = Flask(__name__)
# app.config['MYSQL_DATABASE_USER'] = os.getenv('shortener_db_user')
# app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('shortener_db_password')
# app.config['MYSQL_DATABASE_DB'] = os.getenv('shortener_db_name')
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'

db_user = os.getenv('shortener_db_user')
db_password = os.getenv('shortener_db_password')
db_name = os.getenv('shortener_db_name')
db_host = 'localhost'
db_port = '3306'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}:{}/{}'.format(db_user, db_password, db_host, db_port, db_name)



#app.config.from_object(app_config[config_name])
#app.confg.from_pyfile('config.py')

db = SQLAlchemy(app)

migrate = Migrate(db, app)

@app.route('/hello')
def hello():
    return 'Hello World'




