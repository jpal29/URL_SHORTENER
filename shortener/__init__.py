import os
import datetime
from flask import Flask, render_template, session
from shortener import (
    url_shorten, auth
)




def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)


    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from shortener import db
    db.init_app(app)

    #apply the blueprints to the app
    app.register_blueprint(url_shorten.bp)
    app.register_blueprint(auth.bp)

    #setting session to timeout after 2 hours
    app.permanent_session_lifetime = datetime.timedelta(hours=2)

    #One way to verify that the app has successfully registered the blueprint
    #print(app.url_map)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index

    return app


