import os

import pytest
from shortener import create_app

print(os.path.dirname(__file__))

@pytest.fixture
def app():

    app = create_app({
        'TESTING': True,
    })

    yield app

    #TODO remove the data from the database once all of the tests have run


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()